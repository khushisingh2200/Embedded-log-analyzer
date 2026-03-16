# Embedded Log Analyzer

A Python-based tool to analyze embedded system log files and detect warnings and errors automatically.

## Features
- Reads log files
- Counts INFO, WARN, and ERROR messages
- Generates PASS/FAIL status

## Folder Structure
- `logs/` → sample input logs
- `src/` → source code
- `reports/` → future generated reports

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

## Testing

This project uses `pytest` for unit testing.

Run all tests with:

```bash
pytest

## Multi-File Analysis

You can analyze multiple log files in one command:

```bash
python src/log_analyzer.py logs/device_log.txt logs/device_log_2.txt