import datetime as dt
#from elasticsearch import Elasticsearch as es
import json
from datetime import timezone
import os
import traceback
from typing import ClassVar


class Parsing_Class:
    # Shared qualities among all objects created with this class

    # Dictionary used to obtain AF script is running at
    af_dictionary: ClassVar[dict[str, str]] = {'uc': 'UC-AF', 'slac': 'SLAC-AF', 'bnl': 'BNL-AF'}


    # Dictionary used to obtain job string recognized by ElasticSearch
    job_dictionary = {'Rucio': 'Rucio Download', "TRUTH3": "truth3-batch", "EVNT": "EVNT-batch", "Coffea_Hist": "ntuple-hist-coffea", "TRUTH3_centos": "truth3-centos-container-batch", "TRUTH3_el9_container": "truth3-el9-container-batch", "TRUTH3_centos_interactive": "truth3-centos-container-interactive", "TRUTH3_interactive": "truth3-interactive", "EVNT_contained_el9":"EVNT-el9-container-batch", "EVNT_contained_centos7": "EVNT-centos7-container-batch", "TRUTH3_el9_container_interactive":"truth3-el9-container-interactive", "EVNT_container_el":"EVNT-el9-container-batch", "EVNT_container_centos":"EVNT-centos7-container-batch", "TRUTH3_centos7_container":"truth3-centos-container-batch" }
    
    # Dictionary keys that are used to create dictionaries with no values
    dic_keys = ["cluster", "testType", "submitTime", "queueTime", "runTime", "payloadSize", "status", "host"]
    
    # Dictionary storing the directory where the script directories are located at sites
    ## UPDATE: Need to include SLAC and BNL ##
    benchmarks_dir_dic = {"uc": "/data/selbor/parsing_jobs", "slac": None, "bnl": None}
    
    # Dictionary that contains months mapped to numbers; used when parsing EVNT and TRUTH3 log files
    months_dic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

    # Constructor
    def __init__(self, site_dir, job_name, log_name, site):
        # Directory of the log file
        self.site_dir = site_dir
        # Name of the job
        self.job_name = job_name
        # Name of the log file
        self.log_name = log_name
        # Name of the AF Site
        self.site = site
        # Name of the split log file
        self.split='split.log'
        # Name of piped output
        self.piped='pipe_file.log'
    
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
    

