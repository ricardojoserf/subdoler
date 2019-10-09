import sys
import os
import subprocess
import argparse
import socket
import csv
import config


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
gobuster_dictionary         = config.gobuster_dictionary
fdns_file                   = config.fdns_file
gobuster_threads            = config.gobuster_threads
findsubdomain_token         = config.findsubdomain_token 
ipv4info_token              = config.ipv4info_token 
######################################################


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_file', required=True, action='store', help='Input file')
  parser.add_argument('-o', '--output_file', default="result.csv", required=False, action='store', help='Csv file')
  my_args = parser.parse_args()
  return my_args


def read_domains(domains_file):
	return open(domains_file).read().splitlines()


def create_commands(domains_file):
	amass_cmd = 		"amass enum --passive -d "+",".join(read_domains(domains_file))+" -o "+amass_output_file + "; echo "+"; echo Finished" #+ "; exit"
	findsubdomain_cmd = "python "+findsubdomain_script_file+" -f "+domains_file+" -a "+findsubdomain_token+" -o "+findsubdomain_output_file + "; echo "+"; echo Finished" #+ "; exit"
	ipv4info_cmd = 		"python "+ipv4info_script_file+" -f "+domains_file+" -a "+ipv4info_token+" -o "+ipv4info_output_file + "; echo "+"; echo Finished" #+ "; exit"
	dnsdumpster_cmd = 	"python "+dnsdumpster_script_file+" -f "+domains_file+" -o "+dnsdumpster_output_file + "; echo "+"; echo Finished" #+ "; exit"
	gobuster_cmd = ""
	domains = read_domains(domains_file)
	for d in range(0, len(domains)):
		domain = domains[d]
		gobuster_cmd += "echo; echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; echo; gobuster dns -t "+str(gobuster_threads)+" -w "+gobuster_dictionary+" -d "+domain+" -o "+gobuster_output_file+"_"+domain+"; "
	gobuster_cmd += " echo ; echo Finished" + "; exit"
	fdns_cmd = "zcat "+fdns_file+" | egrep '(" + "|".join(read_domains(domains_file)) + ")' | tee "+fdns_output_file #+ "; exit"
	#############
	comandos = []
	comandos.append({"titulo":"Borrando ficheros temporales", "comando":"touch /tmp/dummy_temp; ls /tmp/*_temp; rm /tmp/*_temp; exit", "active": True})
	comandos.append({"titulo":"Amass - Passive Scan Mode", "comando": amass_cmd, "active": True})
	comandos.append({"titulo":"Findsubdomain - Subdomains", "comando": findsubdomain_cmd, "active": False})
	comandos.append({"titulo":"IPv4info - Subdomains", "comando": ipv4info_cmd, "active": False})
	comandos.append({"titulo":"DNSDumpster - Subdomains", "comando": dnsdumpster_cmd, "active": False})
	comandos.append({"titulo":"Gobuster - Subdomain bruteforce", "comando": gobuster_cmd, "active": True})
	comandos.append({"titulo":"FDNS - Subdomain lister", "comando": fdns_cmd, "active": False})
	return comandos


def exec_commands(comandos):
	for i in comandos:
		if i["active"]:
			os.system('gnome-terminal -q -- bash -c "echo; echo {0}; echo; {1}; exec bash" 2>/dev/null'.format(i["titulo"],i["comando"]))


def join_files():
	os.system("cat /tmp/*_temp_* | sed -e 's/Found: //g' | sort -u > "+merged_output_file)


def generate_output(output_file):
	csv_arr = []
	subdoms = open(merged_output_file).read().splitlines()
	dom_arr = []
	print "\nNumber of subdomains: ", len(subdoms)
	print "------------------------"
	print "------ Subdomains ------"
	print "------------------------"
	for i in subdoms:
		print i
		try:
			ip_dominio =  subprocess.Popen(["dig", "+short", i], stdout=subprocess.PIPE).communicate()[0].replace("\n"," ")
		except:
			ip_dominio = ""
		if ip_dominio is not "":
			try:
				reverse_dns = subprocess.Popen(["dig", "+short", ip_dominio.split(" ")[0]], stdout=subprocess.PIPE).communicate()[0].replace("\n"," ")
			except:
				reverse_dns = ""
		else:
			reverse_dns = ""
		csv_line = [i,ip_dominio,reverse_dns]
		csv_arr.append(csv_line)
	print "------------------------"
	with open(output_file, 'wb') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		for row in csv_arr:
			wr.writerow(row)


def main():
	args = get_args()
	domains_file = args.input_file
	output_file = args.output_file
	comandos = create_commands(domains_file)
	exec_commands(comandos)
	raw_input("\nPress Enter to continue when everything is Finished...")
	join_files()
	generate_output(output_file)


if __name__== "__main__":
	main()