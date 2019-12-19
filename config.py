import os

# Subdomain Enumeration Setting
### Amass
amass_active                = True
### Gobuster
gobuster_active             = True
gobuster_dictionary =       apis_folder_path + "bitquark-subdomains-top100000.txt"
gobuster_threads =          10
### Finsubdomain - Token needed, get it from https://spyse.com/account/user
findsubdomain_active        = False
findsubdomain_token         = "-" 
### DNSDumpster
dnsdumpster_active          = True
# FDNS
fdns_active                 = False
fdns_file =                 "/media/root/Seagate Expansion Drive/fdns.json.gz"
### TheHarvester
theharvester_active         = True
### PwnDB
pwndb_active                = True
### Reverse DNS timeout (Dig)
dig_timeout     =           5

# Temporary files 
### They must contain the string 'temp'
tmp_folder =                "/tmp/"
temp_domains_file =         tmp_folder + "domains_temp"
amass_output_file =         tmp_folder + "amass_temp"
findsubdomain_output_file = tmp_folder + "findsubdomain_temp"
dnsdumpster_output_file	=   tmp_folder + "dnsdumpster_temp"
gobuster_output_file =      tmp_folder + "gobuster_temp"
fdns_output_file =          tmp_folder + "fdns_temp"
pwndb_output_file =         tmp_folder + "pwndb_temp"
harvester_output_file =     tmp_folder + "harvester_temp"
merged_output_file =        tmp_folder + "merged_temp"
tmuxp_yaml_file =           tmp_folder + "subdoler_temp.yaml"

# File paths
program_path =              os.getcwd() + "/"
apis_folder_path =          program_path + "APIs/"
findsubdomain_script_file = apis_folder_path + "findsub.py"
dnsdumpster_script_file =   apis_folder_path + "API-dnsdumpster.com/api.py"
pwndb_script_file =         apis_folder_path + "pwndb/pwndb.py"
harvester_script_file =     apis_folder_path + "theHarvester/theHarvester.py"

