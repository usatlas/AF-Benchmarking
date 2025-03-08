import parsing as pc
import data_handling as dh
import traceback

path_to_logs=r'/data/selbor/benchmarks'

job_name="TRUTH3_interactive"

log_file_name="log.Derivation"

af_site="uc"

script_dir=r'/data/selbor/parsing_jobs/'

old_entries="truth3_native_interactive_sent.txt"

parsing=dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

benchmark_paths = parsing.benchmark_path()

full_path_list = parsing.full_path_function(benchmark_paths)

list_dics = []

for l in full_path_list:
    try:
        list_dics.append(parsing.parsing_truth3(l, batch=True))
    except IndexError:
        try:
            list_dics.append(parsing.parsing_truth3(l, batch=True, year_index=6, day_index=3, submit_time_index=4))
        except IndexError:
            list_dics.append(parsing.parsing_truth3_e1(l, os_used="native", batch=False))
        except ValueError:
            list_dics.append(parsing.parsing_truth3_log_split(l, os_used="native", batch=False))
    except ValueError:
        list_dics.append(parsing.parsing_truth3_log_split(l, os_used="native", batch=False))
    except FileNotFoundError:
        pass
    except Exception as e:
        with open('truth3_native_interactive_errors.txt', 'a') as f:
            f.write(l + "\n")
            f.write(traceback.format_exc())
            continue

list_of_jsons = parsing.json_instances(list_dics)

new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)

parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

parsing.append_new_data(old_entries, new_entries_set)
