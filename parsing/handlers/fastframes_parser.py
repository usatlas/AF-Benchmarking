import datetime as dt
import re


ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

date_format = "%Y-%m-%d %H:%M:%S"


def elapsed_to_seconds(s):
    s = s.rstrip("m")
    minutes, seconds = map(int, s.split(":"))
    return minutes * 60 + seconds


# Strips the text of its green color
def strip_ansi(text):
    return ANSI_ESCAPE.sub("", text)


def parse_fastframes_log(path):
    print(f"[FastFrames] Parsing {path.name}")
    with open(path) as f:
        file_lines = f.readlines()
        N = len(file_lines)
    cleaned_lines = [strip_ansi(lines) for lines in file_lines[N - 2 : N]]
    line1 = cleaned_lines[0].split(" ")  # processed/total events, elapsed time
    elapsed_time = line1[3]
    processed_events = int(line1[13])
    if processed_events == 18304905:
        status = 0
    else:
        status = 1

    line2 = cleaned_lines[1].split(" ")
    date = line2[13]
    time = line2[14]

    combined = f"{date} {time}"

    # It was submitted to the batch so it's in UTC TimeZone already
    dt_obj = dt.datetime.strptime(combined, "%d-%m-%Y %H:%M:%S")
    utc_timestamp = int(dt_obj.timestamp() * 1000)

    run_time = int(elapsed_to_seconds(elapsed_time))
    frequency = int((processed_events / run_time) / 1000)

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
    parser.register_parsers("fastframes.log", parse_fastframes_log)
