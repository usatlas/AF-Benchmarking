from pathlib import Path
import datetime as dt
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


def parse_coffea_log(path):
    print(f"[Coffea NTuple->Hist] Parsing {path.name}")
    with open(path) as f:
        file_lines = f.readlines()
    line_list = file_lines[1].split(" ")

    run_time = round(float(line_list[3]))
    frequency = round(float(line_list[-2]))
    new_path = str(path).replace("coffea_hist.log", "split.log")
    new_path = Path(new_path)
    with open(new_path) as g:
        file_lines = g.readlines()
        start_datetime_list = file_lines[0].split(" ")
    year = int(start_datetime_list[-1])
    month = int(MONTH_DICT[start_datetime_list[1]])
    if len(start_datetime_list) == 6:
        day = int(start_datetime_list[2])
        start_time = start_datetime_list[3]
        start_time = dt.datetime.strptime(start_time, "%H:%M:%S").time()
    else:
        day = int(start_datetime_list[3])
        start_time = start_datetime_list[4]
        start_time = dt.datetime.strptime(start_time, "%H:%M:%S").time()
    start_date_object = dt.date(year, month, day)
    start_datetime_object = dt.datetime.combine(start_date_object, start_time)
    utc_timestamp = int(start_datetime_object.timestamp()) * 1000

    status = 0

    dicti = {
        "submitTime": utc_timestamp,
        "queueTime": 0,
        "runTime": run_time,
        "frequency": frequency,
        "status": status,
    }

    curr_dir = Path().absolute()
    output_path = curr_dir / "coffea_parsed.json"

    print(dicti)

    with open(output_path, "w") as outfile:
        json.dump(dicti, outfile, indent=4)


# Registers this parsing script with the Class
def register(parser):
    parser.register_parsers("coffea_hist.log", parse_coffea_log)
