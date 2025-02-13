import datetime as dt
#from elasticsearch import Elasticsearch as es
import json
from datetime import timezone
import os
import traceback

class Parsing_Class:
    # Shared qualities among all objects created with this class

    # Dictionary used to obtain AF script is running at
    af_dictionary = {'uc':'UC-AF', 'slac':'SLAC-AF', 'bnl':'BNL-AF'}

    # Dictionary used to obtain job string recognized by ElasticSearch
    job_dictionary = {'Rucio': 'Rucio Download', "TRUTH3": "truth3-batch", "EVNT": "EVNT-batch", "Coffea_Hist": "ntuple-hist-coffea", "TRUTH3_centos": "truth3-centos-container-batch"}
    
    # Dictionary keys that are used to create dictionaries with no values
    dic_keys = ["cluster", "testType", "submitTime", "queueTime", "runTime", "payloadSize", "status", "host"]
    
    # Dictionary storing the directory where the script directories are located at sites
    ## UPDATE: Need to include SLAC and BNL ##
    benchmarks_dir_dic = {"uc": "/data/selbor/rucio_parse/metrics_env/", "slac": None, "bnl": None}
    
    # Dictionary that contains months mapped to numbers; used when parsing EVNT and TRUTH3 log files
    months_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    # Constructor
    def __init__(self, site_dir, job_name, log_name, site, script_dir):
        self.site_dir = site_dir
        self.job_name = job_name
        self.log_name = log_name
        self.site = site
        self.script_dir = script_dir
    
    # Obtains the paths and writes a list
    def benchmark_path(self):
        benchmark_paths = [os.path.join(self.site_dir, i) for i in sorted(os.listdir(self.site_dir))]
        return benchmark_paths
    
    # Obtains and appends absolute paths for the log files
    def full_path_function(self, benchmark_paths):
        full_path_list = []
        for i in benchmark_paths:
            if self.job_name in os.listdir(i):
                dir_with_job_name = os.path.join(i, self.job_name)
                full_path_list.append(os.path.join(dir_with_job_name, self.log_name))
        return full_path_list

    # Parses rucio.log
    # sti and eti are default cases, can be shifted if there are errors
    def parsing_rucio(self, l, sti=0, eti=12):
        with open(l,'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                # Job is set to fail if the log file isn't the required length
                if N == 113:
                    exit_code = int(0)
                else:
                    exit_code = int(1)

                # Obtains host name
                host_name = (file_lines[N-2])

                # Obtains the payload size; splits the line at "\t" and grabs first element
                payload_size = int((file_lines[N-1]).split("\t")[0])
            
                # Grabs the start and end date-time lines; splits them at various characters and grabs first element
                start_time_line = file_lines[sti].split('\x1b[32;1m')[1].split(',')[0]
                end_time_line = file_lines[N-eti].split('\x1b[32;1m')[1].split(',')[0]

                # Creates the date_time objects
                start_date_time = dt.datetime(int(start_time_line.split(' ')[0][0:4]), int(start_time_line.split(' ')[0][5:7]), int(start_time_line.split(' ')[0][8:10]), int(start_time_line.split(' ')[1][0:2]), int(start_time_line.split(' ')[1][3:5]), int(start_time_line.split(' ')[1][6:8]))
                end_date_time = dt.datetime(int(end_time_line.split(' ')[0][0:4]), int(end_time_line.split(' ')[0][5:7]), int(end_time_line.split(' ')[0][8:10]), int(end_time_line.split(' ')[1][0:2]), int(end_time_line.split(' ')[1][3:5]), int(end_time_line.split(' ')[1][6:8]))

                # Obtains time delta and casts it as an int, run time
                run_time = int((end_date_time - start_date_time).total_seconds())

                # Interactive job has no queue time
                queue_time = int(0)
            
                # Gets the time stamp and multiplies it by 1000
                start_date_time_timestamp = int(start_date_time.replace(tzinfo=timezone.utc).timestamp()*1e3)
            
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
    
    # Parses TRUTH3
    def parsing_truth3(self, l, os_used="native", container=False, batch=False, year_index=7, day_index=4, submit_time_index=5):
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                # Splits the first line and gets hour:min:sec
                start_time_line_list = file_lines[0].split(" ")
                submit_time_list = start_time_line_list[submit_time_index].split(":")
                start_time_list = start_time_line_list[0].split(":")
                # Obtains year,month,day from first line list
                year = int(start_time_line_list[year_index])
                month = int(self.months_dic[start_time_line_list[2]])
                day = int(start_time_line_list[day_index])
                # Creates submit and start datetime objects
                submit_time_datetime_object = dt.datetime(year, month, day, int(submit_time_list[0]), int(submit_time_list[1]), int(submit_time_list[2]))
                start_time_datetime_object = dt.datetime(year, month, day, int(start_time_list[0]), int(start_time_list[1]), int(start_time_list[2]))
                start_date_time_timestamp = int((start_time_datetime_object.timestamp())*1e3)
                # Obtains the queue time
                queue_time = int((start_time_datetime_object - submit_time_datetime_object).total_seconds())
                end_time_line_list = file_lines[N-3].split(" ")
                end_time_list = end_time_line_list[0].split(":")
                end_time_datetime_object = dt.datetime(year, month, day, int(end_time_list[0]), int(end_time_list[1]), int(end_time_list[2]))
                # Obtains the run time
                run_time = int((end_time_datetime_object - start_time_datetime_object).total_seconds())
                # Obtains the exit code from the last line
                if os_used=="centos":
                    end_line_list = file_lines[N-4].split(" ")
                if "0:" in end_line_list:
                    exit_code = int(0)
                else:
                    exit_code = int(1)
                # Obtains host name
                host_name = file_lines[N-2].split("\t")[0]
                # Obtains payload size
                payload_size = int(file_lines[N-1].split("\t")[0])
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

    def parsing_evnt(self, l, os_used="native", container=False, batch=False, day_index=4, submit_time_index=5, year_index=7):
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                start_time_line_list = file_lines[0].split(' ')
                submit_time_list = start_time_line_list[submit_time_index].split(":")
                start_time_list = start_time_line_list[0].split(":")
                # Obtains year,month,day from first line list
                year = int(start_time_line_list[year_index])
                month = int(self.months_dic[start_time_line_list[2]])
                day = int(start_time_line_list[day_index])
                # Creates submit and start datetime objects
                submit_time_datetime_object = dt.datetime(year, month, day, int(submit_time_list[0]), int(submit_time_list[1]), int(submit_time_list[2]))
                start_time_datetime_object = dt.datetime(year, month, day, int(start_time_list[0]), int(start_time_list[1]), int(start_time_list[2]))
                host_name = file_lines[N-2].split(' ')[0]
                end_time_line_list = file_lines[N-5].split(' ')
                if "0:" in end_time_line_list:
                    exit_code = int(0)
                else:
                    exit_code = int(1)
                # Handles the case for exit code 8, there was only one file with this error on 2/8/25
                try:
                    payload_size = int(file_lines[N-1].split('\t')[0])
                except ValueError:
                    payload_size = int(0)
                    exit_code=int(1)
                end_time_list = end_time_line_list[0].split(":")
                end_time_datetime_object = dt.datetime(year, month, day, int(end_time_list[0]), int(end_time_list[1]), int(end_time_list[2]))
                # Obtains the run time
                run_time = int((end_time_datetime_object - start_time_datetime_object).total_seconds())
                queue_time = int((start_time_datetime_object-submit_time_datetime_object).total_seconds())
                start_date_time_timestamp = int(start_time_datetime_object.timestamp()*1e3)
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
    def parsing_evnt_uc_e1(self, l, os_used="native", container=False, batch=False):
        with open(l, 'r') as f:
            if f:
                file_lines=f.read().splitlines()
                N=len(file_lines)
                host_name = file_lines[0]
                start_date_time_list = l.split("/")
                new_datetime_list=start_date_time_list[4].split('.')
                year = int(new_datetime_list[0])
                month = int(new_datetime_list[1])
                day = int(new_datetime_list[2].split("T")[0])
                hour = int(new_datetime_list[2].split("T")[1])
                start_datetime_object = dt.datetime(year, month, day, hour, 0, 0)
                start_date_time_timestamp = int(start_datetime_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                # Creates a dictionary with predetermined keys
                dic = dict.fromkeys(self.dic_keys)
                # Assigns values to the keys
                dic[self.dic_keys[0]] = self.af_dictionary[self.site]
                dic[self.dic_keys[1]] = self.job_dictionary[self.job_name]
                dic[self.dic_keys[2]] = start_date_time_timestamp
                dic[self.dic_keys[3]] = int(0)
                dic[self.dic_keys[4]] = int(0)
                dic[self.dic_keys[5]] = int(0)
                dic[self.dic_keys[6]] = int(1)
                dic[self.dic_keys[7]] = host_name
            else:
                print("ERROR -- FILE WAS NOT OPENED")
        return dic
   
   # Seems like the first line index varies; 7, 11,..,
    def parsing_ntuple_c(self, l, fli=7):
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                # Extracts start date time information
                start_date_time_line_list = file_lines[fli].split(" ")
                start_date_list = start_date_time_line_list[0].split("-")
                year = int(start_date_list[0])
                start_month = int(start_date_list[1])
                start_day = int(start_date_list[2])
                start_time_list = start_date_time_line_list[1].split(":")
                start_hour = int(start_time_list[0])
                start_min = int(start_time_list[1])
                start_sec = int(start_time_list[2][0:2])
                # Creates the date time object
                start_datetime_object = dt.datetime(year, start_month, start_day, start_hour, start_min, start_sec)
                # Obtains time stamp from the date time object
                start_date_time_timestamp = int(start_datetime_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                # Extracts end date time information
                end_date_time_line_list = file_lines[N-3].split(" ")
                end_date_list = end_date_time_line_list[0].split("-")
                year = int(end_date_list[0])
                end_month = int(end_date_list[1])
                end_day = int(end_date_list[2])
                end_time_list = end_date_time_line_list[1].split(":")
                end_hour = int(end_time_list[0])
                end_min = int(end_time_list[1])
                end_sec = int(end_time_list[2][0:2])
                # Creates the end date time object
                end_datetime_object = dt.datetime(year, end_month, end_day, end_hour, end_min, end_sec)
                run_time = int((end_datetime_object - start_datetime_object).total_seconds())
                host_name = file_lines[N-2]
                payload_size = int(0)
                exit_code = int(0)
                queue_time = int(0)
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

    def parsing_ntuple_c_e1(self, l):
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                # Extracts start date time information
                start_date_time_line_list = l.split("/")
                date_time_string = start_date_time_line_list[4]
                date_string = date_time_string.split("T")[0]
                start_hour = int(date_time_string.split("T")[1])
                year = int(date_string[0:4])
                start_month = int(date_string[5:7])
                start_day = int(date_string[8:10])
                start_min = int(0)
                start_sec = int(0)
                # Creates the date time object
                start_datetime_object = dt.datetime(year, start_month, start_day, start_hour, start_min, start_sec)
                # Obtains time stamp from the date time object
                start_date_time_timestamp = int(start_datetime_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                run_time = int(0)
                host_name = file_lines[N-1]
                payload_size = int(0)
                exit_code = int(1)
                queue_time = int(0)
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
 
        '''
        The following functions deal with the data once it has been parsed and stored in the respective dictionaries.
        json_instances:
        - List input containing dictionaries
        - Elements are made into json instances
        - A list consisting of json instances is returned

        bookkeeping_data:
        - Inputs are list of json instances from the previous function and a txt file
        - The contents of the txt file are inserted into an empty list
        - The newly created list and the list of jsons are converted to sets
        - The old_entries_set is then subtracted from the json set yielding the new entries
        - The new entries set is then returned

        append_new_data:
        - The elements of the newly created new_entries_set are appended to the old_entries txt file
        '''

    def json_instances(self, dic_list):
        # For-loop that will return a list of json instances
        list_of_jsons =[]
        for dic in dic_list:
            list_of_jsons.append(json.dumps(dic))
        return list_of_jsons

    def bookkeeping_data(self, list_of_jsons, old_entries):
        # Checks for the existence of the old_entries txt file in the specified directory
        if old_entries in os.listdir(self.benchmarks_dir_dic[self.site]):
            # Elements of the old_entries.txt file are appended to a list
            old_entries_list = []
            with open(old_entries, 'r') as f:
                if f:
                    lines_in_file = f.readlines()
                    for lines in lines_in_file:
                        lines_in_file.append(lines.split("\n")[0])
                # Converts lists into sets
                old_entries_set = set(old_entries_list)
                all_entries_set = set(list_of_jsons)
                # The difference in sets will be the new entries that will be sent
                new_entries_set = all_entries_set - old_entries_set
        else:
            print("FILE DOES NOT EXIST")
        return new_entries_set

    def append_new_data(self, old_entries, new_entries_set):
        with open(old_entries, 'a') as f:
            if f:
                for item in new_entries_set:
                    f.write(item + "\n")
            else:
                print("ERROR -- FILE WAS NOT OPENED")


if __name__=="__main__":
    # Coffea Job requires me to change the index depending on the error
    path_to_logs=r'/Users/selbor/Juan/SCIPP-ATLAS/testing/'
    job_name="TRUTH3_centos"
    log_file_name="log.EVNTtoDAOD"
    af_site="uc"
    parsing=Parsing_Class(path_to_logs, job_name, log_file_name, af_site, "/Users/selbor/Juan/GitStuff/AF-Benchmarking/parsing")
    benchmark_paths = parsing.benchmark_path()
    full_path_list = parsing.full_path_function(benchmark_paths)

    list_dics=[]
    for l in full_path_list:
        try:
            list_dics.append(parsing.parsing_truth3(l, os_used="centos", container=True, batch=True))
        except Exception as e:
            print(l + "\n")
            print(traceback.format_exc())

    print(list_dics)
