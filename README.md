# Embedded Log Analyzer
This is one of my recent projects where I focussed on building a structured approach to log monitoring and system diagnostics.
This is a Python-based tool to analyze embedded system log files and detect warnings and errors automatically.

# Problem Statement
Embedded Systems generate large volumes of logs during execution. Manually analyzing these logs are time consuming and error prone.
This tool automates:
1) Log parsing
2) Error/Warning detection
3) System health evaluation

## Features
- Reads log files
- Counts INFO, WARN, and ERROR messages
- Generates PASS/FAIL status

## Folder Structure
- `logs/` -> sample input logs
- `src/` -> source code
- `reports/` -> future generated reports
- `tests/` -> unit tests

## Run
```bash
python src/log_analyzer.py logs/device_log.txt

## Output

The tool prints the report in the terminal and also saves it to:

```text
reports/analysis_report.txt

## Advanced Features
- Detects critical embedded/system keywords:
  - `timeout`
  - `failure`
  - `invalid`
  - `disconnect`
  - `overload`
- Saves analysis output to `reports/analysis_report.txt`
- Creates a summary report and saves it to `reports/summary_report.csv`

## Testing

This project uses `pytest` for unit testing.

Run all tests with:

```bash
pytest

## Multi-File Analysis

You can analyze multiple log files in one command:

```bash
python src/log_analyzer.py logs/device_log.txt logs/device_log_2.txt
```

## Learning outcomes
-log-based debugging
-anomaly detection
-PASS/FAIL evaluation
-system health analysis

## Future Improvements
-Real-time log monitoring
-Advanced log parsing (Regex / structured logs)
-Visualization dashboard
-CI/CD integration