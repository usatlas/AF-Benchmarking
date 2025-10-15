from paths import Paths_Class
import datetime as dt
from datetime import timezone
from typing import ClassVar


class Parsing_Class(Paths_Class):
    # Shared qualities among all objects created with this class

    # Dictionary used to obtain AF script is running at
    af_dictionary: ClassVar[dict] = {"uc": "UC-AF", "slack": "SLAC-AF", "bnl": "BNL-AF"}

    # Dictionary used to obtain job string recognized by ElasticSearch
    job_dictionary: ClassVar[dict] = {
        "Rucio": "Rucio Download",
        "TRUTH3": "truth3-batch",
        "EVNT": "EVNT-batch",
        "Coffea_Hist": "ntuple-hist-coffea",
        "TRUTH3_centos": "truth3-centos-container-batch",
        "TRUTH3_el9_container": "truth3-el9-container-batch",
        "TRUTH3_centos_interactive": "truth3-centos-container-interactive",
        "TRUTH3_interactive": "truth3-interactive",
        "EVNT_contained_el9": "EVNT-el9-container-batch",
        "EVNT_contained_centos7": "EVNT-centos7-container-batch",
        "TRUTH3_el9_container_interactive": "truth3-el9-container-interactive",
    }

    # Dictionary keys used to create dictionaries with none values
    dic_keys: ClassVar[list] = [
        "cluster",
        "testType",
        "submitTime",
        "queueTime",
        "runTime",
        "payloadSize",
        "status",
        "host",
    ]

    # Dictionary storing the directory where the script directories are located at sites
    ## UPDATE: Need to include SLAC and BNL ##
    benchmarks_dir_dic: ClassVar[dict] = {
        "uc": "/data/selbor/parsing_jobs",
        "slack": None,
        "bnl": None,
    }

    # Dictionary that contains months mapped to numbers; used when parsing EVNT and TRUTH3 log files
    months_dic: ClassVar[dict] = {
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

    # Constructor
    def __init__(self, site_dir, job_name, log_name, site):
        super().__init__(site_dir, job_name, log_name, site)
        # Name of the split log file
        self.split = "split.log"
        # Name of the piped output
        self.piped = "pipe_file.log"

    # Function that makes the dictionaries
    def dictionary_maker(
        self,
        start_date_time_timestamp,
        queue_time,
        run_time,
        payload_size,
        exit_code,
        host_name,
    ):
        # Creates a dictionary with predetermined keys
        dic = dict.fromkeys(self.dic_keys)
        # Assigns values to the keys
        dic[self.dic_keys[0]] = self.af_dictionary[self.site]
        dic[self.dic_keys[1]] = self.job_dictionary[self.job_name]
        dic[self.dic_keys[2]] = start_date_time_timestamp
        dic[self.dic_keys[3]] = queue_time
        dic[self.dic_keys[4]] = run_time
        dic[self.dic_keys[5]] = payload_size
        dic[self.dic_keys[6]] = exit_code
        dic[self.dic_keys[7]] = host_name
        return dic

    # Function that checks the split log file
    def checks_for_split_logs(self, l):
        split_log = l.replace(self.log_name, self.split)
        with open(split_log) as g:
            lines = g.read().splitlines()
            n = len(lines)
            if n == 3:
                start_time = lines[0]
                end_time = lines[1]
                host_name = lines[2]
                payload_size = 0
            elif n == 4:
                start_time = lines[0]
                end_time = lines[1]
                host_name = lines[2]
                payload_size = lines[3]
        return (start_time, end_time, host_name, payload_size)

    # Uses information from the split log files and the date time string
    def string_and_split(self, l):
        split_lines = self.checks_for_split_logs(l)
        dateTimeString = log_path.split("/")[4]
        year = int(dateTimeString[0:4])
        month = int(dateTimeString[5:7])
        day = int(dateTimeString[8:10])
        start_time_object = dt.datetime.strptime(split_lines[0], "%H:%M:%S")
        start_date_object = dt.datetime(year, month, day)

        start_date_time = dt.datetime.combine(
            start_date_object.date(), start_time_object.time()
        )
        start_date_time_timestamp = int(
            start_date_time.replace(tzinfo=timezone.utc).timestamp() * 1e3
        )
        end_time_object = dt.datetime.strptime(split_lines[1], "%H:%M:%S")
        end_date_object = dt.datetime(year, month, day)

        end_date_time = dt.datetime.combine(
            end_date_object.date(), end_time_object.time()
        )
        run_time = int((end_date_time - start_date_time).total_seconds())
        exit_code = 1
        queue_time = 0
        host_name = split_lines[-2]
        if split_lines[-1] == 0:
            payload_size = int(split_lines[-1])
        elif "DAOD_TRUTH3.TRUTH3.root" in split_lines[-1]:
            payload_size = int(split_lines[-1].split("\t")[0])
        dic = self.dictionary_maker(
            start_date_time_timestamp,
            queue_time,
            run_time,
            payload_size,
            exit_code,
            host_name,
        )
        return dic

    # Rucio parsing function
    # sti and eti are default cases, can be shifted if there are errors
    def parsing_rucio(self, log_path, sti=0, eti=12, psi=1):
        with open(log_path) as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                # Job is set to fail if the log file isn't the required length
                if N == 113:
                    exit_code = 0
                else:
                    exit_code = 1

                # Obtains host name
                host_name = file_lines[N - 2]

                # Obtains the payload size; splits the line at "\t" and grabs first element
                try:
                    payload_size = int((file_lines[N - psi]).split("\t")[0])
                except ValueError:
                    payload_size = 0
                    host_name = file_lines[N - 1]
                # Grabs the start and end date-time lines; splits them at various characters and grabs first element
                try:
                    start_time_line = (
                        file_lines[sti].split("\x1b[32;1m")[1].split(",")[0]
                    )
                except IndexError:
                    sti = 2
                    eti = 14
                    start_time_line = (
                        file_lines[sti].split("\x1b[32;1m")[1].split(",")[0]
                    )
                try:
                    end_time_line = (
                        file_lines[N - eti].split("\x1b[32;1m")[1].split(",")[0]
                    )
                    # Creates the date_time objects
                    start_date_time = dt.datetime(
                        int(start_time_line.split(" ")[0][0:4]),
                        int(start_time_line.split(" ")[0][5:7]),
                        int(start_time_line.split(" ")[0][8:10]),
                        int(start_time_line.split(" ")[1][0:2]),
                        int(start_time_line.split(" ")[1][3:5]),
                        int(start_time_line.split(" ")[1][6:8]),
                    )
                    end_date_time = dt.datetime(
                        int(end_time_line.split(" ")[0][0:4]),
                        int(end_time_line.split(" ")[0][5:7]),
                        int(end_time_line.split(" ")[0][8:10]),
                        int(end_time_line.split(" ")[1][0:2]),
                        int(end_time_line.split(" ")[1][3:5]),
                        int(end_time_line.split(" ")[1][6:8]),
                    )

                    # Obtains time delta and casts it as an int, run time
                    run_time = int((end_date_time - start_date_time).total_seconds())

                    # Interactive job has no queue time
                    queue_time = 0

                    # Gets the time stamp and multiplies it by 1000
                    start_date_time_timestamp = int(
                        start_date_time.replace(tzinfo=timezone.utc).timestamp() * 1e3
                    )

                    # Creates a dictionary with predetermined keys
                    dic = dict.fromkeys(self.dic_keys)

                    # Assigns values to the keys
                    dic[self.dic_keys[0]] = self.af_dictionary[self.site]
                    dic[self.dic_keys[1]] = self.job_dictionary[self.job_name]
                    dic[self.dic_keys[2]] = start_date_time_timestamp
                    dic[self.dic_keys[3]] = queue_time
                    dic[self.dic_keys[4]] = run_time
                    dic[self.dic_keys[5]] = payload_size
                    dic[self.dic_keys[6]] = exit_code
                    dic[self.dic_keys[7]] = host_name
                except IndexError:
                    queue_time = 0
                    run_time = 0
                    payload_size = 0
                    exit_code = 1
                    date_time_string = log_path.split("/")[4]
                    year = int(date_time_string[0:4])
                    month = int(date_time_string[5:7])
                    day = int(date_time_string[8:10])
                    hour = int(date_time_string[11:13])
                    start_date_object = dt.datetime(year, month, day, hour, 0, 0)
                    # Gets the time stamp and multiplies it by 1000
                    start_date_time_timestamp = int(
                        start_date_object.replace(tzinfo=timezone.utc).timestamp() * 1e3
                    )
                    # Creates a dictionary with predetermined keys
                    dic = dict.fromkeys(self.dic_keys)

                    # Assigns values to the keys
                    dic[self.dic_keys[0]] = self.af_dictionary[self.site]
                    dic[self.dic_keys[1]] = self.job_dictionary[self.job_name]
                    dic[self.dic_keys[2]] = start_date_time_timestamp
                    dic[self.dic_keys[3]] = queue_time
                    dic[self.dic_keys[4]] = run_time
                    dic[self.dic_keys[5]] = payload_size
                    dic[self.dic_keys[6]] = exit_code
                    dic[self.dic_keys[7]] = host_name

            else:
                print("ERROR -- FILE WAS NOT OPENED")
        return dic

    # Function that parses EVNT job files
    def parsing_evnt(self, log_path, os_used="native"):
        with open(log_path) as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                first_line = file_lines[0]
                # Deals with cases where the log file only has one line
                # checks if the host-name is in the first line and length is less/equal to one
                if ".af.uchicago.edu" in first_line or (
                    "workers-ads-long-" in first_line and N <= 1
                ):
                    try:
                        self.checks_for_split_logs(l)
                    except FileNotFoundError:
                        dateTimeString = log_path.split("/")[4]
                        year = int(dateTimeString[0:4])
                        month = int(dateTimeString[5:7])
                        day = int(dateTimeString[8:10])
                        hour = int(dateTimeString[11:13])
                        start_datetime = dt.datetime(year, month, day, hour, 0, 0)
                        start_date_time_timestamp = int(
                            start_datetime.replace(tzinfo=timezone.utc).timestamp()
                            * 1e3
                        )
                        run_time = 0
                        queue_time = 0
                        payload_size = 0
                        exit_code = 1
                        host_name = first_line
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )

                #  if the host-name is not in the first line continue
                else:
                    # code block parses the first line of the log file
                    # obtains the submission, start time, month, day, year, queue time, time stamp
                    first_line_list = first_line.split(" ")
                    n = len(first_line_list)
                    start_time = first_line_list[0]
                    start_time_h = int(start_time[0:2])
                    start_time_m = int(start_time[3:5])
                    start_time_s = int(start_time[6:8])
                    year = int(first_line_list[-1])
                    month = int(self.months_dic[first_line_list[2]])
                    if n == 8:
                        submit_time = first_line_list[5]
                        day = int(first_line_list[4])
                    elif n == 7:
                        day = int(first_line_list[3])
                        submit_time = first_line_list[4]
                    submit_time_h = int(submit_time[0:2])
                    submit_time_m = int(submit_time[3:5])
                    submit_time_s = int(submit_time[6:8])
                    start_datetime = dt.datetime(
                        year, month, day, start_time_h, start_time_m, start_time_s
                    )
                    submit_datetime = dt.datetime(
                        year, month, day, submit_time_h, submit_time_m, submit_time_s
                    )
                    queue_time = int((start_datetime - submit_datetime).total_seconds())
                    start_date_time_timestamp = int(
                        start_datetime.replace(tzinfo=timezone.utc).timestamp() * 1e3
                    )
                    ################################################################################

                    # works on the last line of the log file
                    last_line = file_lines[N - 1]
                    # if the name of the payload file is in the last line
                    # Gets: end time, run time, host-name, payload size, exit code, and creates dic.
                    if "EVNT.root" in last_line:
                        end_time = file_lines[N - 3].split(" ")[0]
                        end_time_h = int(end_time[0:2])
                        end_time_m = int(end_time[3:5])
                        end_time_s = int(end_time[6:8])
                        end_datetime = dt.datetime(
                            year, month, day, end_time_h, end_time_m, end_time_s
                        )
                        run_time = int((end_datetime - start_datetime).total_seconds())
                        if run_time < 0:
                            run_time += int((dt.timedelta(days=1)).total_seconds())
                        host_name = file_lines[N - 2]
                        payload_size = last_line.split("\t")[0]
                        exit_code = 0
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )

                    # if the host-name is in the last line of the file
                    # Gets:  end time, run time, host-name, payload size (0), exit code(1), and creates dic.
                    elif (
                        ".af.uchicago.edu" in last_line
                        or "workers-ads-long-" in last_line
                    ):
                        host_name = last_line
                        payload_size = 0
                        exit_code = 1
                        end_time = file_lines[N - 2].split(" ")[0]
                        end_time_h = int(end_time[0:2])
                        end_time_m = int(end_time[3:5])
                        end_time_s = int(end_time[6:8])
                        end_datetime = dt.datetime(
                            year, month, day, end_time_h, end_time_m, end_time_s
                        )
                        run_time = int((end_datetime - start_datetime).total_seconds())
                        if run_time < 0:
                            run_time += int((dt.timedelta(days=1)).total_seconds())
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )

                    # if an error is in the last line of the file
                    # Gets:  end time, run time, host-name, payload size (0), exit code(1), and creates dic.
                    elif "an unknown exception occurred" in last_line:
                        end_time = file_lines[N - 1].split(" ")[0]
                        end_time_h = int(end_time[0:2])
                        end_time_m = int(end_time[3:5])
                        end_time_s = int(end_time[6:8])
                        end_datetime = dt.datetime(
                            year, month, day, end_time_h, end_time_m, end_time_s
                        )
                        run_time = int((end_datetime - start_datetime).total_seconds())
                        if run_time < 0:
                            run_time += int((dt.timedelta(days=1)).total_seconds())
                        exit_code = 1
                        payload_size = 0
                        host_name = self.checks_for_split_logs(l)[2]
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )

                    # if the paper reference is in the last line of the file
                    # Gets:  end time, run time, host-name, payload size, exit code(0), and creates dic.
                    elif "http://arxiv.org/abs/1412.7420" in last_line:
                        end_time = file_lines[N - 1].split(" ")[0]
                        end_time_h = int(end_time[0:2])
                        end_time_m = int(end_time[3:5])
                        end_time_s = int(end_time[6:8])
                        end_datetime = dt.datetime(
                            year, month, day, end_time_h, end_time_m, end_time_s
                        )
                        run_time = int((end_datetime - start_datetime).total_seconds())
                        if run_time < 0:
                            run_time += int((dt.timedelta(days=1)).total_seconds())

                        host_name = self.checks_for_split_logs(l)[2]
                        payload_size = int(
                            self.checks_for_split_logs(l)[3].split("\t")[0]
                        )
                        exit_code = 0
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )
            else:
                print("ERROR -- FILE WAS NOT OPENED")
            return dic

    def parsing_truth3_batch(self, log_path):
        with open(log_path) as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                # print(l)
                # print(self.checks_for_split_logs(l))

                # Checks the length of the file; when it's one it just contains the host-name
                if N == 1:
                    dateTimeString = log_path.split("/")[4]
                    host_name = file_lines[0]
                    year = int(dateTimeString[0:4])
                    month = int(dateTimeString[5:7])
                    day = int(dateTimeString[8:10])
                    hour = int(dateTimeString[11:13])
                    start_datetime = dt.datetime(year, month, day, hour, 0, 0)
                    start_date_time_timestamp = int(
                        start_datetime.replace(tzinfo=timezone.utc).timestamp() * 1e3
                    )
                    run_time = 0
                    run_time = 0
                    queue_time = 0
                    payload_size = 0
                    exit_code = 1
                    dic = self.dictionary_maker(
                        start_date_time_timestamp,
                        queue_time,
                        run_time,
                        payload_size,
                        exit_code,
                        host_name,
                    )
                # This portion deals with the non-empty logs
                else:
                    # code block parses the first line of the log file
                    # obtains the submission, start time, month, day, year, queue time, time stamp
                    first_line_list = file_lines[0].split(" ")
                    n = len(first_line_list)
                    start_time = first_line_list[0]
                    start_time_h = int(start_time[0:2])
                    start_time_m = int(start_time[3:5])
                    start_time_s = int(start_time[6:8])
                    year = int(first_line_list[-1])
                    month = int(self.months_dic[first_line_list[2]])
                    if n == 8:
                        submit_time = first_line_list[5]
                        day = int(first_line_list[4])
                    elif n == 7:
                        day = int(first_line_list[3])
                        submit_time = first_line_list[4]
                    submit_time_h = int(submit_time[0:2])
                    submit_time_m = int(submit_time[3:5])
                    submit_time_s = int(submit_time[6:8])
                    start_datetime = dt.datetime(
                        year, month, day, start_time_h, start_time_m, start_time_s
                    )
                    submit_datetime = dt.datetime(
                        year, month, day, submit_time_h, submit_time_m, submit_time_s
                    )
                    queue_time = int((start_datetime - submit_datetime).total_seconds())
                    start_date_time_timestamp = int(
                        start_datetime.replace(tzinfo=timezone.utc).timestamp() * 1e3
                    )
                    last_line = file_lines[N - 1]
                    if "DAOD_TRUTH3.TRUTH3.root" in last_line:
                        payload_size = last_line.split("\t")[0]
                        host_name = file_lines[N - 2]
                        end_time = file_lines[N - 3].split(" ")[0]
                        end_time_h = int(end_time[0:2])
                        end_time_m = int(end_time[3:5])
                        end_time_s = int(end_time[6:8])
                        end_datetime = dt.datetime(
                            year, month, day, end_time_h, end_time_m, end_time_s
                        )
                        exit_code = 0
                        run_time = int((end_datetime - start_datetime).total_seconds())
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )
                    else:
                        end_time = last_line.split(" ")[0]
                        end_time_h = int(end_time[0:2])
                        end_time_m = int(end_time[3:5])
                        end_time_s = int(end_time[6:8])
                        end_datetime = dt.datetime(
                            year, month, day, end_time_h, end_time_m, end_time_s
                        )
                        run_time = int((end_datetime - start_datetime).total_seconds())
                        host_name = self.checks_for_split_logs(l)[2]
                        if self.checks_for_split_logs(l)[3] != 0:
                            payload_size = int(
                                (self.checks_for_split_logs(l)[3]).split("\t")[0]
                            )
                            exit_code = 0
                        else:
                            payload_size = 0
                            exit_code = 1
                        host_name = self.checks_for_split_logs(l)[2]
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )
                return dic

    def ntuple_parsing(self, l):
        with open(log_path) as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                queue_time = 0
                payload_size = 0
                lines_dates = []
                for line in file_lines:
                    if "2025-" in line:
                        lines_dates.append(line)
                if "ntuple_cfw.pdf" in file_lines[N - 1]:
                    exit_code = 0
                else:
                    exit_code = 1
                if "af.uchicago.edu" in file_lines[N - 1]:
                    host_name = file_lines[N - 1]
                elif "af.uchicago.edu" in file_lines[N - 2]:
                    host_name = file_lines[N - 2]
                else:
                    host_name = "login01.af.uchicago.edu"
                n = len(lines_dates)
                try:
                    start_date = lines_dates[0].split(" ")[0]
                    start_time = lines_dates[0].split(" ")[1][0:8]
                    end_date = lines_dates[n - 1].split(" ")[0]
                    end_time = lines_dates[n - 1].split(" ")[1][0:8]
                    start_time_object = dt.datetime.strptime(start_time, "%H:%M:%S")
                    start_date_object = dt.datetime(
                        int(start_date[0:4]),
                        int(start_date[5:7]),
                        int(start_date[8:10]),
                    )
                    start_date_time = dt.datetime.combine(
                        start_date_object.date(), start_time_object.time()
                    )
                    start_date_time_timestamp = int(
                        start_date_time.replace(tzinfo=timezone.utc).timestamp() * 1e3
                    )
                    end_time_object = dt.datetime.strptime(end_time, "%H:%M:%S")
                    end_date_object = dt.datetime(
                        int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10])
                    )
                    end_date_time = dt.datetime.combine(
                        end_date_object.date(), end_time_object.time()
                    )
                    run_time = int((end_date_time - start_date_time).total_seconds())
                    dic = self.dictionary_maker(
                        start_date_time_timestamp,
                        queue_time,
                        run_time,
                        payload_size,
                        exit_code,
                        host_name,
                    )
                except IndexError:
                    try:
                        dic = self.string_and_split(l)
                    except FileNotFoundError:
                        host_name = file_lines[N - 1]
                        dateTimeString = log_path.split("/")[4]
                        year = int(dateTimeString[0:4])
                        month = int(dateTimeString[5:7])
                        day = int(dateTimeString[8:10])
                        hour = int(dateTimeString[11:13])
                        start_date_time = dt.datetime(year, month, day, hour, 0, 0)
                        start_date_time_timestamp = int(
                            start_date_time.replace(tzinfo=timezone.utc).timestamp()
                            * 1e3
                        )
                        run_time = 0
                        payload_size = 0
                        dic = self.dictionary_maker(
                            start_date_time_timestamp,
                            queue_time,
                            run_time,
                            payload_size,
                            exit_code,
                            host_name,
                        )
        return dic
