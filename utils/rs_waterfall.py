
## Almost similar to Nick's version with the ID variables 
def process_resp_support(df):
    # Step 1: Initiate

    print("Initiating waterfall")
    # Step 2: Order Data for Filling
    df = df.sort_values(by=['encounter_id', 'recorded_dttm'])
    print("Sorted encounters and recorded time")
    
    # Step 3: Fix Missing `device_category` 
    print("Fixing device category")
    df['device_category'] = np.where(
        df['device_category'].isna() & df['device_name'].isna() & 
        df['mode_category'].str.contains("Assist Control-Volume Control|SIMV|Pressure Control", na=False),
        'Vent',
        df['device_category']
    )
    
    # Step 4: Fill Vent and NIPPV based on adjacent rows (Forward fill and Backward fill)
    df['device_category'] = df['device_category'].ffill().bfill()

    # Step 5: Assigning Vent to Missing `device_category` where appropriate
    df['device_category'] = np.where(
        df['device_category'].isna() & ~df['device_name'].str.contains("Trach", na=False) &
        df['tidal_volume_set'].gt(0) & df['resp_rate_set'].gt(0),
        'Vent',
        df['device_category']
    )

    df['mode_category'] = np.where(
        df['mode_category'].isna() & ~df['device_name'].str.contains("Trach", na=False) &
        df['tidal_volume_set'].gt(0) & df['resp_rate_set'].gt(0),
        'Assist Control-Volume Control',
        df['mode_category']
    )
    
    # Fill forward device_category
    print('Fill forward device_category')
    df['device_category'] = df.groupby('encounter_id')['device_category'].ffill()

    # Create device_cat_id to identify unique device sequences
    df['device_cat_f'] = df['device_category'].fillna('missing')
    df['device_cat_f'] = pd.factorize(df['device_cat_f'])[0] + 1
    df['device_cat_id'] = (df['device_cat_f'] != df.groupby('encounter_id')['device_cat_f'].shift()).cumsum()

    # Fill device_name within each device_cat_id group (down and up)
    df['device_name'] = df.groupby(['encounter_id', 'device_cat_id'])['device_name'].ffill().bfill()

    # Create device_id to identify unique device names
    df['device_name_f'] = df['device_name'].fillna('missing')
    df['device_name_f'] = pd.factorize(df['device_name_f'])[0] + 1
    df['device_id'] = (df['device_name_f'] != df.groupby('encounter_id')['device_name_f'].shift()).cumsum()

    # Fill mode_category within each device_id group (down and up)
    df['mode_category'] = df.groupby(['encounter_id', 'device_id'])['mode_category'].ffill().bfill()

    # Create mode_cat_id to identify unique mode sequences
    df['mode_cat_f'] = df['mode_category'].fillna('missing')
    df['mode_cat_f'] = pd.factorize(df['mode_cat_f'])[0] + 1
    df['mode_cat_id'] = (df['mode_cat_f'] != df.groupby('device_id')['mode_cat_f'].shift()).cumsum()

    # Fill mode_name within each mode_cat_id group (down and up)
    df['mode_name'] = df.groupby(['encounter_id', 'mode_cat_id'])['mode_name'].ffill().bfill()

    # Create mode_name_id to identify unique mode names
    df['mode_name_f'] = df['mode_name'].fillna('missing')
    df['mode_name_f'] = pd.factorize(df['mode_name_f'])[0] + 1
    df['mode_name_id'] = (df['mode_name_f'] != df.groupby('mode_cat_id')['mode_name_f'].shift()).cumsum()

    # If fio2 is missing and device_category is 'room air', set fio2 to 0.21
    print('fio2 is missing and device_category is 'room air', set fio2 to 0.21')
    df['fio2_set'] = np.where(df['fio2_set'].isna() & (df['device_category'] == 'room air'), 0.21, df['fio2_set'])

    # Carry forward the remaining variables within each mode_name_id group
    print('Carry forward the remaining variables')
    vars_to_fill = [
        'fio2_set', 'lpm_set', 'tidal_volume_set', 'resp_rate_set',
        'pressure_control_set', 'pressure_support_set', 'flow_rate_set',
        'peak_inspiratory_pressure_set', 'inspiratory_time_set', 'peep_set',
        'tidal_volume_obs', 'resp_rate_obs', 'plateau_pressure_obs',
        'peak_inspiratory_pressure_obs', 'peep_obs', 'minute_vent_obs'
    ]
    df[vars_to_fill] = df.groupby(['encounter_id', 'mode_name_id'])[vars_to_fill].ffill().bfill()

    # Fill tracheostomy (down only)
    df['tracheostomy'] = df.groupby('encounter_id')['tracheostomy'].ffill()

    # Handle Duplicates: Keep the first occurrence
    df = df.drop_duplicates(subset=['encounter_id', 'recorded_dttm'])

    return df


