import data_handling as dh
import traceback

# path to the log files directory
path_to_logs = r"/data/selbor/benchmarks/"

# name of the job
job_name = "Rucio"

# name of the log file
log_file_name = "rucio.log"

# cluster name
af_site = "uc"

# location of parsing script
script_dir = r"/data/selbor/parsing_jobs/"

# name of txt file containing all previously sent json instances
old_entries = "rucio_sent.txt"

# name of txt file containing the errors encountered while sending instances
error_file = "rucio_errors.txt"

# creating the parsing object
parsing = dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

# obtaining a list of paths $DATA/benchmarks/DateHour
benchmark_paths = parsing.benchmark_path()

# obtaining a list of paths $DATA/benchmarks/DateHour/JobName
full_path_list = parsing.full_path_function(benchmark_paths)

# initialize list that will contain dictionaries
list_dics = []

# for loop that will input paths int the respective parsing function
# if an error is encountered it will append message to error file and continue
for log_path in full_path_list:
    try:
        list_dics.append(parsing.parsing_rucio(log_path))
    except Exception:
        with open(error_file, "a") as f:
            f.write(log_path + "\n")
            f.write(traceback.format_exc())
            continue

# converting the dictionaries into json instances and storing in a list
list_of_jsons = parsing.json_instances(list_dics)

# compares the list of json instances with the list of old entries; stores in set
new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)

# matches the set element with the json list element and sends instance to ES
# FIXME: Have it just send the information without comparing; it already did that
# parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

# appends the sent instances to the list of old entries
# parsing.append_new_data(old_entries, new_entries_set)
