import datetime as dt
#from elasticsearch import Elasticsearch as es
import json
from datetime import timezone
import os
import traceback

class Parsing_Class:
    af_dictionary = {'uc':'UC-AF', 'slac':'SLAC-AF', 'bnl':'BNL-AF'}
    job_dictionary = {'Rucio': 'Rucio Download'}
    dic_keys = ["cluster", "testType", "submitTime", "queueTime", "runTime", "payloadSize", "status", "host"]
    
    def __init__(self, site_dir, job_name, log_name, site):
        self.site_dir = site_dir
        self.job_name = job_name
        self.log_name = log_name
        self.site = site
    
    def benchmark_path(self):
        benchmark_paths = [os.path.join(self.site_dir, i) for i in sorted(os.listdir(self.site_dir))]
        return benchmark_paths
    
    def full_path_function(self, benchmark_paths):
        full_path_list = []
        for i in benchmark_paths:
            if self.job_name in os.listdir(i):
                dir_with_job_name = os.path.join(i, self.job_name)
                full_path_list.append(os.path.join(dir_with_job_name, self.log_name))
        return full_path_list

    def parsing_rucio(self, l):
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
                payload_size = (file_lines[N-1]).split("\t")[0]
            
                # Grabs the start and end date-time lines; splits them at various characters and grabs first element
                start_time_line = file_lines[0].split('\x1b[32;1m')[1].split(',')[0]
                end_time_line = file_lines[N-12].split('\x1b[32;1m')[1].split(',')[0]

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
