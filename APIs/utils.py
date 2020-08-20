import os
import sys
import requests
from bs4 import BeautifulSoup
import distutils.spawn

ipv4_base_url = "http://ipv4info.com"


# Get url from IPv4info
def get_info_url(company_name):
	search_url = ipv4_base_url + "/?act=check&ip="+company_name
	response = requests.get(search_url)
	if response.history:
	    for resp in response.history:
	        return resp.headers['Location']
	else:
		print("Failed to get IPv4info page for that company")
		sys.exit(1)


# Get range in slash notation
def get_ranges(company_name):
	array_aux = [{'range': 32, 'val': 1}, {'range': 31, 'val': 2}, {'range': 30, 'val': 4}, {'range': 29, 'val': 8}, {'range': 28, 'val': 16}, {'range': 27, 'val': 32}, {'range': 26, 'val': 64}, {'range': 25, 'val': 128}, {'range': 24, 'val': 256}, {'range': 23, 'val': 512}, {'range': 22, 'val': 1024}, {'range': 21, 'val': 2048}, {'range': 20, 'val': 4096}, {'range': 19, 'val': 8192}, {'range': 18, 'val': 16384}, {'range': 17, 'val': 32768}, {'range': 16, 'val': 65536}, {'range': 15, 'val': 131072}, {'range': 14, 'val': 262144}, {'range': 13, 'val': 524288}, {'range': 12, 'val': 1048576}, {'range': 11, 'val': 2097152}, {'range': 10, 'val': 4194304}, {'range': 9, 'val': 8388608}, {'range': 8, 'val': 16777216}, {'range': 7, 'val': 33554432}, {'range': 6, 'val': 67108864}, {'range': 5, 'val': 134217728}, {'range': 4, 'val': 268435456}, {'range': 3, 'val': 536870912}, {'range': 2, 'val': 1073741824}, {'range': 1, 'val': 2147483648}]
	calc_ranges = []
	ranges_info =  []
	info_url = ipv4_base_url + get_info_url(company_name)
	r = requests.get(info_url)
	soup = BeautifulSoup(r.content, 'html.parser')
	for i in soup.findAll('tr'):
		vals = i.findAll('td')
		if len(vals) == 10:
			first_ip = vals[2].getText()
			last_ip  = vals[3].getText()
			range_size = vals[4].getText()
			asn = vals[6].getText().replace("\n", " ")
			block_name = vals[7].getText()
			organization = vals[8].getText()
			country = ""
			for e in vals[9].findAll('a'):
				country += e.getText() + " "
			ranges_info.append({'organization': organization, 'block_name': block_name, 'first_ip': first_ip, 'last_ip': last_ip, 'range_size': range_size, 'asn': asn, 'country': country})
			# Range translation to slash notation
			if "Size" not in range_size:
				for j in array_aux:
					if (int(range_size)-int(j['val'])) <=0:
						range_val = first_ip+"/"+str(j['range'])
						calc_ranges.append({'name':vals[8].getText(), 'range': range_val, 'country': country})
						ranges_info.append({'organization': organization, 'block_name': block_name, 'first_ip': first_ip, 'last_ip': last_ip, 'range_size': range_size, 'asn': asn, 'country': country, 'range': range_val})
						break		
	return calc_ranges, ranges_info


# Get base 
def get_base(val, index):
	base = 0
	for i in range(0, index):
		if (val - 2**(7-i)) >= 0:
			base += 2**(7-i)
			val -= 2**(7-i)
	return base


# IP resolution
def resolve_ip(ip_addr, output_file):
	comando = "a=$(nslookup " + ip_addr +" | grep name | awk '{print $4}'); if [ ${#a} -ge 1 ]; then echo "+ ip_addr +" - $a | sed -e 's/.$//'; echo $a | tr ' ' '\n' | sed -e 's/.$//' >> "+output_file+"; fi;"
	os.system(comando)	


# Subdomain ordering
def order_subdomains(output_file):
	f = open(output_file).read().splitlines()
	common_extensions = ["com","co","es","net","org","us"]
	possible_domains = []
	print("\n"+"-"*25+"\n"+"Domains list"+"\n"+"-"*25)
	for i in f:
		if len(i)>2:
			splitted = i.split(".")
			if splitted[len(splitted)-2] not in common_extensions:
				pd = splitted[len(splitted)-2]+"."+splitted[len(splitted)-1]
				if pd not in possible_domains:
					print("- "+ pd)
					possible_domains.append(pd)
			else:
				pd = splitted[len(splitted)-3]+"."+splitted[len(splitted)-2]+"."+splitted[len(splitted)-1]
				if pd not in possible_domains:
					print("- "+ pd)
					possible_domains.append(pd)

	print("\n"+"-"*25+"\n"+"Subdomains list"+"\n"+"-"*25)
	aux_arr = []
	for i in f:
		for p in possible_domains:
			if p in i:
				aux_arr.append({'dom':p,'subdom':i})
	for p in possible_domains:
		print("Domain "+ p)
		for i in aux_arr:
			if i['dom'] == p:
				print("- "+ i['subdom'])
	return f


