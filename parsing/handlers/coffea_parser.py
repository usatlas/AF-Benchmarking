import datetime as dt


def parse_coffea_log(path):
    """Parse Coffea analysis log file for timing information.

    Args:
        path: Path to coffea_hist.log file

    Returns:
        dict: Parsed timing data with keys:
            - submitTime: UTC timestamp in milliseconds
            - queueTime: Queue time in seconds (always 0)
            - runTime: Execution time in seconds
            - frequency: Processing frequency in kHz
            - status: Exit status (0 = success)
    """
    print(f"[Coffea NTuple->Hist] Parsing {path.name}")

    with open(path) as f:
        file_lines = f.readlines()

    # Parse execution time and frequency from line 2
    # Format: "... execution time: 205.45 s ( 89.10 kHz)"
    line_list = file_lines[1].split(" ")
    run_time = round(float(line_list[3]))
    frequency = round(float(line_list[-2]))

    # Parse UTC timestamps from end of file
    # Format: "start_time_utc=2025-12-17T00:48:07.953454Z"
    start_time_line = None
    end_time_line = None

    for line in file_lines:
        if line.startswith("start_time_utc="):
            start_time_line = line.strip()
        elif line.startswith("end_time_utc="):
            end_time_line = line.strip()

    if not start_time_line:
        raise ValueError("No start_time_utc found in log file")

    # Extract timestamp string after the = sign
    start_time_str = start_time_line.split("=")[1]

    # Parse ISO 8601 format with Z suffix (UTC)
    # Format: 2025-12-17T00:48:07.953454Z
    start_dt = dt.datetime.fromisoformat(start_time_str.rstrip("Z")).replace(tzinfo=dt.timezone.utc)
    utc_timestamp = int(start_dt.timestamp() * 1000)

    status = 0

    dicti = {
        "submitTime": utc_timestamp,
        "queueTime": 0,
        "runTime": run_time,
        "frequency": frequency,
        "status": status,
    }

    return dicti


# Registers this parsing script with the Class
def register(parser):
    parser.register_parsers("coffea_hist.log", parse_coffea_log)
