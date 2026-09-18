VitaBand – Wearable Health and Safety Monitoring System



1\. Project Overview



VitaBand is a wearable health and safety monitoring project that I developed as part of my R\&D and software-based proof-of-concept work.



The project focuses on monitoring health-related parameters such as heart rate, SpO2, temperature and ECG, along with motion and fall-related information.



At the current stage, I am using real physiological and motion datasets with Python to study sensor outputs, develop processing methods and validate the proposed monitoring logic.



The final system is planned as a wearable device with multiple sensors, real-time processing, data logging and a user dashboard or mobile application.







2\. Project Objectives



The main objectives of my VitaBand project are:



\- Study existing wearable health-monitoring products.

\- Research suitable sensors for health and motion monitoring.

\- Process real physiological and motion datasets.

\- Develop a software-based health monitoring system.

\- Study ECG and PPG signal processing.

\- Develop and validate a basic fall-detection approach.

\- Test missing-data, sensor-failure and motion-artifact conditions.

\- Design the proposed MVP architecture.

\- Prepare a plan for future hardware implementation.





3\. Proposed Sensors and Components



Component  Purpose

MAX30102   Heart Rate and SpO2

MAX30205   Body Temperature

MAX30003   ECG

LSM6DSOX   3-axis Accelerometer and Gyroscope



I selected these components based on their suitability for wearable health and motion-monitoring applications.



The current project stage is software and dataset based. Physical sensor integration is planned as part of my future hardware implementation.





4\. System Architecture



The proposed VitaBand system follows this processing flow:



Sensor Layer

&#x20;    ↓

Data Acquisition

&#x20;    ↓

Pre-processing

&#x20;    ↓

Feature Extraction

&#x20;    ↓

Health and Motion Analysis

&#x20;    ↓

Decision Logic

&#x20;    ↓

Data Logging

&#x20;    ↓

Dashboard / Mobile Application



The proposed sensor layer contains:



\- MAX30102 – HR and SpO2

\- MAX30205 – Body Temperature

\- MAX30003 – ECG

\- LSM6DSOX – Accelerometer and Gyroscope







5\. Software Technologies



I used Python for the current R\&D and validation work.



The main technologies used are:



\- Python

\- Pandas

\- NumPy

\- CSV-based physiological datasets



I used Pandas for loading and handling sensor data, while NumPy was used for numerical calculations and signal processing.







6\. Real Dataset Processing



I used the Pulse Transit Time PPG Dataset v1.1.0 from PhysioNet for real-data processing and validation.



Dataset:



https://physionet.org/content/pulse-transit-time-ppg/1.1.0/



The selected recording contains:



\- 242,815 samples

\- ECG data

\- PPG data

\- Accelerometer data

\- Gyroscope data

\- Sensor-temperature data

\- R-peak annotations



I used the real recorded physiological and motion signals to test the software processing approach.



The complete dataset is not included in this repository because of its large size.



To reproduce the experiments, the required dataset files have to be downloaded separately and placed in the project folder.







7\. ECG Processing



I processed the real ECG recording using the R-peak annotations provided with the dataset.



The test produced:



\- Total ECG samples: 242,815

\- Detected R-peaks: 829

\- Average RR interval: 0.586 seconds

\- Calculated reference heart rate: 102.38 BPM



The current implementation uses the dataset-provided R-peak annotations. Therefore, this demonstrates processing of real ECG data and does not represent an independently developed clinical ECG peak-detection algorithm.







8\. PPG and SpO2 Processing



I processed real Red and Infrared PPG signals using:



\- Red PPG: "pleth\_1"

\- Infrared PPG: "pleth\_2"



I divided the signals into 10-second windows and calculated the ratio-of-ratios.



Validation results:



\- Total PPG samples: 242,815

\- Total windows: 48

\- Valid windows: 48

\- Rejected windows: 0

\- Average R value: 0.6459

\- Minimum R value: 0.5425

\- Maximum R value: 0.9978



The dataset provides reference SpO2 measurements of:



\- Start: 96%

\- End: 97%



These reference SpO2 values are start/end measurements and are not continuous calculated ground-truth values for every PPG window.







9\. Motion Processing



I processed the real accelerometer and gyroscope data to calculate motion magnitudes.



Results:



Accelerometer



\- Minimum magnitude: 0.08

\- Maximum magnitude: 25.52

\- Average magnitude: 9.68



Gyroscope



\- Minimum magnitude: 0.02

\- Maximum magnitude: 5.37

\- Average magnitude: 1.14



These results demonstrate that I can load and process real motion data using the VitaBand software.







10\. Fall Detection



I developed a basic fall-detection approach using accelerometer and gyroscope data.



The current approach considers:



1\. High acceleration

2\. Significant gyroscope activity

3\. Post-event low movement/inactivity



I selected the current thresholds as engineering thresholds for the dataset-based validation. They are not clinical standards.



I also used a public fall-detection dataset to test the approach with both fall and normal-activity data.



The validation demonstrated that the selected test cases could be classified using the current algorithm.







11\. Simulation Validation



I performed controlled simulation tests to check how the system handles abnormal and faulty conditions.



The following cases were tested:



Missing Data



I intentionally replaced 10 ECG samples with missing values.



