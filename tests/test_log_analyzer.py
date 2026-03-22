from pathlib import Path
import tempfile

from src.log_analyzer import analyze_log_file, format_report


def create_temp_log(content: str) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", suffix=".txt")
    temp_file.write(content)
    temp_file.close()
    return temp_file.name


def test_analyze_log_file_counts_levels_correctly():
    log_content = """[INFO] Boot successful
[WARN] Low battery detected
[ERROR] UART communication failure
[INFO] Retry started
"""

    temp_log_path = create_temp_log(log_content)
    result = analyze_log_file(temp_log_path)

    assert result["info_count"] == 2
    assert result["warn_count"] == 1
    assert result["error_count"] == 1
    assert result["system_status"] == "FAIL"


def test_analyze_log_file_detects_keywords():
    log_content = """[INFO] Boot successful
[WARN] Invalid reading detected
[ERROR] Sensor timeout
[ERROR] Network disconnect occurred
"""

    temp_log_path = create_temp_log(log_content)
    result = analyze_log_file(temp_log_path)

    assert result["keyword_hits"]["timeout"] == 1
    assert result["keyword_hits"]["invalid"] == 1
    assert result["keyword_hits"]["disconnect"] == 1
    assert result["total_keyword_hits"] == 3
    assert result["system_status"] == "FAIL"


def test_analyze_log_file_pass_when_no_errors_or_keywords():
    log_content = """[INFO] Boot successful
[INFO] Sensor initialized
[WARN] Temperature slightly high
"""

    temp_log_path = create_temp_log(log_content)
    result = analyze_log_file(temp_log_path)

    assert result["info_count"] == 2
    assert result["warn_count"] == 1
    assert result["error_count"] == 0
    assert result["total_keyword_hits"] == 0
    assert result["system_status"] == "PASS"


def test_format_report_contains_expected_sections():
    sample_result = {
        "file_name": "test_log.txt",
        "info_count": 2,
        "warn_count": 1,
        "error_count": 1,
        "keyword_hits": {
            "timeout": 1,
            "failure": 0,
            "invalid": 0,
            "disconnect": 0,
            "overload": 0,
        },
        "total_keyword_hits": 1,
        "system_status": "FAIL",
    }

    report = format_report(sample_result)

    assert "Log Analysis Report" in report
    assert "INFO count" in report
    assert "Critical Keyword Hits" in report
    assert "System Status" in report


def test_analyze_log_file_raises_file_not_found():
    fakepath = "logs/this_file_does_not_exist.txt"

    try:
        analyze_log_file(fakepath)
        assert False, "Expected FileNotFoundError to be raised"
    except FileNotFoundError:
        assert True

import csv
from src.log_analyzer import save_summary_csv


def test_save_summary_csv_creates_file(tmp_path):
    results = [
        {
            "file_name": "log1.txt",
            "info_count": 2,
            "warn_count": 1,
            "error_count": 0,
            "total_keyword_hits": 0,
            "system_status": "PASS",
            "keyword_hits": {
                "timeout": 0,
                "failure": 0,
                "invalid": 0,
                "disconnect": 0,
                "overload": 0,
            },
        },
        {
            "file_name": "log2.txt",
            "info_count": 1,
            "warn_count": 1,
            "error_count": 1,
            "total_keyword_hits": 2,
            "system_status": "FAIL",
            "keyword_hits": {
                "timeout": 1,
                "failure": 1,
                "invalid": 0,
                "disconnect": 0,
                "overload": 0,
            },
        },
    ]

    output_file = tmp_path / "summary_report.csv"
    save_summary_csv(results, str(output_file))

    assert output_file.exists()

    with output_file.open("r", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    assert rows[0][0] == "file_name"
    assert rows[1][0] == "log1.txt"
    assert rows[2][0] == "log2.txt"