# IP address analysis
# Source: https://medium.com/@sadatnazrul/checking-if-ipv4-address-in-network-python-af61a54d714d
def ip_to_binary(ip):
    octet_list_int = ip.split(".")
    octet_list_bin = [format(int(i), '08b') for i in octet_list_int]
    binary = ("").join(octet_list_bin)
    return binary


def get_addr_network(address, net_size):
    ip_bin = ip_to_binary(address)
    network = ip_bin[0:32-(32-net_size)]    
    return network


def ip_in_prefix(ip_address, prefix):
    [prefix_address, net_size] = prefix.split("/")
    net_size = int(net_size)
    prefix_network = get_addr_network(prefix_address, net_size)
    ip_network = get_addr_network(ip_address, net_size)
    return ip_network == prefix_network


# Binaries path calculation
def bin_path(name1, name2):
    if distutils.spawn.find_executable(name1) is not None:
    	return name1
    elif distutils.spawn.find_executable(name2) is not None:
    	return name2
    else:
    	return "notfound"


# Range Analysis
def analyze_range(arr_points, length_, output_file, counter, len_ranges):
	if length_ < 8:
		aux1 = 8 - length_
		first_ = get_base(int(arr_points[0]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = str(first_) + ".0.0.0"
		last_ip  = str(last_) + ".255.255.255"
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			for i in range(0,255):
				for h in range(0,255):
					for g in range(0,255):
						resolve_ip(str(j) + "." + str(i) + "." + str(h) + "." + str(g), output_file)
	elif length_ < 16:
		aux1 = 16 - length_
		first_ = get_base(int(arr_points[1]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + str(first_) + ".0.0"
		last_ip  = arr_points[0] + "." + str(last_) + ".255.255"
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			for i in range(0,255):
				for h in range(0,255):
					resolve_ip(arr_points[0]+"."+ str(j) + "." + str(i) + "." + str(h), output_file)
	elif length_ < 24:
		aux1 = 24 - length_
		first_ = get_base(int(arr_points[2]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + arr_points[1] + "." + str(first_) + ".0"
		last_ip  = arr_points[0] + "." + arr_points[1] + "." + str(last_) + ".255"
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			for i in range(0,255):
				resolve_ip(arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i), output_file)
	elif length_ < 32:
		aux1 = 32 - length_
		first_ = get_base(int(arr_points[3]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(first_)
		last_ip  = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(last_)
		print("\n"+"["+str(counter)+"/"+str(len_ranges)+"] "+"Range: "+first_ip+"-"+last_ip+"\n")
		for j in range(first_, last_):
			resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + str(j), output_file)
	elif length_ == 32:
		resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + arr_points[3], output_file)
	else:
		print("Wrong IP format")
		sys.exit(1)


# Range Processing and Calculation
def range_extractor(ranges_file, companies_file, output_file, country_filter):
	target_countries = None
	if country_filter is not None:
		target_countries = country_filter.split(",")
	ranges = []
	ranges_info = None
	if ranges_file is not None:
		ranges = open(ranges_file).read().splitlines()
	if companies_file is not None:
		companies = open(companies_file).read().splitlines()
		for c in companies:
			calc_ranges, ranges_info = get_ranges(c)
			print("\nCompany: "+c+"\n")
			for r in calc_ranges:
				print("- Range: %s   \tName: %s "%(r['range'], r['name']))
				# Check if the range is in the country filter -cf option
				if target_countries is not None:
					for c in target_countries:
						if c in r['country']:
							ranges.append(r['range'])
				# If there is no country filter option
				else:
					ranges.append(r['range'])
			if len(calc_ranges) == 0:
				print(" - No data found")
	counter = 0
	len_ranges = len(ranges)
	for r in ranges:
		counter += 1
		try:
			length_ = int(r.split("/")[1])
			arr_points = r.split("/")[0].split(".")
			analyze_range(arr_points, length_, output_file, counter, len_ranges)
		except:
			pass
	if os.path.isfile(output_file):
		order_subdomains(output_file)
	return output_file, ranges, ranges_info