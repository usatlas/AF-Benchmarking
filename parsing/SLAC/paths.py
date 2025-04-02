import datetime as dt
from elasticsearch import Elasticsearch as es
import json
from datetime import timezone
import os
import traceback

class Paths_Class:

    # constructor
    def __init__(self, site_dir, job_name, log_name, site):
        # Directory of the log files
        self.site_dir = site_dir
        # Name of the job
        self.job_name = job_name
        # Name of the log file
        self.log_name = log_name
        # Name of the AF site
        self.site = site
    
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

