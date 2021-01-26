#!/usr/bin/python3
from APIs.utils import bin_path, ip_in_prefix, range_extractor
from config import *
from six.moves import input
import progressbar
import subprocess
import xlsxwriter
import argparse
import time
import sys
import csv
import six
import os


unique_subdomains = {}


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--companies_file', required=False, default=None, action='store', help='File with ranges to analyze')
	parser.add_argument('-C', '--companies_list', required=False, default=None, action='store', help='Comma separated list of companies')
	parser.add_argument('-d', '--domains_file', required=False, default=None, action='store', help='File with a list of domains')
	parser.add_argument('-D', '--domains_list', required=False, default=None, action='store', help='Comma separated list of domains')
	parser.add_argument('-r', '--ranges_file', required=False, default=None, action='store', help='File with ranges to analyze')
	parser.add_argument('-R', '--ranges_list', required=False, default=None, action='store', help='Comma separated list of ranges')
	parser.add_argument('-o', '--output_directory', required=False, default="res_subdoler", action='store', help='Output directory')
	parser.add_argument('-cf', '--country_filter', required=False, action='store', help='Country filter for the list of IP ranges calculated in IPv4info')
	parser.add_argument('-ns', '--no_subdomains', required=False, action='store_true', help='Do not list subdomains (just ranges and domains)')
	parser.add_argument('-p', '--process', required=False, action='store_true', help='Process files in the folder')
	parser.add_argument('-k', '--kill', required=False, action='store_true', help='Kill subdoler')	
	my_args = parser.parse_args()
	return my_args


def get_commands(domains_file, output_directory):
	python_bin = bin_path("python3", "python")
	if not os.path.isfile(domains_file):
		print("\n"+"No domains calculated. Exiting...")
		sys.exit(1)
	domains = open(domains_file).read().splitlines()
	amass_cmd =         "amass enum --passive -d "+",".join(domains)+" -o "+output_directory+"/"+amass_output_file + "; echo Finished"
	dnsdumpster_cmd =   python_bin+" "+dnsdumpster_script_file+" -f "+domains_file+" -o "+output_directory+"/"+dnsdumpster_output_file +"; echo Finished"
	fdns_cmd =          "zcat '"+fdns_file+"' | egrep '(" + "|\\.".join(domains) + ")' | cut -d ',' -f 2 | cut -d '\"' -f 4 | tee "+output_directory+"/"+fdns_output_file
	gobuster_cmd =      ""
	theharvester_cmd =  ""
	sublist3r_cmd =     ""
	pwndb_cmd =         "service tor start; "
	for d in range(0, len(domains)):
		domain = domains[d]
		gobuster_cmd       += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; "+gobuster_file+" dns -t "+str(gobuster_threads)+" -w "+gobuster_dictionary+" -d "+domain+" -o "+output_directory+"/"+gobuster_output_file+"_"+domain+"; "
		sublist3r_cmd      += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; " + python_bin + " " + sublist3r_file + " -d " + domain +" -o "+output_directory+"/"+sublist3r_output_file+"_"+domain+"; "
		current_location = os.getcwd() + "/"
		theharvester_cmd   += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; cd "+harvester_location+" && "+python_bin+" theHarvester.py -d " + domain + " -b google | grep -v cmartorella | grep '@' >> "+current_location+output_directory+"/"+harvester_output_file+"; "
		pwndb_cmd          += "echo "+str(d+1)+"/"+str(len(domains))+" "+domain+"; " + python_bin + " " + pwndb_script_file + " --target @" + domain + " | grep '@' | grep -v donate | awk '{print $2}' >> "+output_directory+"/"+pwndb_output_file+"; "
	gobuster_cmd     += "echo Finished"
	theharvester_cmd += "echo Finished"
	pwndb_cmd        += "echo Finished"
	sublist3r_cmd    += "echo Finished"
	commands = []
	commands.append({"title":"Amass - Passive Scan Mode", "command": amass_cmd, "active": amass_active})
	commands.append({"title":"DNSDumpster - Subdomains", "command": dnsdumpster_cmd, "active": dnsdumpster_active})
	commands.append({"title":"FDNS - Subdomain lister", "command": fdns_cmd, "active": fdns_active})
	commands.append({"title":"Gobuster - Subdomain bruteforce", "command": gobuster_cmd, "active": gobuster_active})
	commands.append({"title":"Sublist3r", "command": sublist3r_cmd, "active": sublist3r_active})
	commands.append({"title":"TheHarvester", "command": theharvester_cmd, "active": theharvester_active})
	commands.append({"title":"Pwndb", "command": pwndb_cmd, "active": pwndb_active})
	return commands


def create_tmux_file(commands, output_directory):
	os.system("tmux kill-session -t subdoler 2>/dev/null")
	f = open(output_directory+"/"+tmuxp_yaml_file,"w")
	f.write("session_name: "+tmux_session_name+"\n")
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


