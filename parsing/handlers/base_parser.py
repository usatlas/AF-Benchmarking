"""Base parser class for ATLAS benchmark logs.

This module provides common parsing logic shared across different
benchmark types (TRUTH3, EVNT, etc.).
"""

import datetime as dt


# Month abbreviation to number mapping
MONTH_DICT = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
}


def parse_atlas_log(path, log_name="ATLAS"):
    """Parse ATLAS benchmark log file for timing information.

    Args:
        path: Path to log file
        log_name: Name of benchmark for logging (e.g., "TRUTH3", "EVNT")

    Returns:
        dict: Parsed timing data with keys:
            - submitTime: UTC timestamp in milliseconds
            - queueTime: Queue time in seconds
            - runTime: Execution time in seconds
            - status: Exit status (0 = success)
    """
    print(f"[{log_name}] Parsing {path.name}")

    # Read log file
    with open(path) as f:
        file_lines = f.readlines()
        N = len(file_lines)

    # Parse start datetime from first line
    start_datetime_list = file_lines[0].split(" ")
    end_time_list = file_lines[N - 1].split(" ")

    start_time = start_datetime_list[0]
    month = int(MONTH_DICT[start_datetime_list[2]])
    year = int(start_datetime_list[-1])

    # Handle different date formats (with/without day of week)
    if len(start_datetime_list) == 8:
        day = int(start_datetime_list[4])
        submit_time = dt.datetime.strptime(start_datetime_list[5], "%H:%M:%S").time()
    else:
        day = int(start_datetime_list[3])
        submit_time = dt.datetime.strptime(start_datetime_list[4], "%H:%M:%S").time()

    # Build datetime objects
    start_date_object = dt.date(year, month, day)
    start_time = dt.datetime.strptime(start_datetime_list[0], "%H:%M:%S").time()
    start_datetime_object = dt.datetime.combine(start_date_object, start_time)
    utc_timestamp = int(start_datetime_object.timestamp()) * 1000

    # Calculate queue time
    submit_datetime_object = dt.datetime.combine(start_datetime_object, submit_time)
    queue_time = int((start_datetime_object - submit_datetime_object).total_seconds())

    # Calculate run time
    end_time = dt.datetime.strptime(end_time_list[0], "%H:%M:%S").time()
    end_datetime_object = dt.datetime.combine(start_date_object, end_time)
    run_time = int((end_datetime_object - start_datetime_object).total_seconds())

    status = 0

    return {
        "submitTime": utc_timestamp,
        "queueTime": queue_time,
        "runTime": run_time,
        "status": status,
    }
