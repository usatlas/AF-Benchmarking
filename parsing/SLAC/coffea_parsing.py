import data_handling as dh
import traceback

# Path to log files
path_to_logs=r'/sdf/home/s/selbor/benchmarks/'

# Job name
job_name = 'Coffea_Hist'

# Name of log file
log_file_name='coffea_hist.log'

# AF site used
af_site ='slac' 

# Directory where the parsing script is located
script_dir=r'/sdf/home/s/selbor/parsing_jobs'

# Txt file containing all the previously sent json instances
old_entries="coffea_sent.txt"

# Txt file containing all the 'new' errors
error_file='coffea_error.txt'

# Constructing the object with the Data_Handling Class
parsing = dh.Data_Handling(path_to_logs, job_name, log_file_name, af_site, script_dir)

# Path to benchmarks directory: /foo/bar/benchmarks/
benchmark_paths = parsing.benchmark_path()

# List containing full path: /foo/bar/benchmarks/DATETIME/JobName
full_path_list = parsing.full_path_function(benchmark_paths)


# List of dictionaries
list_dics=[]

# For-loop block used to populate the list
for l in full_path_list:
    try:
        list_dics.append(parsing.parsing_ntuple_c(l, fli=0))
    except IndexError:
        list_dics.append(parsing.parsing_ntuple_c(l, fli=11))
    except ValueError:
        try:
            list_dics.append(parsing.parsing_ntuple_c(l, fli=11))
        except ValueError:
            try:
                #print(l)
                list_dics.append(parsing.parsing_ntuple_c_e2(l))
            except ValueError:
                list_dics.append(parsing.parsing_ntuple_c_e3(l))
        except IndexError:
            list_dics.append(parsing.parsing_ntuple_c_e1(l))
    except Exception as e:
        with open(error_file, 'a') as f:
            f.write(l + "\n")
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
