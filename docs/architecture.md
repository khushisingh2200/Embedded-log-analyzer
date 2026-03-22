# Architecture Overview
The Embedded Log Analyzer processes one or more log files and generates validation reports.
The entire architecture overview of this project is as follows:

+----------------------+
|  Log Files           |
|  (device_log.txt)    |
|  (device_log_2.txt)  |
+----------+-----------+
           |
           v
+----------------------+
|  Log Analyzer        |
|  (Python Script)     |
|                      |
|  - Count log levels  |
|  - Detect keywords   |
|  - Determines status |
+----------+-----------+
           |
           v
+----------------------+
|  Output Reports      |
|                      |
|  Terminal Output     |
|  analysis_report.txt |
|  summary_report.csv  |
+----------------------+
