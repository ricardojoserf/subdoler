import os

# File paths
program_path = os.getcwd() + "/"
apis_folder_path = program_path + "APIs/"
dnsdumpster_script_file = apis_folder_path + "API-dnsdumpster.com/api.py"
pwndb_script_file = apis_folder_path + "pwndb/pwndb.py"
harvester_location = apis_folder_path + "theHarvester/"
gobuster_file = apis_folder_path + "gobuster/gobuster"

# Subdomain Enumeration Setting
amass_active = True
gobuster_active = True
gobuster_dictionary = apis_folder_path + "bitquark-subdomains-top100000.txt"
gobuster_threads = 10
dnsdumpster_active = True
fdns_active = False
fdns_file = "/media/root/Seagate Expansion Drive/fdns.json.gz"
theharvester_active = True
pwndb_active = True
dig_timeout = 5
blacklist_words = "akamai,telefonica,microsoft"
tmux_session_name = "subdoler"

# Temporary files 
temp_domains_file =         "subdoler_temp_domains"
temp_ranges_file =          "subdoler_temp_ranges"
temp_companies_file =       "subdoler_temp_companies"
amass_output_file =         "subdoler_temp_amass"
dnsdumpster_output_file	=   "subdoler_temp_dnsdumpster"
gobuster_output_file =      "subdoler_temp_gobuster"
fdns_output_file =          "subdoler_temp_fdns"
pwndb_output_file =         "subdoler_temp_pwndb"
harvester_output_file =     "subdoler_temp_harvester"
tmuxp_yaml_file =           "subdoler_temp.yaml"
