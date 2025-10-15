import datetime as dt
import os
import json
from elasticsearch import Elasticsearch
from datetime import timezone

logs_dir=r"/data/selbor/benchmarks"
job = "Coffea_Hist"
log_file="coffea_hist.log"
python_script_dir = r"<Python Script Directory>"
af_location=

months_dic = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

# This cell makes a list of all of the directories in logs_dir
def list_of_dirs(logs_dir, job):
    names_of_files = os.listdir(logs_dir)
    list_of_dates = []
    for files in names_of_files:
        list_of_dates.append(files)
    return list_of_dates

def list_of_full_paths(list_of_dates, job, logs_dir):
    paths_to_jobs = []
    for dirs in sorted(list_of_dates):
        new_path = os.path.join(logs_dir,dirs)
        full_path = os.path.join(new_path, job)
        if os.path.exists(full_path):
            paths_to_jobs.append(full_path)
    list_of_full_path = []
    for p in paths_to_jobs:
        if log_file in sorted(os.listdir(p)):
            list_of_full_path.append(os.path.join(p,log_file))
    return list_of_full_path

def parsing_function(l):
    f = open(l, 'r')
    if f:
        lines = f.read()
        lines_list = lines.splitlines()
        N = len(lines_list)
        start_time_list = lines_list[11].split(" ")
        start_year = start_time_list[0][0:4]
        start_month = start_time_list[0][5:7]
        start_day = start_time_list[0][8:10]
        start_hour = start_time_list[1][0:2]
        start_minute = start_time_list[1][3:5]
        start_second = start_time_list[1][6:8]
        try:
            start_datetime_object = dt.datetime(int(start_year), int(start_month), int(start_day), int(start_hour), int(start_minute), int(start_second))
        except ValueError:
            start_time_list = lines_list[7].split(" ")
            start_year = start_time_list[0][0:4]
            start_month = start_time_list[0][5:7]
            start_day = start_time_list[0][8:10]
            start_hour = start_time_list[1][0:2]
            start_minute = start_time_list[1][3:5]
            start_second = start_time_list[1][6:8]
            start_datetime_object = dt.datetime(int(start_year), int(start_month), int(start_day), int(start_hour), int(start_minute), int(start_second))
        end_time_list = lines_list[N-3].split(" ")
        end_year = end_time_list[0][0:4]
        end_month = end_time_list[0][5:7]
        end_day = end_time_list[0][8:10]
        end_hour = end_time_list[1][0:2]
        end_minute = end_time_list[1][3:5]
        end_second = end_time_list[1][6:8]
        end_datetime_object = dt.datetime(int(end_year), int(end_month), int(end_day), int(end_hour), int(end_minute), int(end_second))
        run_time = end_datetime_object - start_datetime_object
        host_machine = lines_list[N-2]
        if '25\tntuple_cfw.pdf' in lines_list:
            exit_code = int(0)
        else:
            exit_code = int(1)
        host_machine = lines_list[N-2]
        payload_size = int(0)
        queue_time = int(0)
        start_datetime_object = start_datetime_object.replace(tzinfo=timezone.utc)
        run_time = int(run_time.total_seconds())
        return (start_datetime_object, run_time, payload_size, host_machine, queue_time, exit_code)
    else:
        print("ERROR -- FILE WAS NOT OPENED")
    f.close()


def creates_dics(list_of_data_tuples, af_location):
    af_dictionary = {'uc':'UC-AF', 'slac':'SLAC-AF', 'bnl':'BNL-AF'}
    list_of_dics = []
    for tuples in list_of_data_tuples:
        dic={}
        dic["cluster"]=af_dictionary[af_location]
        dic["testType"] = "ntuple-hist-coffea"
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
    if 'coffea_sent.txt' in os.listdir(python_script_dir):
        instances_not_in_file = []
        f = open('coffea_sent.txt', 'r')
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
        f = open('coffea_sent.txt', 'w')
        if f:
            for instance in list_of_jsons:
                f.write(instance + "\n")
        f.close()
    return diff_set

def sending_data_to_es(diff_set, list_of_jsons):
    es = Elasticsearch(
            [{'host':"atlas-kibana.mwt2.org", 'port': 9200, 'scheme': "https"}],
            basic_auth=("<USERNAME>", "<PASSWORD>")
            )
    try:
        response = es.info()
        success = True
    except Exception as e:
        success = False
        print(e)
    if success:
        for i in list_of_jsons:
            if i in diff_set:
                es.index(
                        index="af_benchmarks",
                        document=i
                        )

def append_new_data(diff_set):
    f = open('coffea_sent.txt', 'a')
    if f:
        for item in diff_set:
            f.write(item + "\n")
    f.close()

def saving_data_as_tuple(list_of_dics, list_of_full_path, list_of_jsons):
    datesThour = []
    for i in list_of_full_path:
        items = i.split("/")
        datesThour.append(items[4])
    success_fail = []
    for dics in list_of_dics:
        exit_code = dics.get("status")
        if exit_code == 1:
            success_fail.append("Failure")
        else:
            success_fail.append("Success")
    f = open("coffea_job_log.txt", "w")
    if f:
        for i in range(len(datesThour)):
            f.write(datesThour[i] + " " + list_of_jsons[i] + " " + success_fail[i] + "\n")
    f.close()


def main():
    list_of_dates = list_of_dirs(logs_dir, job)
    list_of_full_path = list_of_full_paths(list_of_dates, job, logs_dir)
    list_of_data_tuples=[]
    for l in list_of_full_path:
        list_of_data_tuples.append(parsing_function(l))
    list_of_dics = creates_dics(list_of_data_tuples, af_location)
    list_of_jsons = makes_json_instances(list_of_dics)
    diff_set = bookkeeping_data(list_of_jsons)
    sending_data_to_es(diff_set, list_of_jsons)
    append_new_data(diff_set)
    saving_data_as_tuple(list_of_dics, list_of_full_path, list_of_jsons)



if __name__ == '__main__':
    main()
