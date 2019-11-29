import sys
import os
import subprocess
import argparse
import socket
import csv
import config
import time
import csv


################ Configuration file ##################
tmp_folder                  = config.tmp_folder
amass_output_file           = config.amass_output_file
ipv4info_output_file        = config.ipv4info_output_file
findsubdomain_output_file   = config.findsubdomain_output_file
dnsdumpster_output_file     = config.dnsdumpster_output_file
gobuster_output_file        = config.gobuster_output_file
fdns_output_file            = config.fdns_output_file
merged_output_file          = config.merged_output_file
ipv4info_script_file        = config.ipv4info_script_file
findsubdomain_script_file   = config.findsubdomain_script_file
dnsdumpster_script_file     = config.dnsdumpster_script_file
pwndb_script_file           = config.pwndb_script_file
gobuster_dictionary         = config.gobuster_dictionary
fdns_file                   = config.fdns_file
gobuster_threads            = config.gobuster_threads
findsubdomain_token         = config.findsubdomain_token 
ipv4info_token              = config.ipv4info_token 
amass_active                = config.amass_active
findsubdomain_active        = config.findsubdomain_active 
ipv4info_active             = config.ipv4info_active
dnsdumpster_active          = config.dnsdumpster_active
fdns_active                 = config.fdns_active
gobuster_active             = config.gobuster_active
theharvester_active         = config.theharvester_active
pwndb_active                = config.pwndb_active
tmuxp_yaml_file 	    = config.tmuxp_yaml_file


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_file', required=True, action='store', help='Input file')
	parser.add_argument('-o', '--output_file', default="result.csv", required=False, action='store', help='Csv file')
	parser.add_argument('-t', '--type', required=False, default="terminal", action='store', help='Type of output (gnome-terminal/tmux)')
	my_args = parser.parse_args()
	return my_args


def read_domains(domains_file):
	return open(domains_file).read().splitlines()


def create_commands(domains_file):
	amass_cmd =         "amass enum --passive -d "+",".join(read_domains(domains_file))+" -o "+amass_output_file + "; echo Finished" #+ "; exit"
	findsubdomain_cmd = "python "+findsubdomain_script_file+" -f "+domains_file+" -a "+findsubdomain_token+" -o "+findsubdomain_output_file + "; echo Finished" #+ "; exit"
	ipv4info_cmd =      "python "+ipv4info_script_file+" -f "+domains_file+" -a "+ipv4info_token+" -o "+ipv4info_output_file +"; echo Finished" #+ "; exit"
	dnsdumpster_cmd =   "python "+dnsdumpster_script_file+" -f "+domains_file+" -o "+dnsdumpster_output_file +"; echo Finished" #+ "; exit"
	fdns_cmd =          "zcat '"+fdns_file+"' | egrep '(" + "|\\.".join(read_domains(domains_file)) + ")' | cut -d ',' -f 2 | cut -d '\"' -f 4 | tee "+fdns_output_file  #+ "; exit"
	gobuster_cmd =      ""
	theharvester_cmd =  ""
	pwndb_cmd =         "service tor start; "
	domains = read_domains(domains_file)
	for d in range(0, len(domains)):
		domain = domains[d]
		gobuster_cmd       += "echo; echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; echo; gobuster dns -t "+str(gobuster_threads)+" -w "+gobuster_dictionary+" -d "+domain+" -o "+gobuster_output_file+"_"+domain+"; "
		theharvester_cmd   += "echo; echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; echo; theHarvester -d " + domain + " -b google; " # -b baidu,censys,crtsh,dogpile,google,linkedin,netcraft,pgp,threatcrowd,twitter,vhost,yahoo
		pwndb_cmd          += "echo; echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; echo; python " + pwndb_script_file + " --target @" + domain + "; "
	gobuster_cmd     += "echo Finished" #+ "; exit"
	theharvester_cmd += "echo Finished" #+ "; exit"
	pwndb_cmd        += "echo Finished" #+ "; exit"
	comandos = []
	comandos.append({"titulo":"Borrando ficheros temporales", "comando":"touch /tmp/dummy_temp; ls /tmp/*_temp*; rm /tmp/*_temp*; echo 'Finished'", "active": True})
	comandos.append({"titulo":"Amass - Passive Scan Mode", "comando": amass_cmd, "active": amass_active})
	comandos.append({"titulo":"Findsubdomain - Subdomains", "comando": findsubdomain_cmd, "active": findsubdomain_active})
	comandos.append({"titulo":"IPv4info - Subdomains", "comando": ipv4info_cmd, "active": ipv4info_active})
	comandos.append({"titulo":"DNSDumpster - Subdomains", "comando": dnsdumpster_cmd, "active": dnsdumpster_active})
	comandos.append({"titulo":"FDNS - Subdomain lister", "comando": fdns_cmd, "active": fdns_active})
	comandos.append({"titulo":"Gobuster - Subdomain bruteforce", "comando": gobuster_cmd, "active": gobuster_active})
	comandos.append({"titulo":"TheHarvester", "comando": theharvester_cmd, "active": theharvester_active})
	comandos.append({"titulo":"Pwndb", "comando": pwndb_cmd, "active": pwndb_active})
	return comandos


