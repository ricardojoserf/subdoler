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


def print_rec(records, res):
	for r in records:
		val = r["domain"]
		print("- %s"%(r["domain"]))
		res.write(val+"\n")


def req_page(domain, api_token, page=1):
	response = requests.get("https://api.spyse.com/v1/subdomains?domain="+domain+"&api_token="+api_token+"&page="+page)
	json_data = json.loads(response.text)
	return json_data


def main():
	args = get_args()
	domains_file = args.domains_file
	domains = open(domains_file).read().splitlines()
	results_file = args.output_file
	api_token = args.api_token
	res = open(results_file, "a")
	subdomains_count = {}
	for d in domains:
		done = False
		page = 1
		val = str(d)
		print(val)
		res.write(val+"\n")
		while done is not True:
			try:
				data = req_page(d, api_token, str(page))
				print_rec(data["records"], res)
				subdomains_count[d]=data["count"]
				page += 1
				if data["count"] == 0 or data["count"] % 30 != 0:
					done = True
			except:
				done = True
				pass
	res.close()


main()