import json
import sys
import requests
import argparse


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--domains_file', required=True, action='store', help='Domains file')
  parser.add_argument('-o', '--output_file', required=True, action='store', help='Output file')
  parser.add_argument('-a', '--api_token', required=False, action='store', help='API token')
  my_args = parser.parse_args()
  return my_args


def print_rec(records):
	for r in records:
		'''
		try:
			val = "SUBDOMAIN: \t"+r["domain"]+"   \t\t"+r["ip"]["ip"]
		except:
			val = "SUBDOMAIN: \t"+r["domain"]
		'''
		#val = "SUBDOMAIN: \t"+r["domain"]
		val = r["domain"]
		print(val)
		res.write(val+"\n")


def req_page(domain, api_token, page=1):
	response = requests.get("https://api.spyse.com/v1/subdomains?domain="+domain+"&api_token="+api_token+"&page="+page)
	json_data = json.loads(response.text)
	return json_data


def subd_analisis(subdomains_count):
	print("\n"*3 + "Subdominios por dominio" + "\n"*3)
	for key, value in sorted(subdomains_count.items(), key=lambda x: int(x[1])):
		if int(value) > 1:
			print("%s: %s" % (key, value))

args = get_args()
domains_file = args.domains_file # "dominios.txt"
domains = open(domains_file).read().splitlines()
results_file = args.output_file # "results.txt"
api_token = args.api_token

res = open(results_file, "a")
subdomains_count = {}

for d in domains:
	done = False
	page = 1
	#val = "DOMAIN:    \t"+str(d)
	val = str(d)
	print(val)
	res.write(val+"\n")
	while done is not True:
		data = req_page(d, api_token, str(page))
		try:
			## print "DOMAIN:    \t"+str(d)+"\t\t\t\t"+"  Page "+str(data["page"])+" with "+str(data["count"])+"/"+str(data["per_page"])
			print_rec(data["records"])
			subdomains_count[d]=data["count"]
			page += 1
			if data["count"] == 0 or data["count"] % 30 != 0:
				done = True
		except:
			## print "DOMAIN:    \t"+str(d) #+"\t\t\t\t"+"(Data: null)"
			done = True
			pass

res.close()
subd_analisis(subdomains_count)