## Simpler version without the IDs- much faster

def process_resp_support(df):
    # Step 1: Initiate
    print("Initiating waterfall")

    # Step 2: Order Data for Filling
    df = df.sort_values(by=['encounter_id', 'recorded_dttm'])
    print("Sorted encounters and recorded time")
    
    # Step 3: Fix Missing `device_category`
    print("Fixing device category")
    df['device_category'] = np.where(
        df['device_category'].isna() & df['device_name'].isna() & 
        df['mode_category'].str.contains("Assist Control-Volume Control|SIMV|Pressure Control", na=False),
        'Vent',
        df['device_category']
    )
    
    # Step 4: Fill `device_category` based on adjacent rows (Forward fill and Backward fill)
    df['device_category'] = df['device_category'].ffill().bfill()

    # Step 5: Assigning `Vent` to Missing `device_category` where appropriate
    df['device_category'] = np.where(
        df['device_category'].isna() & ~df['device_name'].str.contains("Trach", na=False) &
        df['tidal_volume_set'].gt(0) & df['resp_rate_set'].gt(0),
        'Vent',
        df['device_category']
    )

    df['mode_category'] = np.where(
        df['mode_category'].isna() & ~df['device_name'].str.contains("Trach", na=False) &
        df['tidal_volume_set'].gt(0) & df['resp_rate_set'].gt(0),
        'Assist Control-Volume Control',
        df['mode_category']
    )
    
    # Fill forward and backward `device_name` and `mode_name` within each encounter
    print('Filling forward and backward device_name and mode_name')
    df['device_name'] = df.groupby('encounter_id')['device_name'].ffill().bfill()
    df['mode_name'] = df.groupby('encounter_id')['mode_name'].ffill().bfill()

    # Fill forward and backward `mode_category` within each encounter
    df['mode_category'] = df.groupby('encounter_id')['mode_category'].ffill().bfill()

    # If `fio2_set` is missing and `device_category` is 'room air', set `fio2_set` to 0.21
    print("Filling missing fio2_set where device_category is 'room air'")
    df['fio2_set'] = np.where(df['fio2_set'].isna() & (df['device_category'] == 'room air'), 0.21, df['fio2_set'])

    # Carry forward the remaining variables within each encounter
    print('Carrying forward the remaining variables')
    vars_to_fill = [
        'fio2_set', 'lpm_set', 'tidal_volume_set', 'resp_rate_set',
        'pressure_control_set', 'pressure_support_set', 'flow_rate_set',
        'peak_inspiratory_pressure_set', 'inspiratory_time_set', 'peep_set',
        'tidal_volume_obs', 'resp_rate_obs', 'plateau_pressure_obs',
        'peak_inspiratory_pressure_obs', 'peep_obs', 'minute_vent_obs'
    ]
    df[vars_to_fill] = df.groupby('encounter_id')[vars_to_fill].ffill().bfill()

    # Fill `tracheostomy` (down only)
    print('Filling tracheostomy (down only)')
    df['tracheostomy'] = df.groupby('encounter_id')['tracheostomy'].ffill()

    # Handle Duplicates: Keep the first occurrence
    print('Removing duplicates')
    df = df.drop_duplicates(subset=['encounter_id', 'recorded_dttm'])

    return df