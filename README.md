# Eligibility for Mobilization

## Objective

The primary objective of this project is to determine the windows of opportunity for safely mobilizing patients on ventilators within the first 72 hours of intubation, during business hours (8am-5pm). The analysis is guided by two established criteria sets, *Patel et al.* and *TEAM Study*, as well as a consensus criteria approach, which includes Green, Yellow, and Red safety flags.

## Criteria for Safe Therapy

### 1. Patel et al. Criteria
The *Patel et al.* criteria define safe physiological ranges that must be met for mobilization:
- **Mean arterial blood pressure (MAP):** 65-110 mm Hg
- **Systolic blood pressure (SBP):** ≤ 200 mm Hg
- **Heart rate:** 40-130 beats per minute
- **Respiratory rate:** 5-40 breaths per minute
- **Pulse oximetry (SpO2):** ≥ 88%

### 2. TEAM Study Criteria
The *TEAM Study* criteria focus on hemodynamic and respiratory stability:
- **Heart rate:** ≤ 150 bpm
- **Most recent lactate:** ≤ 4.0 mmol/L
- **Noradrenaline infusion rate:**
  - ≤ 0.2 mcg/kg/min, OR
  - 0.1-0.2 mcg/kg/min (without an increase in the infusion rate of more than 25% in the last 6 hours)
- **Respiratory stability:**
  - FiO2: ≤ 0.6
  - PEEP: ≤ 16 cm H2O
- **Current respiratory rate:** ≤ 45 breaths per minute

### 3. Consensus Criteria
The Consensus Criteria categorize safety flags into Green, Yellow, and Red, providing a hierarchical assessment of patient stability:

#### Green Criteria
- **Respiratory:**
  - SpO2 ≥ 90%
  - Respiratory rate ≤ 30 breaths/min
  - FiO2 ≤ 0.6
  - PEEP ≤ 10 cm H2O
- **Cardiovascular:**
  - MAP ≥ 65 mm Hg with no or low support (Norepi < 0.1 μg/kg/min)
  - Heart rate < 120 bpm
  - Lactate < 4 mmol/L
  - Heart rate > 40 bpm

#### Yellow Criteria
- **Respiratory:**
  - SpO2 ≥ 90%
  - FiO2 > 0.6
  - Respiratory rate > 30 breaths/min
  - PEEP > 10 cm H2O
- **Cardiovascular:**
  - MAP ≥ 65 mm Hg with moderate support (Norepi 0.1-0.3 μg/kg/min)
  - Heart rate 120-150 bpm
  - Shock with lactate > 4 mmol/L
  - Heart rate > 40 bpm

#### Red Criteria
- **Respiratory:**
  - SpO2 < 90%
- **Cardiovascular:**
  - MAP < 65 mm Hg despite support
  - MAP ≥ 65 mm Hg but on high support (Norepi > 0.3 μg/kg/min)
  - IV therapy for hypertensive emergency (SBP > 200 mm Hg or MAP > 110 mm Hg with specific medications)
  - Heart rate > 150 bpm or < 40 bpm

## Analysis Workflow

1. **Data Filtering:** The analysis is restricted to the first 72 hours of intubation and only considers data recorded during business hours (8am-5pm). This analysis is done using the CLIF-1.0 data format constructed using the COVID DataMart at University of Chicago. Time period under consideration is March 1, 2020 to March 31, 2023.

2. **Criteria Application:** Each encounter is evaluated against the Patel, TEAM, and Consensus Criteria (Green, Yellow, Red).

3. **Criteria Satisfaction:** For each encounter, the percentage of business hours where the criteria are met is calculated.

4. **Visualization:** Various visualizations are generated to explore the data, including:
   - Time series plots to show when criteria are met over time.
   - Histograms showing the distribution of encounters meeting each criterion.
   - Heatmaps to identify patterns in criteria satisfaction across encounters.

5. **Outcome Evaluation:** Encounters are assessed for eligibility for mobilization based on the criteria, and the results are summarized.




## Environment setup
```
python3 -m venv .mortality_model
source .mobilization/bin/activate
# Install Jupyter and IPykernel
pip install jupyter ipykernel
# Register the virtual environment as a kernel for Jupyter
python -m ipykernel install --user --name=.mobilization --display-name="Python (mobilization)"
```