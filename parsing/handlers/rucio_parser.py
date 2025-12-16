from collections import deque
import re
import datetime as dt

from rich.console import Console

ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

date_format = "%Y-%m-%d %H:%M:%S"

console = Console()


# Strips the text of its green color
def strip_ansi(text):
    return ANSI_ESCAPE.sub("", text)


def parse_rucio_log(path):
    console.print(f"[bold yellow][Rucio][/bold yellow] Parsing {path.name}")

    first_line = None
    last_lines = deque(maxlen=12)

    with open(path) as f:
        for line in f:
            if "Processing 1 item(s) for input" in line and first_line is None:
                first_line = line
            last_lines.append(line)

    payload_line = last_lines[-1]
    last_line = last_lines[0] if len(last_lines) == 12 else None

    first_line = strip_ansi(first_line).split(" ")
    start_date_string = first_line[0]
    start_time_string = first_line[1].split(",")[0]

    last_line = strip_ansi(last_line).split(" ")
    end_date_string = last_line[0]
    end_time_string = last_line[1].split(",")[0]

    # Obtaining the payload for status check; casted as int
    payload = int(payload_line.split("\t")[0])
    if payload != 0:
        status = 0
    else:
        status = 1

    # Creating start and end time objects
    start_datetime_string = start_date_string + " " + start_time_string
    start_dt = dt.datetime.strptime(start_datetime_string, date_format)
    end_datetime_string = end_date_string + " " + end_time_string
    end_dt = dt.datetime.strptime(end_datetime_string, date_format)

    # Obtains timestamp and run_time
    start_dt_utc = start_dt.astimezone(dt.timezone.utc)
    utc_timestamp = int(start_dt_utc.timestamp()) * 1000
    run_time = int((end_dt - start_dt).total_seconds())

    dicti = {
        "submitTime": utc_timestamp,
        "queueTime": 0,
        "runTime": run_time,
        "status": status,
    }

    return dicti


# Registers this parsing script with the Class
def register(parser):
    parser.register_parsers("rucio.log", parse_rucio_log)