def create_tmux_session(output_directory):
	os.system("tmuxp load "+output_directory+""+tmuxp_yaml_file+";")


def write_ip_list(ip_list, workbook):
	worksheet = workbook.add_worksheet("Unique IP addresses")
	row = 0
	col = 0
	ip_list.sort()
	for ip in ip_list:
		worksheet.write(row, col, ip)
		row += 1


def check_ip(string_):
	import socket
	try:
	    socket.inet_aton(string_)
	    return True
	except socket.error:
	    return False


def dig_short(val_):
	try:
		calculated_ips =  subprocess.Popen(["dig", "+short", val_], stdout=subprocess.PIPE, encoding='utf8').communicate(timeout = dig_timeout)[0].replace("\n"," ").split(" ")
	except Exception as e:
		calculated_ips = ''
	if isinstance(calculated_ips, list):
		calculated_ips.remove('')
	if calculated_ips == []:
		calculated_ips = ''
	return calculated_ips


def get_range(calculated_ip, ranges):
	ip_in_range = ''
	if ranges is not None:
		for r in ranges:
			if ip_in_prefix(calculated_ip, r) is True:
				return r
	return ''


def write_to_files(worksheet, writer, row, col, data_array):
	writer.writerow(data_array)
	for i in data_array:
		worksheet.write(row, col, i)
		col += 1
	col = 0
	row += 1
	return worksheet, writer,row,col


