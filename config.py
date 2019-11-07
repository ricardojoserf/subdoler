# Options 
#amass_active                = False
amass_active                = True
#findsubdomain_active        = False
findsubdomain_active        = True
#ipv4info_active             = False
ipv4info_active             = True
#dnsdumpster_active          = False
dnsdumpster_active          = True
#fdns_active                 = False
fdns_active                 = True
#gobuster_active             = False
gobuster_active             = True
#theharvester_active         = False
theharvester_active         = True
#pwndb_active                = False
pwndb_active                = True
# Tokens
findsubdomain_token =       "-"
ipv4info_token =            "-"
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
gobuster_threads =          10
# FDNS
fdns_file =                 "fdns.json.gz"
#tmux
tmuxp_yaml_file = 			tmp_folder + "subolder_temp.yaml"
