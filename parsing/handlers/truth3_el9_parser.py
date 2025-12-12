import datetime as dt
from pathlib import Path
import json


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


def parse_truth3_el9_log(path):
    print(f"[TRUTH3 EL9] Parsing {path.name}")
    with open(path) as f:
        file_lines = f.readlines()
        N = len(file_lines)
    start_datetime_list = file_lines[0].split(" ")
    end_time_list = file_lines[N - 1].split(" ")

    start_time = start_datetime_list[0]
    month = int(MONTH_DICT[start_datetime_list[2]])
    year = int(start_datetime_list[-1])
    if len(start_datetime_list) == 8:
        day = int(start_datetime_list[4])
        submit_time = dt.datetime.strptime(start_datetime_list[5], "%H:%M:%S").time()
    else:
        day = int(start_datetime_list[3])
        submit_time = dt.datetime.strptime(start_datetime_list[4], "%H:%M:%S").time()

    start_date_object = dt.date(year, month, day)
    start_time = dt.datetime.strptime(start_datetime_list[0], "%H:%M:%S").time()
    start_datetime_object = dt.datetime.combine(start_date_object, start_time)
    utc_timestamp = int(start_datetime_object.timestamp()) * 1000

    submit_datetime_object = dt.datetime.combine(start_datetime_object, submit_time)
    queue_time = int((start_datetime_object - submit_datetime_object).total_seconds())
    end_time = dt.datetime.strptime(end_time_list[0], "%H:%M:%S").time()
    end_datetime_object = dt.datetime.combine(start_date_object, end_time)
    run_time = int((end_datetime_object - start_datetime_object).total_seconds())
    status = 0
    payload = 0

    dicti = {
        "submitTime": utc_timestamp,
        "queueTime": queue_time,
        "runTime": run_time,
        "payloadSize": payload,
        "status": status,
    }

    curr_dir = Path().absolute()
    output_path = curr_dir / "truth3_el9_parsed.json"

    print(dicti)

    with open(output_path, "w") as outfile:
        json.dump(dicti, outfile, indent=4)


# Registers this parsing script with the Class
def register(parser):
    parser.register_parsers("log.Derivation", parse_truth3_el9_log)
