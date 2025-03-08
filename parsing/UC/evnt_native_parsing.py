import data_handling as dh
import traceback

path_to_logs=r'/data/selbor/benchmarks/'

job_name="EVNT"

log_file_name="log.generate"

af_site="uc"

parsing_dir="/data/selbor/parsing_jobs/"

old_entries="evnt_native_sent.txt"

parsing=dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, parsing_dir)

benchmark_paths = parsing.benchmark_path()

full_path_list = parsing.full_path_function(benchmark_paths)

list_dics=[]
for l in full_path_list:
    try:
        list_dics.append(parsing.parsing_evnt(l, batch=True))
    except Exception as e:
        with open('evnt_native_errors.txt', 'a') as f:
            f.write(l + "\n")
            f.write(traceback.format_exc())
        continue


list_of_jsons = parsing.json_instances(list_dics)


new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)


parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

parsing.append_new_data(old_entries, new_entries_set)
