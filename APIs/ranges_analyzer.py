import os
import sys
import socket
import struct
import requests
from bs4 import BeautifulSoup

ipv4_base_url = "http://ipv4info.com"

def get_info_url(range):
	search_url = ipv4_base_url + "/?act=check&ip="+range
	response = requests.get(search_url)
	if response.history:
	    for resp in response.history:
	        return resp.headers['Location']
	else:
		print "Failed to get IPv4info page for that company"
		sys.exit(1)


def get_range_info(company_name):
	ranges = []
	ranges_info =  []
	info_url = ipv4_base_url + get_info_url(company_name)
	r = requests.get(info_url)
	soup = BeautifulSoup(r.content, 'html.parser')
	info = {}
	for i in soup.findAll('tr'):
		vals = i.findAll('td')
		if len(vals) == 2:
			info[ vals[0].getText().encode('ascii','ignore') ] = vals[1].getText().replace("\n", "").replace("\t", "").encode('utf-8')
	print info['Organization'],";",info['Block name'],";",info['Block start'],";",info['End of block'],";",info['Block size'],";",info['AS number'],";",info['Country']


input_file = sys.argv[1]
ranges = open(input_file).read().splitlines()

for r in ranges:
	r = r.split("/")[0]
	get_range_info(r)
