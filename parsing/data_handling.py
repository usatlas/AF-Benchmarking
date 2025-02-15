from parsing import Parsing_Class
import json
import os
from elasticsearch import Elasticsearch

class Data_Handling(Parsing_Class):
    def __init__(self, site_dir, job_name, log_name, site, script_dir):
        super().__init__(site_dir, job_name, log_name, site)
        self.script_dir = script_dir
            
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
                        old_entries_list.append(lines.split("\n")[0])
                        # Converts lists into sets
            old_entries_set = set(old_entries_list)
            all_entries_set = set(list_of_jsons)
            # The difference in sets will be the new entries that will be sent
            new_entries_set = all_entries_set - old_entries_set
        else:
            print("FILE DOES NOT EXIST")
        return new_entries_set

    def sending_data_to_ES(self, list_of_jsons, new_entries_set):
        es = Elasticsearch(
                [{'host':"atlas-kibana.mwt2.org", 'port': 9200, 'scheme': "https"}],
                basic_auth=("username", "password")
                )
        try:
            response = es.info()
            success = True
        except Exception as e:
            success = False
            print(e)
        if success:
            for i in list_of_jsons:
                if i in new_entries_set:
                    es.index(
                        index="af_benchmarks",
                        document=i
                        )

    def append_new_data(self, old_entries, new_entries_set):
        with open(old_entries, 'a') as f:
            if f:
                for item in new_entries_set:
                    f.write(item + "\n")
            else:
                print("ERROR -- FILE WAS NOT OPENED")