Result:



Missing data detected – PASS



Sensor Failure



I intentionally removed the Red and Infrared PPG values.



Result:



PPG sensor failure detected – PASS



Motion Artifact



I modified the acceleration signal to introduce an artificial motion artifact.



\- Original acceleration maximum: 25.52

\- Simulated artifact peak: 51.04



Result:



Motion artifact detected – PASS



Abnormal Condition



I used the following values for a controlled abnormal-condition test:



\- Heart Rate: 145 BPM

\- Temperature: 39.2 °C

\- SpO2: 91%



Result:



Abnormal condition detected – PASS



\---



12\. Health Monitoring Logic



The proposed health monitoring process is:



Real Sensor / Dataset Data

&#x20;         ↓

&#x20;    Data Validation

&#x20;         ↓

&#x20;    Pre-processing

&#x20;         ↓

&#x20;  Feature Extraction

&#x20;         ↓

&#x20;Health Parameter Extraction

&#x20;         ↓

&#x20;  Health Condition

&#x20;      Evaluation

&#x20;         ↓

&#x20;    Decision Logic

&#x20;         ↓

&#x20;Normal / Attention Required /

&#x20;Sensor or Data Error

&#x20;         ↓

&#x20;     Data Logging

&#x20;         ↓

&#x20;Dashboard / Alert



For motion and fall detection, I use a separate processing path based on accelerometer and gyroscope data.





13\. Current Project Status



I have completed the main R\&D and software-based validation activities for the current VitaBand stage.



The completed areas include:



\- Existing product study

\- Sensor research

\- Sensor comparison and selection

\- Communication research

\- System architecture

\- Data flow

\- ECG research and processing

\- PPG processing

\- Temperature sensor-data analysis

\- Fall detection research and validation

\- Health monitoring logic

\- Simulation validation

\- Technology evaluation

\- Risks and limitations

\- Proposed MVP architecture

\- Future hardware implementation plan



The current status can be summarized as:



R\&D and software-based proof-of-concept validation completed.



The physical wearable MVP and complete hardware integration are planned as future work.







14\. Limitations



The current system is at the R\&D and software validation stage.



The main limitations are:



\- Complete hardware integration has not yet been carried out.

\- The fall-detection thresholds are dataset-specific engineering thresholds.

\- ECG heart-rate calculation currently uses provided R-peak annotations.

\- Continuous ground-truth SpO2 values are not available for every PPG window.

\- Dataset temperature channels are sensor-temperature measurements and are not treated as continuous body-temperature ground truth.

\- Real-world wearable testing is still required.

\- Sensor calibration, placement, power consumption and communication reliability need to be evaluated during hardware integration.



VitaBand is currently an engineering R\&D project and is not intended to provide medical diagnosis.







15\. Future Hardware Implementation



My planned hardware implementation includes:



1\. Selection of a suitable low-power MCU.

2\. Integration of MAX30102, MAX30205, MAX30003 and LSM6DSOX.

3\. Sensor communication and synchronization.

4\. Real-time signal acquisition.

5\. Embedded signal processing.

6\. Health and fall decision logic.

7\. Data logging and wireless communication.

8\. Dashboard or mobile application.

9\. Hardware validation and sensor calibration.

10\. PCB, enclosure and wearable prototype development.



I may consider AI/ML techniques in future work for advanced anomaly detection, fall classification and personalized health analysis.







16\. Project Structure



The repository contains the Python scripts that I developed and used during the R\&D and validation stages.



Important files include:



\- "main.py" – basic VitaBand health-monitoring program

\- "ecg\_simulation.py" – ECG-related simulation

\- "fall\_detection.py" – fall-detection logic

\- "ppg\_spo2\_test.py" – PPG and SpO2 processing

\- "real\_ecg\_tests.py" – real ECG data processing

\- "real\_motion\_tests.py" – real motion-data processing

\- "real\_fall\_detection.py" – real fall-detection processing

\- "real\_fall\_test.py" – fall-data testing

\- "temperature\_tests.py" – temperature-data analysis

\- "simulation\_validation.py" – controlled simulation validation

\- "vitaband\_simulation.py" – VitaBand simulation

\- "vitaband\_simulation\_validated.py" – validated simulation

\- "check\_csv.py" – CSV/data checking



The repository also contains additional experimental scripts that I developed during the R\&D process.







17\. Dataset Files



I intentionally excluded large datasets from the GitHub repository using ".gitignore".



The repository does not contain the complete PhysioNet dataset or the large extracted fall-detection dataset.



To reproduce the experiments:



1\. Download the required public dataset.

2\. Place the required CSV files in the project directory.

3\. Run the corresponding Python script.

4\. Check the generated output against the documented validation results.







18\. Disclaimer



VitaBand is an academic and engineering R\&D project.



The results presented in this repository demonstrate software processing and dataset-based validation. They should not be considered medical diagnosis or clinical validation.



Further hardware testing, calibration, real-world validation and appropriate regulatory evaluation would be required before use in a medical or clinical application.







19\. References



PhysioNet



Pulse Transit Time PPG Dataset v1.1.0



https://physionet.org/content/pulse-transit-time-ppg/1.1.0/



Sensor References

