import data_handling as dh
import traceback

# Path to log files
path_to_logs = r"/sdf/home/s/selbor/benchmarks/"

# Job name
job_name = "TRUTH3_el9_container"

# Name of log file
log_file_name = "log.Derivation"

# AF site used
af_site = "slack"

# Directory where the parsing script is located
script_dir = r"/sdf/home/s/selbor/parsing_jobs"

# Txt file containing all the previously sent json instances
old_entries = "truth3_el_sent.txt"

# Txt file containing all the 'new' errors
error_file = "truth3_el_error.txt"

# Constructing the object with the Data_Handling Class
parsing = dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

# Path to benchmarks directory: /foo/bar/benchmarks/
benchmark_paths = parsing.benchmark_path()

# List containing full path: /foo/bar/benchmarks/DATETIME/JobName
full_path_list = parsing.full_path_function(benchmark_paths)


# List of dictionaries
list_dics = []

# For-loop block used to populate the list
for log_path in full_path_list:
    try:
        list_dics.append(
            parsing.parsing_truth3(
                log_path,
                os_used="el",
                container=True,
                batch=True,
                year_index=6,
                day_index=3,
                submit_time_index=4,
            )
        )
    except IndexError:
        list_dics.append(
            parsing.parsing_truth3_slac_e1(
                l, os_used="centos", container=True, batch=True
            )
        )
    except ValueError:
        list_dics.append(
            parsing.parsing_truth3_log_split(
                l, os_used="centos", container=True, batch=True
            )
        )

    except Exception:
        with open(error_file, "a") as f:
            f.write(log_path + "\n")
            f.write(traceback.format_exc())
            continue

# Constructs a list of json instances from the list of dictionaries
list_of_jsons = parsing.json_instances(list_dics)

# Creates a set of entries that are "new" by comparing with the set found in 'old_entries'
new_entries_set = parsing.bookkeeping_data(list_of_jsons, old_entries)

# Compares the new entries set with the list of json instances, if they match the instance gets sent to ES
parsing.sending_data_to_ES(list_of_jsons, new_entries_set)

# The new entries are appended onto the old_entries file
parsing.append_new_data(old_entries, new_entries_set)