def calculate_subdomain_info(output_directory, workbook, ranges, unique_subdomains):
	row = 0
	col = 0
	worksheet = workbook.add_worksheet("Subdomain by source")
	for i in ["Subdomain", "Source", "IP", "Reversed IP", "IP in range"]:
		worksheet.write(row, col, i)
		col += 1
	col = 0
	row += 1
	ip_list = []
	print("\nCalculating data from "+str(len(unique_subdomains))+" total entries")
	csv_file = open(output_directory+"subdomain_by_source.csv","w+") 
	writer = csv.writer(csv_file)
	writer.writerow(["Subdomain", "Source", "IP", "Reversed IP", "IP in range"])
	bar = progressbar.ProgressBar(maxval=len(unique_subdomains), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	bar_counter = 0
	for subdomain in unique_subdomains.keys():
		bar_counter += 1
		bar.update(bar_counter)
		calculated_ips = dig_short(subdomain)
		if calculated_ips == '':
			data_array = [subdomain, unique_subdomains[subdomain], '', '', '']
			worksheet,writer,row,col = write_to_files(worksheet, writer, row, col, data_array)
		else:
			for calculated_ip in calculated_ips:
				if (check_ip(calculated_ip)) and (calculated_ip not in ip_list):
						ip_list.append(calculated_ip)
				if calculated_ip == ";;":
					break
				reverse_dns = dig_short(calculated_ip)
				reverse_dns = ','.join(reverse_dns)
				ip_in_range = get_range(calculated_ip, ranges)
				data_array = [subdomain, unique_subdomains[subdomain], calculated_ip, reverse_dns, ip_in_range]
				worksheet,writer,row,col = write_to_files(worksheet, writer, row, col, data_array)
	bar.finish()
	return ip_list


def get_subdomain_info(res_files, workbook):
	for f in res_files:
		f_name = f['name']
		if os.path.isfile(f_name):
			file_values = open(f_name).read().splitlines()
			blacklist_words_list = blacklist_words.split(",")
			for bw in blacklist_words_list:
				for fv in file_values:
					if bw in fv:
						file_values.remove(fv)
						print ("Not analyzing %s, %s"%(fv,str(len(file_values))))
			file_values.sort()
			print("Calculating data from "+str(len(file_values))+" entries from "+f['code'])
			for v in file_values:
				if len(v) > 2:
					source_ = f['code']
					if v not in unique_subdomains.keys():
						unique_subdomains[v] = source_
					elif source_ not in unique_subdomains[v]:
						unique_subdomains[v] += ", " + source_
					else:
						pass
	return unique_subdomains


def get_unique_subdomains(output_dir, workbook):
	row = 0
	col = 0
	csv_file = open(output_dir+"unique_subdomains.txt","w+") 
	writer = csv.writer(csv_file)
	print("\n"+"-"*25+"\n"+"Subdomains (total: "+str(len(unique_subdomains))+")\n"+"-"*25)
	worksheet = workbook.add_worksheet("Unique subdomains")
	for u in sorted(unique_subdomains, key=unique_subdomains.get):
		print("- %s" % u)
		worksheet.write(row, col, u)
		writer.writerow([u])
		row += 1


def get_leaked_information(output_directory, workbook):
	csv_file = open(output_directory+"leaked_information.txt","w+") 
	writer = csv.writer(csv_file)
	print("\n"+"-"*25+"\n"+"Leaked information"+"\n"+"-"*25)
	worksheet = workbook.add_worksheet("Leaked emails (theHarvester)")
	row = 0
	col = 0
	if os.path.isfile(output_directory+"/"+harvester_output_file):
			print("\n"+"-"*25+"Leaked emails: "+"-"*25+"\n")
			file_values = open(output_directory+"/"+harvester_output_file).read().splitlines()
			file_values.sort()
			for v in file_values:
				print(v)
				worksheet.write(row, col, v)
				writer.writerow([v])
				row += 1
	worksheet = workbook.add_worksheet("Leaked credentials (Pwndb)")
	row = 0
	col = 0
	if os.path.isfile(output_directory+"/"+pwndb_output_file):
			print("\n"+"-"*25+"Leaked credentials: "+"-"*25+"\n")
			file_values = open(output_directory+"/"+pwndb_output_file).read().splitlines()
			file_values.sort()
			for v in file_values:
				print(v)
				worksheet.write(row, col, v)
				writer.writerow([v])
				row += 1


def get_range_info(output_directory, workbook, ranges_info):
	if ranges_info is not None:
		row = 0
		col = 0
		csv_file = open(output_directory+"/ranges_information.csv","w+") 
		writer = csv.writer(csv_file)
		worksheet = workbook.add_worksheet("Ranges information")
		heading = ["Organization", "Block name", "First IP", "Last IP", "Range size", "ASN", "Country"]
		writer.writerow(heading)
		for i in heading:
			worksheet.write(row, col, i)
			col += 1
		col = 0
		row += 1
		for r in ranges_info:
			file_values = [r['organization'], r['block_name'], r['first_ip'], r['last_ip'], r['range_size'], r['asn'], r['country']]
			if r['organization'] != "Organization":
				writer.writerow(file_values)
				for val in file_values:
					worksheet.write(row, col, val)
					col += 1
				col = 0
				row += 1


def get_domains(output_directory, workbook, domains_file):
	row = 0
	col = 0
	domains_ = open(domains_file).read().splitlines()
	domains_.sort()
	csv_file = open(output_directory+"main_domains.txt","w+")
	writer = csv.writer(csv_file)
	worksheet = workbook.add_worksheet("Main domains")
	print("-------------------------\nDomains (total: "+str(len(domains_))+")\n-------------------------")
	for d in domains_:
		if d != "":
			print("- %s" % d)
			worksheet.write(row, col, d)
			writer.writerow([d])
			row += 1
	print(" ")


def parse_files(output_directory,final_file):
	list_domains = []
	for f in os.listdir(output_directory):
		if f.startswith(final_file):
			file_values = open(output_directory+f).read().splitlines()
			for v in file_values:
				if "Found" in v:
					list_domains.append(v.split(" ")[1])
				else:
					list_domains.append(v)
		with open(output_directory+final_file, 'w') as txt_file:
			for dom in list_domains:
				txt_file.write(dom+ "\n")


def analyze(output_directory, ranges, ranges_info, domains_file, dont_list_subdomains):
	res_files = [{'name': output_directory+amass_output_file,'code':'Amass'},{'name': output_directory+dnsdumpster_output_file,'code':'DNSDumpster API'},{'name': output_directory+sublist3r_output_file,'code':'Sublist3r'},{'name': output_directory+gobuster_output_file,'code':'Gobuster'},{'name': output_directory+fdns_output_file,'code':'FDNS'}]
	workbook = xlsxwriter.Workbook(output_directory+"results.xlsx")
	# Main domains
	if domains_file is not None:
		get_domains(output_directory, workbook, domains_file)
	if not dont_list_subdomains:
		# Parse and join Gobuster and Sublist3r files
		parse_files(output_directory,gobuster_output_file)
		parse_files(output_directory,sublist3r_output_file)
		# Subdomains by source
		unique_subdomains = get_subdomain_info(res_files, workbook)
		# IP list
		ip_list = calculate_subdomain_info(output_directory, workbook, ranges, unique_subdomains)
		# Unique IP address
		write_ip_list(ip_list, workbook)
		# Unique subdomains
		get_unique_subdomains(output_directory, workbook)
		# Leaked information
		get_leaked_information(output_directory, workbook)
	# Range information
	get_range_info(output_directory, workbook, ranges_info)
	workbook.close()
	print ("\n"+"Cleaning temporary files...")
	clean_cmd = "touch "+output_directory+"subdoler_temp_; rm "+output_directory+"/*subdoler_temp_*;"
	os.system(clean_cmd)
	print("Done! Output saved in "+output_directory)


def print_banner():
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


def print_usage():
	print("Error: Domains, ranges or company file or comma separated list is necessary.")
	print("\nOne of these arguments is necessary:")
	print(" + -c: File of companies. Ex: ./subdoler.py -c /tmp/companies.txt")
	print(" + -C: List of companies. Ex: ./subdoler.py -C company1,company2")
	print(" + -r: File of IP ranges. Ex: ./subdoler.py -r /tmp/ip_ranges.txt")
	print(" + -R: List of IP ranges. Ex: ./subdoler.py -R 10.20.30.40/24,11.21.31.41/22")
	print(" + -d: File of domains.   Ex: ./subdoler.py -d /tmp/domains.txt")
	print(" + -D: List of domains.   Ex: ./subdoler.py -D company1.com,company2.es")
	print(" + -k: Kill tmux session. Ex: ./subdoler.py -k")
	print("\nOptional arguments:")
	print(" + -o:  Output directory. Ex: ./subdoler.py -c /tmp/companies.txt -o /tmp/subdoler_results")
	print(" + -cf: Country filter for IP range extraction from IPv4info. Ex: ./subdoler.py -c /tmp/companies.txt -cf ES,IT,US")
	print(" + -ns: No subdomain calculation. Ex: ./subdoler.py -r /tmp/ip_ranges.txt -ns")
	print(" + -p:  Process results (useful for closing everything except the tmux session and process the resulting files some hours later). Ex: ./subdoler.py -o /tmp/subdoler_results -p")
	print("")
	sys.exit(1)


def check_python_version():
	if not (sys.version_info > (3, 0)):
		print ("Sorry, Python 2 is not supported!")
		sys.exit(1)


def create_directory(output_directory):
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)


