import datetime as dt
import os
import json
from datetime import timezone

"""
Set the following:
    - testing directory
    - python script directory
    - the af the script is running at
"""


# Setting the directory where all of the dated directories are stored
testing_dir = r"/Users/selbor/Work/benchmarks"


# From the sorted directories within testing_dir
## create a list containing the paths
def path_function(testing_dir):
    list_of_paths = []
    for i in sorted(os.listdir(testing_dir)):
        list_of_paths.append(os.path.join(testing_dir, i))
    return list_of_paths


# From the list of dated paths
## make a list of absolute paths
def full_path_function(list_of_paths):
    list_of_full_path = []
    for i in list_of_paths:
        # Considering just changing the name of the job for every job; make it a function
        if "Rucio" in os.listdir(i):
            dir_with_job_name = os.path.join(i, "Rucio")
            name_of_log_file = "rucio.log"
            list_of_full_path.append(os.path.join(dir_with_job_name, name_of_log_file))
    return list_of_full_path


# From the given list of files
## Parse through them and get the submit/exit datetime objects, payload size, and host machine
## return it as a tuple
def parsing_function(element_from_list_of_full_path):
    f = open(element_from_list_of_full_path)
    if f:
        date_time_list = []
        lines = f.readlines()
        N = len(lines)
        # Obtains the host machine
        host_machine = lines[N - 2]
        host_machine = host_machine[:-1]
        # Following seven lines obtain the payload size and host machine if there is an error
        payload_size_line = lines[N - 1].split("\t")
        payload_size = payload_size_line[0]
        try:
            payload_size = int(payload_size)
            exit_status = 0
            queue_time = 0
        except ValueError:
            host_machine = payload_size[:-1]
            payload_size = 0
            exit_status = 1
            queue_time = 0
        # Following ten lines get the date/time when submitted and exited
        for line in lines:
            if "INFO" in line:
                line_elements = line.split(",")
                date_time_in_file = line_elements[0].split("\x1b[32;1m")
                date_time_list.append(date_time_in_file[1])
        n = len(date_time_list)
        submit_date_time = date_time_list[0].split(" ")
        exit_date_time = date_time_list[n - 1].split(" ")
        submit_date_time_object = dt.datetime(
            int(submit_date_time[0][0:4]),
            int(submit_date_time[0][5:7]),
            int(submit_date_time[0][8:10]),
            int(submit_date_time[1][0:2]),
            int(submit_date_time[1][3:5]),
            int(submit_date_time[1][6:8]),
        )
        exit_date_time_object = dt.datetime(
            int(exit_date_time[0][0:4]),
            int(exit_date_time[0][5:7]),
            int(exit_date_time[0][8:10]),
            int(exit_date_time[1][0:2]),
            int(exit_date_time[1][3:5]),
            int(exit_date_time[1][6:8]),
        )
        run_time = int(
            (exit_date_time_object - submit_date_time_object).total_seconds()
        )
        submit_date_time_object = submit_date_time_object.replace(tzinfo=timezone.utc)
    else:
        print("ERROR -- FILE WAS NOT OPENED")
    f.close()
    return (
        submit_date_time_object,
        run_time,
        payload_size,
        host_machine,
        queue_time,
        exit_status,
    )


def creates_dictionaries(list_of_parsed_data, af_location="uc"):
    af_dictionary = {"uc": "UC-AF", "slack": "SLAC-AF", "bnl": "BNL-AF"}
    list_of_dics = []
    for tuples in list_of_parsed_data:
        dic = {}
        dic["cluster"] = af_dictionary[af_location]
        dic["testType"] = "Rucio Download"
        # Make this into UTC; best to do it in the parsing function.
        dic["submitTime"] = int(tuples[0].timestamp() * 1000)
        dic["queueTime"] = int(tuples[4])
        dic["runTime"] = tuples[1]
        dic["payloadSize"] = tuples[2]
        dic["status"] = tuples[5]
        dic["host"] = tuples[3]
        list_of_dics.append(dic)
    return list_of_dics


def makes_json_instances(list_of_dics):
    list_of_jsons = []
    for dics in list_of_dics:
        list_of_jsons.append(json.dumps(dics))
    return list_of_jsons


def bookkeeping_data(list_of_jsons):
    python_script_dir = r"/Users/selbor/Work/env/"
    if "rucio_sent.txt" in os.listdir(python_script_dir):
        instances_not_in_file = []
        f = open("rucio_sent.txt")
        formatted_lines = []
        if f:
            lines_in_file = f.readlines()
            for lines in lines_in_file:
                line = (lines.split("\n"))[0]
                formatted_lines.append(line)
        f.close()
        sent_set = set(formatted_lines)
        new_set = set(list_of_jsons)
        diff_set = new_set - sent_set
    else:
        f = open("rucio_sent.txt", "w")
        if f:
            for instance in list_of_jsons:
                f.write(instance + "\n")
        f.close()
    return diff_set


def append_new_data(diff_set):
    python_script_dir = r"/Users/selbor/Work/env/"
    f = open("rucio_sent.txt", "a")
    if f:
        for item in diff_set:
            f.write(item + "\n")
    f.close()


def saving_data_as_tuple(list_of_dics, list_of_full_path, list_of_jsons):
    datesThour = []
    for i in list_of_full_path:
        items = i.split("/")
        datesThour.append(items[5])
    success_fail = []
    for dics in list_of_dics:
        exit_code = dics.get("status")
        if exit_code == 1:
            success_fail.append("Failure")
        else:
            success_fail.append("Success")
    f = open("rucio_job_log.txt", "w")
    if f:
        for i in range(len(datesThour)):
            f.write(
                datesThour[i] + " " + list_of_jsons[i] + " " + success_fail[i] + "\n"
            )
    f.close


def main():
    list_of_paths = path_function(testing_dir)

    list_of_full_path = full_path_function(list_of_paths)

    list_of_parsed_data = []

    for element_from_list_of_full_path in list_of_full_path:
        list_of_parsed_data.append(parsing_function(element_from_list_of_full_path))

    list_of_dics = creates_dictionaries(list_of_parsed_data)

    list_of_jsons = makes_json_instances(list_of_dics)

    diff_set = bookkeeping_data(list_of_jsons)

    append_new_data(diff_set)

    saving_data_as_tuple(list_of_dics, list_of_full_path, list_of_jsons)


if __name__ == "__main__":
    main()
