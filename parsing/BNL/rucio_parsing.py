# I need to install ES here
import traceback
import data_handling as dh


path_to_logs = r"/usatlas/u/jroblesgo/benchmarks"

job_name = "Rucio"

log_file_name = "rucio.log"

af_site = "bnl"

script_dir = r"/usatlas/u/jroblesgo/"

old_entries = "rucio_sent.txt"

error_file = "rucio_error.txt"

parsing = dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

benchmark_paths = parsing.benchmark_path()

full_path_list = parsing.full_path_function(benchmark_paths)

list_dics = []

for log_path in full_path_list:
    try:
        list_dics.append(parsing.parsing_rucio(log_path))
    except Exception:
        with open(error_file, "a") as f:
            f.write(log_path + "n")
            f.write(traceback.format_exc())
            continue

list_of_jsons = parsing.json_instances(list_dics)

new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)

parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

parsing.append_new_data(old_entries, new_entries_set)
