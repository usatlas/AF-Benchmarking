import parsing as pc
import data_handling as dh
import traceback

path_to_logs = r"/data/selbor/benchmarks/"

job_name = "Rucio"

log_file_name="rucio.log"

af_site = "uc"

script_dir=r"/data/selbor/parsing_jobs/"

old_entries="rucio_sent.txt"

parsing = dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

benchmark_paths = parsing.benchmark_path()

full_path_list = parsing.full_path_function(benchmark_paths)

list_dics = []

for l in full_path_list:
    try:
        list_dics.append(parsing.parsing_rucio(l))
    except IndexError:
        try:
            list_dics.append(parsing.parsing_rucio(l, 2, 14))
        except IndexError:
            list_dics.append(parsing.parsing_rucio_e1(l))
    except Exception as e:
        with open('rucio_errors.txt', 'a') as f:
            f.write(l + "\n")
            f.write(traceback.format_exc())
            continue

list_of_jsons = parsing.json_instances(list_dics)


new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)

parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

parsing.append_new_data(old_entries, new_entries_set)
