import datetime as dt


def parse_eventloop_log(path):
    print(f"[EventLoop] Parsing {path.name}")

    with open(path) as f:
        lines = f.readlines()

    # EventLoop benchmark info
    block = lines[-8:]

    start_datetime = block[1].split("=", 1)[1].strip()
    run_time = int(float(block[3].split("=", 1)[1].strip()))
    frequency = int(float(block[-3].split("=", 1)[1].strip()))

    start_dt = dt.datetime.fromisoformat(start_datetime.rstrip("Z")).replace(
        tzinfo=dt.timezone.utc
    )
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
    parser.register_parsers("eventloop_arrays.log", parse_eventloop_log)
