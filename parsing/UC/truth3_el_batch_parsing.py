import data_handling as dh
import traceback

path_to_logs = r"/data/selbor/benchmarks/"

job_name = "TRUTH3_el9_container"

log_file_name = "log.Derivation"

af_site = "uc"

script_dir = "/data/selbor/parsing_jobs/"

old_entries = "truth3_el9_batch_sent.txt"

parsing = dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

benchmark_paths = parsing.benchmark_path()

full_path_list = parsing.full_path_function(benchmark_paths)

list_dics = []
for log_path in full_path_list:
    try:
        list_dics.append(parsing.parsing_truth3_batch(l))
    except FileNotFoundError:
        try:
            list_dics.append(parsing.string_and_split(log_path))
        except FileNotFoundError:
            continue
    except Exception:
        with open("truth3_el_batch_errors.txt", "a") as f:
            f.write(log_path + "\n")
            f.write(traceback.format_exc())
            continue

list_of_jsons = parsing.json_instances(list_dics)

new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)

parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

parsing.append_new_data(old_entries, new_entries_set)
