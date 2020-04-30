import os

program_path =              os.getcwd() + "/"
apis_folder_path =          program_path + "APIs/"

# Subdomain Enumeration Setting
### Amass
amass_active                = True
### Gobuster
gobuster_active             = False
gobuster_dictionary =       apis_folder_path + "bitquark-subdomains-top100000.txt"
gobuster_threads =          10
### Finsubdomain - Token needed, get it from https://spyse.com/account/user
# findsubdomain_active        = False
# findsubdomain_token         = "-" 
### DNSDumpster
dnsdumpster_active          = False
# FDNS
fdns_active                 = False
fdns_file =                 "/media/root/Seagate Expansion Drive/fdns.json.gz"
### TheHarvester
theharvester_active         = False
### PwnDB
pwndb_active                = False
### Reverse DNS timeout (Dig)
dig_timeout     =           5

# Temporary files 
### They must contain the string 'temp'
#tmp_folder =                "/tmp/"
temp_domains_file =         "subdoler_temp_domains"
amass_output_file =         "subdoler_temp_amass"
#findsubdomain_output_file = "findsubdomain_temp"
dnsdumpster_output_file	=   "subdoler_temp_dnsdumpster"
gobuster_output_file =      "subdoler_temp_gobuster"
fdns_output_file =          "subdoler_temp_fdns"
pwndb_output_file =         "subdoler_temp_pwndb"
harvester_output_file =     "subdoler_temp_harvester"
#merged_output_file =        "merged_temp_"
tmuxp_yaml_file =           "subdoler_temp.yaml"

# File paths
#findsubdomain_script_file = apis_folder_path + "findsub.py"
dnsdumpster_script_file =   apis_folder_path + "API-dnsdumpster.com/api.py"
pwndb_script_file =         apis_folder_path + "pwndb/pwndb.py"
harvester_script_file =     apis_folder_path + "theHarvester/theHarvester.py"

