from pathlib import Path
import sys
import csv


CRITICAL_KEYWORDS = ["timeout", "failure", "invalid", "disconnect", "overload"]


def analyze_log_file(file_path: str) -> dict:
    """
    Analyze an embedded log file and count INFO, WARN, ERROR,
    and critical keyword occurrences.
    """
    info_count = 0
    warn_count = 0
    error_count = 0
    keyword_hits = {keyword: 0 for keyword in CRITICAL_KEYWORDS}

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line_lower = line.lower()

            if "[INFO]" in line:
                info_count += 1
            elif "[WARN]" in line:
                warn_count += 1
            elif "[ERROR]" in line:
                error_count += 1

            for keyword in CRITICAL_KEYWORDS:
                if keyword in line_lower:
                    keyword_hits[keyword] += 1

    total_keyword_hits = sum(keyword_hits.values())
    system_status = "FAIL" if error_count > 0 or total_keyword_hits > 0 else "PASS"

    return {
        "file_name": path.name,
        "info_count": info_count,
        "warn_count": warn_count,
        "error_count": error_count,
        "keyword_hits": keyword_hits,
        "total_keyword_hits": total_keyword_hits,
        "system_status": system_status,
    }


def format_report(result: dict) -> str:
    """
    Create a formatted log analysis report as a string.
    """
    keyword_section = "\n".join(
        [f"{keyword:<12}: {count}" for keyword, count in result["keyword_hits"].items()]
    )

    return (
        f"Log Analysis Report: {result['file_name']}\n"
        "------------------------------\n"
        f"INFO count         : {result['info_count']}\n"
        f"WARN count         : {result['warn_count']}\n"
        f"ERROR count        : {result['error_count']}\n"
        f"Keyword hits total : {result['total_keyword_hits']}\n"
        "\n"
        "Critical Keyword Hits\n"
        "---------------------\n"
        f"{keyword_section}\n"
        "\n"
        f"System Status      : {result['system_status']}\n"
    )


def print_report(report_text: str) -> None:
    """
    Print the report to the terminal.
    """
    print(report_text)


def save_report(report_text: str, output_path: str) -> None:
    """
    Save the report to a text file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        file.write(report_text)


def save_summary_csv(results: list[dict], output_path: str) -> None:
    """
    Save summary results for multiple log files into a CSV file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "file_name",
            "info_count",
            "warn_count",
            "error_count",
            "total_keyword_hits",
            "system_status",
            "timeout",
            "failure",
            "invalid",
            "disconnect",
            "overload",
        ])

        for result in results:
            writer.writerow([
                result["file_name"],
                result["info_count"],
                result["warn_count"],
                result["error_count"],
                result["total_keyword_hits"],
                result["system_status"],
                result["keyword_hits"]["timeout"],
                result["keyword_hits"]["failure"],
                result["keyword_hits"]["invalid"],
                result["keyword_hits"]["disconnect"],
                result["keyword_hits"]["overload"],
            ])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/log_analyzer.py <log_file_path_1> [<log_file_path_2> ...]")
        sys.exit(1)

    log_files = sys.argv[1:]
    all_results = []
    combined_report_text = ""

    for log_file in log_files:
        try:
            result = analyze_log_file(log_file)
            all_results.append(result)

            report = format_report(result)
            print_report(report)
            print("=" * 50)

            combined_report_text += report + "\n" + ("=" * 50) + "\n\n"

        except FileNotFoundError as error:
            print(error)

    if all_results:
        save_report(combined_report_text, "reports/analysis_report.txt")
        save_summary_csv(all_results, "reports/summary_report.csv")
        print("Combined text report saved to: reports/analysis_report.txt")
        print("CSV summary report saved to   : reports/summary_report.csv")
    else:
        print("No valid log files were analyzed.")
        sys.exit(1)