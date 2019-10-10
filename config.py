# Tokens
findsubdomain_token =       ""
ipv4info_token =            ""
# Temp files
tmp_folder =                "/tmp/"
amass_output_file =         tmp_folder + "amass_temp"
ipv4info_output_file  =     tmp_folder + "ipv4info_temp"
findsubdomain_output_file = tmp_folder + "findsubdomain_temp"
dnsdumpster_output_file	=   tmp_folder + "dnsdumpster_temp"
gobuster_output_file =      tmp_folder + "gobuster_temp"
fdns_output_file =          tmp_folder + "fdns_temp"
merged_output_file =        tmp_folder + "merged_temp"
# File paths
program_path =              "/root/subdoler/"
apis_folder_path =          program_path + "APIs/"
ipv4info_script_file =      apis_folder_path + "ipv4info.py"
findsubdomain_script_file = apis_folder_path + "findsub.py"
dnsdumpster_script_file =   apis_folder_path + "API-dnsdumpster.com/api.py"
pwndb_script_file =         apis_folder_path + "pwndb/pwndb.py"
# Gobuster
gobuster_dictionary =       apis_folder_path + "bitquark-subdomains-top100000.txt"
gobuster_threads =          20
# FDNS
fdns_file =                 "fdns.json.gz"
