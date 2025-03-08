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
    job_dictionary = {'Rucio': 'Rucio Download', "TRUTH3": "truth3-batch", "EVNT": "EVNT-batch", "Coffea_Hist": "ntuple-hist-coffea", "TRUTH3_centos": "truth3-centos-container-batch", "TRUTH3_el9_container": "truth3-el9-container-batch", "TRUTH3_centos_interactive": "truth3-centos-container-interactive", "TRUTH3_interactive": "truth3-interactive", "EVNT_contained_el9":"EVNT-el9-container-batch", "EVNT_contained_centos7": "EVNT-centos7-container-batch", "TRUTH3_el9_container_interactive":"truth3-el9-container-interactive"}
    
    # Dictionary keys that are used to create dictionaries with no values
    dic_keys = ["cluster", "testType", "submitTime", "queueTime", "runTime", "payloadSize", "status", "host"]
    
    # Dictionary storing the directory where the script directories are located at sites
    ## UPDATE: Need to include SLAC and BNL ##
    benchmarks_dir_dic = {"uc": "/data/selbor/parsing_jobs", "slac": None, "bnl": None}
    
    # Dictionary that contains months mapped to numbers; used when parsing EVNT and TRUTH3 log files
    months_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    # Constructor
    def __init__(self, site_dir, job_name, log_name, site):
        # Directory of the log files
        self.site_dir = site_dir
        # Name of the job
        self.job_name = job_name
        # Name of the log file
        self.log_name = log_name
        # Name of the AF site
        self.site = site
        # Name of the split log file
        self.split='split.log'
    
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
    def parsing_rucio(self, l, sti=0, eti=12, psi=1):
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
                try:
                    payload_size = int((file_lines[N-psi]).split("\t")[0])
                except ValueError:
                    payload_size = int(0)
                    host_name = file_lines[N-1]
            
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


    def parsing_rucio_e1(self, l):
        # Creates a dictionary with predetermined keys
        dic = dict.fromkeys(self.dic_keys)
        queue_time = int(0)
        run_time = int(0)
        payload_size = int(0)
        exit_code = int(1)
        date_time_string = l.split('/')[4]
        year = int(date_time_string[0:4])
        month = int(date_time_string[5:7])
        day = int(date_time_string[8:10])
        hour = int(date_time_string[11:13])
        start_date_object=dt.datetime(year, month, day, hour, int(0), int(0))
        # Gets the time stamp and multiplies it by 1000
        start_date_time_timestamp = int(start_date_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                host_name=file_lines[N-1]
            else:
                print("ERROR -- FILE WAS NOT OPENED")
 
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
                
                # Gives the last line in the log file, without hostname or payload size
                if os_used=="centos":
                    end_line_list = file_lines[N-4].split(" ")
                elif os_used=="el":
                    end_line_list = file_lines[N-3].split(" ")
                elif os_used=="native":
                    end_line_list = file_lines[N-3].split(" ")
                # Checks the exit code
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

    def parsing_truth3_e1(self, l, os_used="native", container=False, batch=False):
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                dic = dict.fromkeys(self.dic_keys)
                date_time_string = (l.split("/"))[4]
                start_year = int(date_time_string[0:4])
                start_month = int(date_time_string[5:7])
                start_day = int(date_time_string[8:10])
                start_hour = int(date_time_string[11:13])
                start_min = int(0)
                start_sec= int(0)
                start_datetime_object = dt.datetime(start_year, start_month, start_day, start_hour, start_min, start_sec)
                start_date_timestamp = int(start_datetime_object.timestamp()*1e3)
                # Creates a dictionary with predetermined keys
                dic = dict.fromkeys(self.dic_keys)
                # Assigns values to the keys
                dic[self.dic_keys[0]] = self.af_dictionary[self.site]
                dic[self.dic_keys[1]] = self.job_dictionary[self.job_name]
                dic[self.dic_keys[2]] = start_date_timestamp
                dic[self.dic_keys[3]] = int(0)
                dic[self.dic_keys[4]] = int(0)
                dic[self.dic_keys[5]] = int(0)
                dic[self.dic_keys[6]] = int(1)
                dic[self.dic_keys[7]] = file_lines[0]
            else:
                print("ERROR -- FILE WAS NOT OPENED")
        return dic

    # Parsing TRUTH3 with new log splitting workflow
    def parsing_truth3_log_split(self, l, os_used='native', container=False, batch=False): 
        # Getting the absolute path of the split log file
        split_log_path = l.replace(self.log_name, self.split)
        # Creates a dictionary with predetermined keys
        dic = dict.fromkeys(self.dic_keys)
        # Opening the log file produced by the scheduled job
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                first_line = file_lines[0].split(" ")
                # Getting the start time
                start_time = first_line[0]
                # Getting the month
                month = int(self.months_dic[first_line[2]])
                # Getting the day, submit time, year
                try:
                    day = int(first_line[3])
                    submit_time = first_line[4]
                    year = int(first_line[6])
                except ValueError:
                    day = int(first_line[4])
                    submit_time = first_line[5]
                    year = int(first_line[7])
                # Start and submit list
                start_time_list = start_time.split(":")
                submit_time_list = submit_time.split(":")
                # Start and submit time objects
                start_time_object = dt.datetime(year, month, day, int(start_time_list[0]), int(start_time_list[1]), int(start_time_list[2]))
                submit_time_object = dt.datetime(year, month, day, int(submit_time_list[0]), int(submit_time_list[1]), int(submit_time_list[2]))
                # Checks if the job is batch
                if batch:
                    start_time_timestamp = int((start_time_object.timestamp())*1e3)
                    queue_time = int((start_time_object - submit_time_object).total_seconds())
                else:
                    start_time_timestamp = int((start_time_object.replace(tzinfo=timezone.utc).timestamp())*1e3)
                    queue_time = int(0)

                # Checks exit codes and obtains last line
                if os_used=="centos":
                    exit_code_line = file_lines[N-2]
                elif os_used=="el":
                    exit_code_line = file_lines[N-1]
                elif os_used=='native':
                    exit_code_line= file_lines[N-1]
                last_line = file_lines[N-1]
                if "successful run" in exit_code_line:
                    exit_code = int(0)
                else:
                    exit_code=int(1)
                end_time = last_line.split(" ")[0]
                end_time_list = end_time.split(':')
                end_time_object = dt.datetime(year, month, day, int(end_time_list[0]), int(end_time_list[1]), int(end_time_list[2]))
                run_time = int((end_time_object - start_time_object).total_seconds())
            else:
                print("ERROR -- FILE WAS NOT OPENED")

        with open(split_log_path, 'r') as g:
            if g:
                file_lines = g.read().splitlines()
                n = len(file_lines)
                if n==4:
                    host_name = file_lines[n-2]
                    payload_size = file_lines[n-1].split("\t")[0]
                else:
                    host_name=file_lines[n-1]
                    payload_size=int(0)
            else:
                print("ERROR -- FILE WAS NOT OPENED")
        # Assigns values to the keys
        # Cluster
        dic[self.dic_keys[0]] = self.af_dictionary[self.site]
        # Test Type
        dic[self.dic_keys[1]] = self.job_dictionary[self.job_name]
        # Submit Time
        dic[self.dic_keys[2]] = start_time_timestamp
        # Queue Time
        dic[self.dic_keys[3]] = queue_time
        # Run time
        dic[self.dic_keys[4]] = run_time
        # Payload Size
        dic[self.dic_keys[5]] = payload_size
        # Status
        dic[self.dic_keys[6]] = exit_code
        # Host Name
        dic[self.dic_keys[7]] = host_name
        return dic
    


    def parsing_truth3_interactive(self, l, os_used="native", container=False, batch=False, year_index=7, day_index=4, submit_time_index=5):
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
                start_date_time_timestamp = int((start_time_datetime_object.replace(tzinfo=timezone.utc).timestamp())*1e3)
                # Obtains the queue time
                queue_time = int((start_time_datetime_object - submit_time_datetime_object).total_seconds())
                payload_line_list = file_lines[N-1].split("\t")
                if "DAOD_TRUTH3.TRUTH3.root" in payload_line_list:
                    payload_size = int(payload_line_list[0])
                    end_time_string = file_lines[N-3].split(" ")[0]
                    exit_code = int(0)
                else:
                    end_time_string = file_lines[N-1].split(" ")[0]
                    payload_size = int(0)
                    exit_code = int(1)
                end_datetime_object=dt.datetime(year, month, day, int(end_time_string[0:2]), int(end_time_string[3:5]), int(end_time_string[6:8]))
                run_time = int((end_datetime_object - start_time_datetime_object).total_seconds())
                host_name_line = file_lines[N-2].split(" ")
                if "login01.af.uchicago.edu" in host_name_line:
                    host_name = host_name_line[0]
                else:
                    host_name = "login01.af.uchicago.edu"
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
        # Creates a dictionary with predetermined keys
        dic = dict.fromkeys(self.dic_keys)

        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                first_line = file_lines[0]
                last_line = file_lines[N-1]
                # Checks if the whole log file is there; if it isn't then the first line is just the host name
                if first_line==last_line:
                    host_name = first_line
                    payload_size = int(0)
                    exit_code=int(1)
                    run_time=int(0)
                    queue_time=int(0)
                    start_string=l.split('/')[4]
                    year = int(start_string[0:4])
                    month = int(start_string[5:7])
                    day = int(start_string[8:10])
                    hour = int(start_string[11:13])
                    start_datetime_object = dt.datetime(year, month, day, hour, int(0), int(0))
                    start_date_time_timestamp = int(start_datetime_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                elif ".af.uchicago.edu" in last_line:
                    host_name=last_line
                    exit_code = int(1)
                    payload_size=int(0)
                    last_line = file_lines[N-2]
                    first_line_list = first_line.split(" ")
                    start_time = first_line_list[0]
                    month = int(self.months_dic[first_line_list[2]])
                    year = int(first_line_list[-1])
                    if len(first_line_list)==8:
                        day = int(first_line_list[4])
                        submit_time = first_line_list[5]
                    else:
                        day = int(first_line_list[3])
                        submit_time = first_line_list[4]
                    last_line_list =last_line.split(" ")
                    start_time_object = dt.datetime(year, month, day, int(start_time[0:2]), int(start_time[3:5]), int(start_time[6:8]))
                    submit_time_object = dt.datetime(year, month, day, int(submit_time[0:2]), int(submit_time[3:5]), int(submit_time[6:8]))
                    start_date_time_timestamp = int(start_time_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                    if start_time_object==submit_time_object:
                        queue_time = int(0)
                    else:
                        queue_time = int((start_time_object-submit_time_object).total_seconds())
                    end_time = last_line_list[0]
                    end_time_object = dt.datetime(year, month, day, int(end_time[0:2]), int(end_time[3:5]), int(end_time[6:8]))
                    run_time = int((end_time_object-start_time_object).total_seconds())
                elif "EVNT.root" in last_line:
                    payload_size=last_line.split("\t")[0]
                    last_line = file_lines[N-5]
                    host_name = file_lines[N-2]
                    if "successful run" in last_line:
                        exit_code=int(0)
                    else:
                        exit_code=int(1)
                    first_line_list = first_line.split(" ")
                    start_time = first_line_list[0]
                    month = int(self.months_dic[first_line_list[2]])
                    year = int(first_line_list[-1])
                    if len(first_line_list)==8:
                        day = int(first_line_list[4])
                        submit_time = first_line_list[5]
                    else:
                        day = int(first_line_list[3])
                        submit_time = first_line_list[4]
                    last_line_list =last_line.split(" ")
                    start_time_object = dt.datetime(year, month, day, int(start_time[0:2]), int(start_time[3:5]), int(start_time[6:8]))
                    submit_time_object = dt.datetime(year, month, day, int(submit_time[0:2]), int(submit_time[3:5]), int(submit_time[6:8]))
                    start_date_time_timestamp = int(start_time_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                    if start_time_object==submit_time_object:
                        queue_time = int(0)
                    else:
                        queue_time = int((start_time_object-submit_time_object).total_seconds())
                    end_time = last_line_list[0]
                    end_time_object = dt.datetime(year, month, day, int(end_time[0:2]), int(end_time[3:5]), int(end_time[6:8]))
                    run_time = int((end_time_object-start_time_object).total_seconds())
                else:
                    last_line = file_lines[N-3]
                    if "successful run" in last_line:
                        exit_code=int(0)
                    else:
                        exit_code=int(1)
                    first_line_list = first_line.split(" ")
                    start_time = first_line_list[0]
                    month = int(self.months_dic[first_line_list[2]])
                    year = int(first_line_list[-1])
                    if len(first_line_list)==8:
                        day = int(first_line_list[4])
                        submit_time = first_line_list[5]
                    else:
                        day = int(first_line_list[3])
                        submit_time = first_line_list[4]
                    last_line_list =last_line.split(" ")
                    start_time_object = dt.datetime(year, month, day, int(start_time[0:2]), int(start_time[3:5]), int(start_time[6:8]))
                    submit_time_object = dt.datetime(year, month, day, int(submit_time[0:2]), int(submit_time[3:5]), int(submit_time[6:8]))
                    start_date_time_timestamp = int(start_time_object.replace(tzinfo=timezone.utc).timestamp()*1e3)
                    if start_time_object==submit_time_object:
                        queue_time = int(0)
                    else:
                        queue_time = int((start_time_object-submit_time_object).total_seconds())
                    end_time = last_line_list[0]
                    end_time_object = dt.datetime(year, month, day, int(end_time[0:2]), int(end_time[3:5]), int(end_time[6:8]))
                    run_time = int((end_time_object-start_time_object).total_seconds())
                    # Getting the absolute path of the split log file
                    split_log_path = l.replace(self.log_name, self.split)

                    with open(split_log_path, 'r') as g:
                        if g:
                            file_lines = g.read().splitlines()
                            n = len(file_lines)
                            if n==4:
                                host_name = file_lines[n-2]
                                payload_size = file_lines[n-1].split("\t")[0]
                            else:
                                host_name=file_lines[n-1]
                                payload_size=int(0)
                        else:
                            print("ERROR -- FILE WAS NOT OPENED")
            else:
                print("ERROR -- FILE WAS NOT OPENED")
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

    def parsing_evnt_log_split(self, l, os_used='native', container=False, batch=True):
        # Getting the absolute path of the split log file
        split_log_path = l.replace(self.log_name, self.split)
        # Creates a dictionary with predetermined keys
        dic = dict.fromkeys(self.dic_keys)
        # Opening the log file produced by the scheduled job
        with open(l, 'r') as f:
            if f:
                file_lines = f.read().splitlines()
                N = len(file_lines)
                print(file_lines[0])
            else:
                print("ERROR -- FILE WAS NOT OPENED")




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

    def parsing_ntuple_c_e2(self, l, fli=7):
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
                queue_time=int(0)
                if "AssertionError" in file_lines[N-2]:
                    exit_code=int(1)
                    host_name=file_lines[N-1]
                    run_time=int(0)
                    payload_size=int(0)
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
