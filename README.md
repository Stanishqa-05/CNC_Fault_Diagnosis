# CNC Machine Fault Diagnosis Using Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-1.3+-purple.svg)](https://pandas.pydata.org)

## Overview
This project is a **Machine Learning-based fault diagnosis system** for a CNC machine. The system ingests raw sensor data, applies signal processing techniques to remove noise, extracts statistical features, and uses classification algorithms to identify the machine's operating condition. 

The objective is to accurately predict abnormal machine conditions (such as spindle issues or overloads) before they cause critical failures, enabling predictive maintenance.

## Data Processing Pipeline
The system follows a structured pipeline to convert raw sensor data into actionable predictions:

```text
Raw CNC Sensor Data
       ↓
Moving Average Filter (Noise Reduction)
       ↓
Normalization (Feature Scaling)
       ↓
Feature Extraction
       ↓
Feature Vector Creation [RMS, Energy, Std Dev, Mean]
       ↓
Machine Learning Model (SVM / Random Forest)
       ↓
Prediction & Performance Evaluation
```

### Step-by-Step Breakdown:
1. **Raw Data Collection:** Sensor data is collected from the CNC machine, containing noise and operational fluctuations.
2. **Moving Average Filter:** Smooths sudden fluctuations and removes random noise to make underlying patterns easier to analyze.
3. **Normalization:** Scales the data so features have comparable numerical ranges. This is critical for distance-based algorithms like SVM.
4. **Feature Extraction:** Extracts key statistical characteristics from the filtered signal:
   - **RMS** (Root Mean Square) - Indicates signal energy/power.
   - **Energy** - Captures the total signal strength.
   - **Standard Deviation** - Measures signal variability.
   - **Mean** - Represents the central tendency of the signal.
5. **Feature Vector Creation:** Combines the above features into a structured input vector: `[RMS, Energy, Standard Deviation, Mean]`.
6. **Target Label:** The dataset contains a target column named `Condition`, which represents the machine's operating state (e.g., Normal, Faulty).

## Machine Learning Models
Two classification algorithms are implemented and compared to determine the most effective model for this dataset:

*   **Support Vector Machine (SVM):** Used to separate different machine conditions based on the extracted feature vectors. Works well for high-dimensional spaces but requires normalized data.
*   **Random Forest:** An ensemble learning method that builds multiple decision trees. It is robust to overfitting and handles non-linear relationships well without heavy scaling requirements.

## Tech Stack
*   **Language:** Python
*   **Data Manipulation:** Pandas, NumPy
*   **Machine Learning:** Scikit-learn (SVM, Random Forest, StandardScaler, train_test_split)
*   **Data Visualization:** Matplotlib, Seaborn
*   **Environment:** Jupyter Notebook / Python Scripts

## Repository Structure
```text
├── data/                   # Raw and processed sensor datasets
├── notebooks/              # Jupyter notebooks for EDA, filtering, and model training
│   ├── 01_Data_Preprocessing.ipynb
│   ├── 02_Feature_Extraction.ipynb
│   └── 03_Model_Training.ipynb
├── src/                    # Python scripts for the production pipeline
│   ├── preprocess.py       # Moving average & normalization logic
│   ├── features.py         # Feature extraction (RMS, Energy, etc.)
│   └── train.py            # Model training and evaluation
├── requirements.txt        # Dependencies
└── README.md
```

##  How to Run This Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Stanishqa-05/CNC_Fault_Diagnosis.git
   cd CNC_Fault_Diagnosis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the preprocessing pipeline:**
   ```bash
   python src/preprocess.py
   ```

4. **Train and evaluate the models:**
   ```bash
   python src/train.py
   ```

## Model Evaluation & Results
*The system is evaluated using standard classification metrics such as Accuracy, Precision, Recall, and F1-Score.*

*(Add your actual results here once you have them! For example:)*
- **SVM Accuracy:** ~XX%
- **Random Forest Accuracy:** ~XX%
- **Best Performing Model:** [SVM / Random Forest]

## Future Improvements
- Deploy the trained model to an edge device (e.g., STM32) for real-time inference at the machine level.
- Integrate with an MQTT broker to send live fault alerts to a cloud dashboard (e.g., ThingsBoard).
- Expand the dataset to include more fault categories (e.g., tool wear, misalignment).

## Author
**Sheela Bangade**  
*Electronics & Telecommunication Engineering (2026)*  
[GitHub Profile](https://github.com/Stanishqa-05) | [Email](mailto:tsbangade0504@gmail.com)

---
*If you are a recruiter or fellow engineer, feel free to reach out to discuss the project or potential opportunities!*
