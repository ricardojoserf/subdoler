import sys
import os
import subprocess
import argparse
import xlsxwriter
import range_domains
import csv
from config import *
import utils
from six.moves import input
import six
import multiprocessing, time
import progressbar

unique_subdomains = []

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--domains_file', required=False, default=None, action='store', help='File with domains to analyze')
	parser.add_argument('-r', '--ranges_file', required=False, default=None, action='store', help='File with ranges to analyze')
	parser.add_argument('-c', '--companies_file', required=False, default=None, action='store', help='File with ranges to analyze')
	parser.add_argument('-o', '--output_directory', required=False, default="result.csv", action='store', help='Csv file')
	parser.add_argument('-t', '--type', required=False, default="tmux", action='store', help='Type of output (tmux/gnome-terminal)')
	my_args = parser.parse_args()
	return my_args


def create_commands(domains_file):
	python_bin = ""
	if six.PY2:
		python_bin = utils.bin_path("python2", "python")
	else:
		python_bin = utils.bin_path("python3", "python")
	if not os.path.isfile(domains_file):
		print("\n"+"No domains calculated. Exiting...")
		sys.exit(1)
	domains = open(domains_file).read().splitlines()
	amass_cmd =         "amass enum --passive -d "+",".join(domains)+" -o "+amass_output_file + "; echo Finished"
	findsubdomain_cmd = python_bin+" "+findsubdomain_script_file+" -f "+domains_file+" -a "+findsubdomain_token+" -o "+findsubdomain_output_file + "; echo Finished"
	ipv4info_cmd =      python_bin+" "+ipv4info_script_file+" -f "+domains_file+" -a "+ipv4info_token+" -o "+ipv4info_output_file +"; echo Finished"
	dnsdumpster_cmd =   python_bin+" "+dnsdumpster_script_file+" -f "+domains_file+" -o "+dnsdumpster_output_file +"; echo Finished"
	fdns_cmd =          "zcat '"+fdns_file+"' | egrep '(" + "|\\.".join(domains) + ")' | cut -d ',' -f 2 | cut -d '\"' -f 4 | tee "+fdns_output_file
	gobuster_cmd =      ""
	theharvester_cmd =  ""
	theharvester_binary = utils.bin_path("theHarvester","theharvester")
	pwndb_cmd =         "service tor start; "
	for d in range(0, len(domains)):
		domain = domains[d]
		gobuster_cmd       += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; gobuster dns -t "+str(gobuster_threads)+" -w "+gobuster_dictionary+" -d "+domain+" -o "+gobuster_output_file+"_"+domain+"; "
		if theharvester_binary != "notfound":
			theharvester_cmd   += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; "+theharvester_binary+" -d " + domain + " -b google | grep -v cmartorella | grep '@' >> "+harvester_output_file+"; "
		else:
			theharvester_cmd   += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; "+python_bin+" "+harvester_script_file+" -d " + domain + " -b google | grep -v cmartorella | grep '@' >> "+harvester_output_file+"; "
		pwndb_cmd          += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; " + python_bin +" "+ pwndb_script_file + " --target @" + domain + " | grep '@' | grep -v donate | awk '{print $2}' >> "+pwndb_output_file+"; "
	gobuster_cmd     += "echo Finished"
	theharvester_cmd += "echo Finished"
	pwndb_cmd        += "echo Finished"
	commands = []
	commands.append({"title":"Amass - Passive Scan Mode", "command": amass_cmd, "active": amass_active})
	if findsubdomain_token is not "" and findsubdomain_token is not "-":
		commands.append({"title":"Findsubdomain - Subdomains", "command": findsubdomain_cmd, "active": findsubdomain_active})
	if ipv4info_token is not "" and ipv4info_token is not "-":
		commands.append({"title":"IPv4info - Subdomains", "command": ipv4info_cmd, "active": ipv4info_active})
	commands.append({"title":"DNSDumpster - Subdomains", "command": dnsdumpster_cmd, "active": dnsdumpster_active})
	commands.append({"title":"FDNS - Subdomain lister", "command": fdns_cmd, "active": fdns_active})
	commands.append({"title":"Gobuster - Subdomain bruteforce", "command": gobuster_cmd, "active": gobuster_active})
	commands.append({"title":"TheHarvester", "command": theharvester_cmd, "active": theharvester_active})
	commands.append({"title":"Pwndb", "command": pwndb_cmd, "active": pwndb_active})
	return commands


