findsubdomain_token = ""
ipv4info_token = ""

tmp_folder = 				  "/tmp/"
amass_output_file 		  	= tmp_folder + "amass_temp"
ipv4info_output_file 	  	= tmp_folder + "ipv4info_temp"
findsubdomain_output_file 	= tmp_folder + "findsubdomain_temp"
dnsdumpster_output_file   	= tmp_folder + "dnsdumpster_temp"
gobuster_output_file   	  	= tmp_folder + "gobuster_temp"
fdns_output_file   	  		= tmp_folder + "fdns_temp"
merged_output_file			= tmp_folder + "merged"

ipv4info_script_file 		= "/root/subdoler/ipv4info.py"
findsubdomain_script_file 	= "/root/subdoler/findsub.py"
dnsdumpster_script_file 	= "/root/subdoler/API-dnsdumpster.com/api.py"
gobuster_dictionary 		= "/root/OSINT/gobuster/bitquark-subdomains-top100000.txt"
fdns_file 					= "fdns.json.gz"

gobuster_threads = 20
