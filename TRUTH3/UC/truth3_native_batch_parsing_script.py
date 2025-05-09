import datetime as dt
import os
import json

# Setting the directory where all of the dated directories are stored
testing_dir=r"/Users/selbor/Work/benchmarks/"

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
        if "TRUTH3" in sorted(os.listdir(i)):
            dir_with_job_name = os.path.join(i, "TRUTH3")
            name_of_log_file = "log.Derivation"
            if name_of_log_file in sorted(os.listdir(dir_with_job_name)):
                list_of_full_path.append(os.path.join(dir_with_job_name, name_of_log_file))
            else:
                continue
    return list_of_full_path

# From the given list of files
## Parse through them and get the submit/exit datetime objects, payload size, and host machine
## return it as a tuple
def parsing_function(element_from_list_of_full_path):
    months_dic = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    f = open(element_from_list_of_full_path, 'r')
    if f:
        lines = f.readlines()
        N = len(lines)
        first_line = lines[0]
        first_line_list = first_line.split(" ")
        start_time = first_line_list[0]
        month_submitted = months_dic[first_line_list[2]]
        if len(first_line_list) == 8:
            day_started = first_line_list[4]
            submit_time = first_line_list[5]
            year_submitted = first_line_list[7][:-1]
        else:
            day_started = first_line_list[3]
            submit_time = first_line_list[4]
            year_submitted = first_line_list[6][:-1]
        last_line = lines[N-3]
        last_line_list = last_line.split(" ")
        if '"successful' in last_line_list:
            exit_code = int(0)
        else:
            exit_code = int(1)
        exit_time = last_line_list[0]
        host_machine_line = lines[N-2]
        host_machine = host_machine_line[:-1]
        payload_size_line = lines[N-1]
        payload_size_list = payload_size_line.split("\t")
        payload_size = payload_size_list[0]
        time_diff_queue = dt.datetime.strptime(start_time, "%H:%M:%S") - dt.datetime.strptime(submit_time, "%H:%M:%S")
        queue_time = int(time_diff_queue.total_seconds())
        # Constructs the initial datetime object
        start_datetime_object = dt.datetime(int(year_submitted), int(month_submitted), int(day_started), int(start_time[0:2]), int(start_time[3:4]), int(start_time[6:8]))
        running_time_diff = dt.datetime.strptime(exit_time, "%H:%M:%S") - dt.datetime.strptime(start_time, "%H:%M:%S")
        run_time = int(running_time_diff.total_seconds()) + queue_time
        return (start_datetime_object, run_time, payload_size, host_machine, queue_time, exit_code)
    else:
        print("ERROR -- FILE WAS NOT OPENED")
    f.close()

def creates_dictionaries(list_of_parsed_data, af_location='uc'):
    af_dictionary = {'uc':'UC-AF', 'slac':'SLAC-AF', 'bnl':'BNL-AF'}
    list_of_dics = []
    for tuples in list_of_parsed_data:
        dic = {}
        dic["cluster"] = af_dictionary[af_location]
        dic["testType"] = "truth3-batch"
        # Make this into UTC; best to do it in the parsing function.
        dic["submitTime"] = int(tuples[0].timestamp()*1000)
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
    if 'truth3_native_batch_sent.txt' in os.listdir(python_script_dir):
        instances_not_in_file = []
        f = open('truth3_native_batch_sent.txt', 'r')
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
        f = open('truth3_native_batch_sent.txt', 'w')
        if f:
            for instance in list_of_jsons:
                f.write(instance + "\n")
        f.close()
    return diff_set

def append_new_data(diff_set):
    python_script_dir = r"/Users/selbor/Work/env/"
    f = open('truth3_native_batch_sent.txt', 'a')
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
    f = open("truth3_native_batch_job_log.txt", "w")
    if f:
        for i in range(len(datesThour)):
            f.write(datesThour[i] + " " + list_of_jsons[i] + " " + success_fail[i] + "\n")
    f.close


def main():
    list_of_paths =  path_function(testing_dir)
    list_of_full_path =  full_path_function(list_of_paths)
    list_of_parsed_data = []
    for i in list_of_full_path:
        list_of_parsed_data.append(parsing_function(i))
    list_of_dics = creates_dictionaries(list_of_parsed_data)
    list_of_jsons = makes_json_instances(list_of_dics)
    diff_set = bookkeeping_data(list_of_jsons)
    append_new_data(diff_set)
    saving_data_as_tuple(list_of_dics, list_of_full_path, list_of_jsons)




if __name__ == '__main__':
    main()
