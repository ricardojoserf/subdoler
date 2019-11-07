import argparse
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
import base64
import sys


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--domains_file', required=True, action='store', help='Domains file')
  parser.add_argument('-o', '--output_file', required=True, action='store', help='Output file')
  my_args = parser.parse_args()
  return my_args


def main():
  args = get_args()
  results_file = args.output_file
  res_file = open(results_file, "a")
  domains = open(args.domains_file).read().splitlines()
  for d in domains:
    res = DNSDumpsterAPI(True).search(d)
    if len(res) > 1:
      try:
        for entry in res['dns_records']['host']:
              if entry['reverse_dns']:
                val = ("{domain}".format(**entry))
                res_file.write(val+"\n")
      except:
        pass


main()

