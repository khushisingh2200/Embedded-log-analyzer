# Architecture Overview
The Embedded Log Analyzer processes one or more log files and generates validation reports.

+----------------------+
|  Log Files           |
|  (device_log.txt)    |
+----------+-----------+
           |
           v
+----------------------+
|  Log Analyzer        |
|  (Python Script)     |
|                      |
|  - Count log levels  |
|  - Detect keywords   |
|  - Determine status  |
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
