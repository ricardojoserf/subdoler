import os

# Subdomains enumeration options 
amass_active                = True
gobuster_active             = True
findsubdomain_active        = False
# Get the token in https://spyse.com/account/user
findsubdomain_token         = "-"
ipv4info_active             = False
ipv4info_token              = "-"
dnsdumpster_active          = True
fdns_active                 = False
# Leaks
theharvester_active         = True
pwndb_active                = True

# Temp files
tmp_folder =                "/tmp/"
temp_domains_file =         tmp_folder + "domains_temp"
amass_output_file =         tmp_folder + "amass_temp"
ipv4info_output_file  =     tmp_folder + "ipv4info_temp"
findsubdomain_output_file = tmp_folder + "findsubdomain_temp"
dnsdumpster_output_file	=   tmp_folder + "dnsdumpster_temp"
gobuster_output_file =      tmp_folder + "gobuster_temp"
fdns_output_file =          tmp_folder + "fdns_temp"
pwndb_output_file =         tmp_folder + "pwndb_temp"
harvester_output_file =     tmp_folder + "harvester_temp"
merged_output_file =        tmp_folder + "merged_temp"

# File paths
program_path =              os.getcwd() + "/"
apis_folder_path =          program_path + "APIs/"
ipv4info_script_file =      apis_folder_path + "ipv4info.py"
findsubdomain_script_file = apis_folder_path + "findsub.py"
dnsdumpster_script_file =   apis_folder_path + "API-dnsdumpster.com/api.py"
pwndb_script_file =         apis_folder_path + "pwndb/pwndb.py"
harvester_script_file =     apis_folder_path + "theHarvester/theHarvester.py"

# Gobuster
gobuster_dictionary =       apis_folder_path + "bitquark-subdomains-top100000.txt"
gobuster_threads =          50
# FDNS
fdns_file =                 "/media/root/Seagate Expansion Drive/fdns.json.gz"
#tmux
tmuxp_yaml_file =           tmp_folder + "subdoler_temp.yaml"
#dig
dig_timeout     =           5
dig_threads     =           3