def exec_commands(comandos, type_):
	if type_ == "tmux":
		#print (time.strftime("%H-%M-%S"))
		os.system("tmux kill-session -t subdoler 2>/dev/null")
		f = open(tmuxp_yaml_file,"w")
		f.write("session_name: subdoler\n")
		f.write("windows:\n")
		f.write("- window_name: dev window\n")
		f.write("  layout: tiled\n")
		f.write("  panes:\n")
		for i in comandos:
			if i["active"]:
				f.write('    - shell_command:\n    ')
				cmd_ = i["comando"].replace(";", "\n        -")
				f.write('    - echo {0} \n'.format(i["titulo"]))
				f.write('        - {0} \n'.format(cmd_))
		tmux_cmd = "tmuxp load "+tmuxp_yaml_file
		os.system('gnome-terminal -q -- bash -c "echo; {0}; exec bash" 2>/dev/null'.format(tmux_cmd))
	else:
		for i in comandos:
			if i["active"]:
				os.system('gnome-terminal -q -- bash -c "echo; echo {0}; echo; {1}; exec bash" 2>/dev/null'.format(i["titulo"],i["comando"]))


def join_files(output_file):
	#command = "cat /tmp/*_temp* | sed -e 's/Found: //g' | sort -u > "+merged_output_file
	#os.system(command)
	
	res_files = [{'name': amass_output_file,'code':'Amass'},{'name': ipv4info_output_file,'code':'IPv4info API'},{'name': findsubdomain_output_file,'code':'Findsubdomain API'},{'name': dnsdumpster_output_file,'code':'DNSDumpster API'},{'name': gobuster_output_file,'code':'Gobuster'},{'name': fdns_output_file,'code':'FDNS'}]
	
	unique_subdomains = []
	with open(output_file,"w+") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["Subdomain", "Source", "IP", "Reversed IP"])
		for f in res_files:
			if os.path.isfile(f['name']):
				file_values = open(f['name']).read().splitlines()
				for v in file_values:
					print "v", v
					if f['code'] == 'Gobuster':
						v = v.split(" ")[2]
					if v not in unique_subdomains:
							unique_subdomains.append(f)
					try:
						calculated_ip =  subprocess.Popen(["dig", "+short", v], stdout=subprocess.PIPE).communicate()[0].replace("\n"," ")
					except:
						calculated_ip = ""
					try:
						reverse_dns = subprocess.Popen(["dig", "+short", calculated_ip.split(" ")[0]], stdout=subprocess.PIPE).communicate()[0].replace("\n"," ")
					except:
						reverse_dns = ""
					writer.writerow([v, f['code'], calculated_ip, reverse_dns])
					

def main():
	args = get_args()
	domains_file = args.input_file
	output_file = args.output_file
	type_ = args.type
	comandos = create_commands(domains_file)
	exec_commands(comandos, type_)
	print ""
	print " .d8888b.           888           888          888"
	print "d88P  Y88b          888           888          888                  "
	print "Y88b.               888           888          888                  "
	print " *Y888b.   888  888 88888b.   .d88888  .d88b.  888  .d88b.  888d888 "
	print "    *Y88b. 888  888 888 *88b d88* 888 d88**88b 888 d8P  Y8b 888P"
	print "      *888 888  888 888  888 888  888 888  888 888 88888888 888     "
	print "Y88b  d88P Y88b 888 888 d88P Y88b 888 Y88..88P 888 Y8b.     888     "
	print " *Y8888P*   *Y88888 88888P*   *Y88888  *Y88P*  888  *Y8888  888"
	print ""
	print "      -  A (hopefully) less painful way to list subdomains -      "
	print ""
	raw_input("\nPress Enter to continue when every terminal has 'Finished'...")
	join_files(output_file)
	#generate_output(output_file)


if __name__== "__main__":
	main()
