import os
import sys
import socket
import struct
import requests
from bs4 import BeautifulSoup

ipv4_base_url = "http://ipv4info.com"

def get_info_url(company_name):
	search_url = ipv4_base_url + "/?act=check&ip="+company_name
	response = requests.get(search_url)
	if response.history:
	    for resp in response.history:
	        return resp.headers['Location']
	else:
		print "Failed to get IPv4info page for that company"
		sys.exit(1)


def get_ranges(company_name):
	array_aux = [{'range': 32, 'val': 1}, {'range': 31, 'val': 2}, {'range': 30, 'val': 4}, {'range': 29, 'val': 8}, {'range': 28, 'val': 16}, {'range': 27, 'val': 32}, {'range': 26, 'val': 64}, {'range': 25, 'val': 128}, {'range': 24, 'val': 256}, {'range': 23, 'val': 512}, {'range': 22, 'val': 1024}, {'range': 21, 'val': 2048}, {'range': 20, 'val': 4096}, {'range': 19, 'val': 8192}, {'range': 18, 'val': 16384}, {'range': 17, 'val': 32768}, {'range': 16, 'val': 65536}, {'range': 15, 'val': 131072}, {'range': 14, 'val': 262144}, {'range': 13, 'val': 524288}, {'range': 12, 'val': 1048576}, {'range': 11, 'val': 2097152}, {'range': 10, 'val': 4194304}, {'range': 9, 'val': 8388608}, {'range': 8, 'val': 16777216}, {'range': 7, 'val': 33554432}, {'range': 6, 'val': 67108864}, {'range': 5, 'val': 134217728}, {'range': 4, 'val': 268435456}, {'range': 3, 'val': 536870912}, {'range': 2, 'val': 1073741824}, {'range': 1, 'val': 2147483648}]
	ranges = []
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
			print organization + ";" + block_name + ";" + first_ip + ";" + last_ip + ";" + range_size + ";" + asn + ";" + country + "; IPv4info"

	return ranges


get_ranges(sys.argv[1])