def exec_commands(commands, type_):
	if type_ == "tmux":
		os.system("tmux kill-session -t subdoler 2>/dev/null")
		f = open(tmuxp_yaml_file,"w")
		f.write("session_name: subdoler"+"\n")
		f.write("windows:"+"\n")
		f.write("- window_name: dev window"+"\n")
		f.write("  layout: tiled"+"\n")
		f.write("  panes:"+"\n")
		for i in commands:
			if i["active"]:
				f.write('    - shell_command:\n    ')
				cmd_ = i["command"].replace(";", "\n        -")
				f.write('    - echo {0} \n'.format(i["title"]))
				f.write('        - {0} \n'.format(cmd_))
		tmux_cmd = "tmuxp load "+tmuxp_yaml_file
		tmux_gnome_cmd = 'gnome-terminal -- bash -c "echo; {0}; exec bash" 2>/dev/null'.format(tmux_cmd)
		os.system(tmux_gnome_cmd)
	else:
		for i in commands:
			if i["active"]:
				os.system('gnome-terminal -- bash -c "echo; echo {0}; echo; {1}; exec bash" 2>/dev/null'.format(i["title"],i["command"]))


def analyze(output_dir, ranges, ranges_info, domains_file):
	res_files = [{'name': domains_file,'code':'Dig (IP range)'},{'name': amass_output_file,'code':'Amass'},{'name': ipv4info_output_file,'code':'IPv4info API'},{'name': findsubdomain_output_file,'code':'Findsubdomain API'},{'name': dnsdumpster_output_file,'code':'DNSDumpster API'},{'name': gobuster_output_file,'code':'Gobuster'},{'name': fdns_output_file,'code':'FDNS'}]
	output_dir = output_dir + "/" if not output_dir.endswith("/") else output_dir
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)	
	workbook = xlsxwriter.Workbook(output_dir+"results.xlsx")
	# Subdomains by source
	worksheet = workbook.add_worksheet("Subdomain by source")
	row = 0
	col = 0
	for i in ["Subdomain", "Source", "IP", "Reversed IP", "IP in range"]:
		worksheet.write(row, col, i)
		col += 1
	col = 0
	row += 1
	csv_file = open(output_dir+"subdomain_by_source.csv","w+") 
	writer = csv.writer(csv_file)
	writer.writerow(["Subdomain", "Source", "IP", "Reversed IP", "IP in range"])
	for f in res_files:
		f_name = f['name']
		if os.path.isfile(f_name):
			file_values = open(f_name).read().splitlines()
			print("Calculating data from "+str(len(file_values))+" entries in "+f_name)
			#analyze_values(f, file_values, writer, worksheet, row, col)
			bar = progressbar.ProgressBar(maxval=len(file_values), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
			bar.start()
			bar_counter = 0
			for v in file_values:
				bar_counter += 1
				bar.update(bar_counter)
				if len(v) > 2:
					if f['name'] == 'Gobuster':
						v = v.split(" ")[2]
					if v not in unique_subdomains:
						unique_subdomains.append(v)
					try:
						if six.PY2:
							calculated_ips =  subprocess.Popen(["dig", "+short", v], stdout=subprocess.PIPE).communicate(timeout = dig_timeout)[0].replace("\n"," ").split(" ")
						else:
							calculated_ips =  subprocess.Popen(["dig", "+short", v], stdout=subprocess.PIPE, encoding='utf8').communicate(timeout = dig_timeout)[0].replace("\n"," ").split(" ")
					except Exception as e:
						#print(str(e))
						calculated_ips = ['']
					if calculated_ips == ['']:
						data_array = [v, f['code'], '', '', '']
						writer.writerow(data_array)
						for i in data_array:
							worksheet.write(row, col, i)
							col += 1
						col = 0
						row += 1
					else:
						for calculated_ip in calculated_ips:
							try:
								if calculated_ip == '' and len(calculated_ips) >= 2:
									break
								if calculated_ip == ";;":
									break
								try:
									if six.PY2:
										reverse_dns = subprocess.Popen(["dig", "+short", calculated_ip], stdout=subprocess.PIPE).communicate(timeout = dig_timeout)[0].replace("\n"," ") if calculated_ip != "" else ""
									else:
										reverse_dns = subprocess.Popen(["dig", "+short", calculated_ip], stdout=subprocess.PIPE, encoding='utf8').communicate(timeout = dig_timeout)[0].replace("\n"," ") if calculated_ip != "" else ""		
								except Exception as e:
									#print(str(e))
									reverse_dns = ''
								ip_in_range = ""
								if calculated_ip is not '' and ranges is not None:
									for r in ranges:
										if utils.ip_in_prefix(calculated_ip, r) is True:
											ip_in_range = r
											break
								data_array = [v, f['code'], calculated_ip, reverse_dns, ip_in_range]
								writer.writerow(data_array)
								for i in data_array:
									worksheet.write(row, col, i)
									col += 1
								col = 0
								row += 1
							except:
								pass
			bar.finish()

	# Unique subdomains
	csv_file = open(output_dir+"unique_subdomains.txt","w+") 
	writer = csv.writer(csv_file)
	print("\n"+"-"*25+"\n"+"Unique subdomains: "+str(len(unique_subdomains))+"\n"+"-"*25)
	worksheet = workbook.add_worksheet("Unique subdomains")
	row = 0
	col = 0
	for u in unique_subdomains:
		print("-"+u)
		worksheet.write(row, col, u)
		writer.writerow([u])
		row += 1
	# Leaked information
	csv_file = open(output_dir+"leaked_information.txt","w+") 
	writer = csv.writer(csv_file)
	worksheet = workbook.add_worksheet("Leaked information")
	row = 0
	col = 0
	leaked = []
	if os.path.isfile(harvester_output_file) or os.path.isfile(pwndb_output_file):
		print("\n"+"-"*25+"\n"+"Leaked information"+"\n"+"-"*25)
		if os.path.isfile(harvester_output_file):
			print("\n"+"-"*25+"Leaked emails: "+"-"*25+"\n")
			os.system("cat "+harvester_output_file+ " | grep -v cmartorella")
			file_values = open(harvester_output_file).read().splitlines()
			leaked.extend(file_values)
		if os.path.isfile(pwndb_output_file):
			print("\n"+"-"*25+"Leaked credentials: "+"-"*25+"\n")
			os.system("cat "+pwndb_output_file)
			file_values = open(pwndb_output_file).read().splitlines()
			leaked.extend(file_values)
	for l in leaked:
		if "cmartorella" in leaked:
			worksheet.write(row, col, l)
			writer.writerow([l])
			row += 1
	# Range information
	if ranges_info is not None:
		csv_file = open(output_dir+"ranges_information.csv","w+") 
		writer = csv.writer(csv_file)
		worksheet = workbook.add_worksheet("Ranges information")
		row = 0
		col = 0
		heading = ["Organization", "Block name", "First IP", "Last IP", "Range size", "ASN", "Country"]
		writer.writerow(heading)
		for i in heading:
			worksheet.write(row, col, i)
			col += 1
		col = 0
		row += 1
		for r in ranges_info:
			file_values = [r['organization'], r['block_name'], r['first_ip'], r['last_ip'], r['range_size'], r['asn'], r['country']]
			writer.writerow(file_values)
			for val in file_values:
				worksheet.write(row, col, val)
				col += 1
			col = 0
			row += 1
	##############################################################
	workbook.close()
	print ("\n"+"Cleaning temporary files...")
	os.system("touch /tmp/dummy_temp; rm /tmp/*_temp*;")
	print("Done! Output saved in "+output_dir)


def main():
	args = get_args()
	domains_file = args.domains_file
	output_directory = args.output_directory
	type_ = args.type
	ranges_file = args.ranges_file
	companies_file = args.companies_file
	print( "")
	print( " .d8888b.           888           888          888")
	print( "d88P  Y88b          888           888          888                  ")
	print( "Y88b.               888           888          888                  ")
	print( " *Y888b.   888  888 88888b.   .d88888  .d88b.  888  .d88b.  888d888 ")
	print( "    *Y88b. 888  888 888 *88b d88* 888 d88**88b 888 d8P  Y8b 888P")
	print( "      *888 888  888 888  888 888  888 888  888 888 88888888 888     ")
	print( "Y88b  d88P Y88b 888 888 d88P Y88b 888 Y88..88P 888 Y8b.     888     ")
	print( " *Y8888P*   *Y88888 88888P*   *Y88888  *Y88P*  888  *Y8888  888")
	print( "")
	print( "      -  A (hopefully) less painful way to list subdomains -      ")
	print( "")
	if domains_file is None and ranges_file is None and companies_file is None:
		print( "Error: Domains, ranges or company file is necessary")
		print( "usage: subdoler.py [-h] [-d DOMAINS_FILE] [-r RANGES_FILE] [-c COMPANIES_FILE] [-o OUTPUT_DIRECTORY] [-t TYPE]")
		sys.exit(1)
	ranges = None
	ranges_info = None
	if domains_file is None:
		if os.path.isfile(temp_domains_file):
			os.remove(temp_domains_file)
		try:
			domains_file, ranges, ranges_info = range_domains.range_extractor(ranges_file, companies_file, temp_domains_file)
		except:
			print("There was an error, maybe too many connections to IPv4info")
			sys.exit(1)
	commands = create_commands(domains_file)
	exec_commands(commands, type_)
	input("\n"+"Press 'Enter' to continue when everything has finished..."+"\n")
	analyze(output_directory, ranges, ranges_info, domains_file)


if __name__== "__main__":
	main()