def create_file_from_list(list_, fname_, output_directory):
	values_ = list_.split(",")
	fname_ = output_directory+"/"+fname_
	with open(fname_, 'w') as f:
		for item in values_:
			f.write("%s\n" % item)
	return fname_


def delete_blacklisted_terms(output_directory, domains_file):
	# Delete domains with terms blacklisted in the config file (such as "akamai" or "telefonica")
	with open(domains_file, "r") as f:
		lines = f.readlines()
	blacklist_words_list = blacklist_words.split(",")
	dummy_domains_file = output_directory+"/"+temp_domains_file+"_dummy"
	with open(dummy_domains_file, "w") as f:
		for line in lines:
			detected = False
			for bw in blacklist_words_list:
				if bw in line:
					detected = True
			if not detected and len(line) > 2:
				f.write(line)
	os.rename(dummy_domains_file, domains_file)
	

def kill():
	os.system("tmux kill-session -t "+tmux_session_name)
	sys.exit(1)


def main():
	check_python_version()
	args = get_args()
	domains_file = args.domains_file
	ranges_file = args.ranges_file
	companies_file = args.companies_file
	dont_list_subdomains = args.no_subdomains
	process = args.process
	output_directory = args.output_directory
	output_directory = output_directory + "/" if not output_directory.endswith("/") else output_directory
	create_directory(output_directory)	
	kill_flag = args.kill
	if args.domains_list is not None:
		domains_file = create_file_from_list(args.domains_list, temp_domains_file, output_directory)
	if args.ranges_list is not None:
		ranges_file = create_file_from_list(args.ranges_list, temp_ranges_file, output_directory)
	if args.companies_list is not None:
		companies_file = create_file_from_list(args.companies_list, temp_companies_file, output_directory)
	# Print usage if there is not enough information
	if (domains_file is None) and (ranges_file is None) and (companies_file is None) and (process is False) and (kill_flag is False):
		print_usage()
	if kill_flag:
		kill()
	ranges = None
	ranges_info = None
	if not process:
		if domains_file is None:
			try:
				country_filter = args.country_filter
				domains_file, ranges, ranges_info = range_extractor(ranges_file, companies_file, (output_directory+"/"+temp_domains_file), country_filter)
				if len(ranges) >= 1:
					delete_blacklisted_terms(output_directory, domains_file)
			except Exception as e:
				print("There was an error, maybe too many connections to IPv4info? \nError %s"%(str(e)))
				sys.exit(1)
		if not dont_list_subdomains:
			commands = get_commands(domains_file, output_directory)
			create_tmux_file(commands, output_directory)
			create_tmux_session(output_directory)
			print("Options:\n\n - 'p': Process the files now\n - 'k': Kill the TMUX session \n - Other: Quit and process the results later with parameter '-p'\n")
			user_input = input("Press a key: ")
			if user_input == 'p' or user_input == 'P':
				print("\nAnalyzing files...\n")
				analyze(output_directory, ranges, ranges_info, domains_file, dont_list_subdomains)
			elif user_input == 'k' or user_input == 'K':
				print("\nKilling TMUX session...")
				kill()
			else:
				print("\nExiting...")
				sys.exit(1)
	else:
		analyze(output_directory, ranges, ranges_info, domains_file, dont_list_subdomains)


if __name__== "__main__":
	main()
