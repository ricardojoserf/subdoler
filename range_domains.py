import sys
import os
import argparse


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_file', required=True, action='store', help='Input file')
  parser.add_argument('-o', '--output_file', default="results", required=False, action='store', help='Output folder')
  my_args = parser.parse_args()
  return my_args


def read_lines(domains_file):
	return open(domains_file).read().splitlines()


def get_base(val, index):
	base = 0
	for i in range(0, index):
		if (val - 2**(7-i)) >= 0:
			base += 2**(7-i)
			val -= 2**(7-i)
	return base


def resolve_ip(ip_addr, output_file):
	comando = "a=$(nslookup " + ip_addr +" | grep name | awk '{print $4}'); if [ ${#a} -ge 1 ]; then echo "+ ip_addr +" - $a | sed -e 's/.$//'; echo $a | tr ' ' '\n' | sed -e 's/.$//' >> "+output_file+"; fi;"
	os.system(comando)	


def create_command(arr_points, length_, output_file):
	final_cmd = ""
	if length_ < 8:
		aux1 = 8 - length_
		first_ = get_base(int(arr_points[0]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = str(first_) + ".0.0.0"
		last_ip  = str(last_) + ".255.255.255"
		print "\n[debug] Range: "+first_ip+"-"+last_ip
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
		print "\n[debug] Range: "+first_ip+"-"+last_ip
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
		print "\n[debug] Range: "+first_ip+"-"+last_ip
		for j in range(first_, last_):
			for i in range(0,255):
				resolve_ip(arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i), output_file)
	elif length_ < 32:
		aux1 = 32 - length_
		first_ = get_base(int(arr_points[3]), int(8 - aux1))
		last_ = first_ + 2**aux1 - 1
		first_ip = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(first_)
		last_ip  = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(last_)
		print "\n[debug] Range: "+first_ip+"-"+last_ip
		for j in range(first_, last_):
			resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + str(j), output_file)
	elif length_ == 32:
		resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + arr_points[3], output_file)
	else:
		print "Wrong IP format"
		sys.exit(1)


def extract_domains(output_file):
	subdoms = open(output_file).read().splitlines()
	dom_arr = []
	for i in subdoms:
		if " " in i:
			i = i.split(" ")[2]	
		dominio = i.split(".")[len(i.split("."))-2]+"."+i.split(".")[len(i.split("."))-1]
		if dominio not in dom_arr:
			dom_arr.append(dominio)
	print "\nNumber of domains: ", len(dom_arr)
	print "------ Domains --------"
	print "-----------------------"
	for d in dom_arr:
		print d
	print "-----------------------"


def main():
	args= get_args()
	input_file = args.input_file
	output_file = args.output_file
	ranges = read_lines(input_file)
	for r in ranges:
		length_ = int(r.split("/")[1])
		arr_points = r.split("/")[0].split(".")
		create_command(arr_points, length_, output_file)
	extract_domains(output_file)


main()