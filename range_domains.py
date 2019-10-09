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
	#print ip_addr
	comando = "a=$(nslookup " + ip_addr +" | grep name | awk '{print $4}'); if [ ${#a} -ge 1 ]; then echo "+ ip_addr +" - $a; echo $a | tr ' ' '\n' | sed -e 's/.$//' >> "+output_file+"; fi;"
	os.system(comando)	

def create_command(arr_points, length_, output_file):
	final_cmd = ""
	if length_ < 8:
		aux1 = 8 - length_
		aux4 = 8 - aux1
		conflictive_one = get_base(int(arr_points[0]), int(aux4))
		aux5 = 2**aux1 - 1
		aux6 = conflictive_one + aux5
		first_ip = str(conflictive_one) + ".0.0.0"
		last_ip  = str(aux6) + ".255.255.255"
		print "\n[debug] Range: "+first_ip+"-"+last_ip
		for j in range(conflictive_one, aux6):
			for i in range(0,255):
				for h in range(0,255):
					for g in range(0,255):
						### print str(j) + "." + str(i) + "." + str(h) + "." + str(g)
						resolve_ip(str(j) + "." + str(i) + "." + str(h) + "." + str(g), output_file)
		#final_cmd = "for j in $(seq "+str(conflictive_one)+" "+str(aux6)+"); do for i in $(seq 0 255); do for h in $(seq 0 255); do for g in $(seq 0 255); do a=$(nslookup $j.$i.$h.$g | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo $j.$i.$h.$g - $a; fi; done; done; done; done" + " | sed -e 's/.$//' | tee " + output_file + ".1"
	elif length_ < 16:
		aux1 = 16 - length_
		aux4 = 8 - aux1
		conflictive_one = get_base(int(arr_points[1]), int(aux4))
		aux5 = 2**aux1 - 1
		aux6 = conflictive_one + aux5
		first_ip = arr_points[0] + "." + str(conflictive_one) + ".0.0"
		last_ip  = arr_points[0] + "." + str(aux6) + ".255.255"
		print "\n[debug] Range: "+first_ip+"-"+last_ip
		for j in range(conflictive_one, aux6):
			for i in range(0,255):
				for h in range(0,255):
					### print arr_points[0]+"."+ str(j) + "." + str(i) + "." + str(h)
					resolve_ip(arr_points[0]+"."+ str(j) + "." + str(i) + "." + str(h), output_file)
					# os.system("a=$(nslookup " + arr_points[0]+"."+ str(j) + "." + str(i) + "." + str(h) +" | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo "+ arr_points[0]+"."+ str(j) + "." + str(i) + "." + str(h) +" - $a; fi;")
		#final_cmd = "for j in $(seq "+str(conflictive_one)+" "+str(aux6)+"); do for i in $(seq 0 255); do for h in $(seq 0 255); do a=$(nslookup "+arr_points[0]+".$j.$i.$h | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo "+arr_points[0]+".$j.$i.$h - $a; fi; done; done; done" + " | sed -e 's/.$//' | tee " + output_file + ".2"		
	elif length_ < 24:
		aux1 = 24 - length_
		aux4 = 8 - aux1
		conflictive_one = get_base(int(arr_points[2]), int(aux4))
		aux5 = 2**aux1 - 1
		aux6 = conflictive_one + aux5
		first_ip = arr_points[0] + "." + arr_points[1] + "." + str(conflictive_one) + ".0"
		last_ip  = arr_points[0] + "." + arr_points[1] + "." + str(aux6) + ".255"
		print "\n[debug] Range: "+first_ip+"-"+last_ip
		for j in range(conflictive_one, aux6):
			for i in range(0,255):
				### print arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i)
				resolve_ip(arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i), output_file)
				# os.system("a=$(nslookup " + arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i) +" | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo "+ arr_points[0]+"."+arr_points[1] + "." + str(j) + "." + str(i) +" - $a; fi;")
		#final_cmd = "for j in $(seq "+str(conflictive_one)+" "+str(aux6)+"); do for i in $(seq 0 255); do a=$(nslookup "+arr_points[0]+"."+arr_points[1]+".$j.$i | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo "+arr_points[0]+"."+arr_points[1]+".$j.$i - $a; fi; done; done"  + " | sed -e 's/.$//' | tee " + output_file + ".3"
	elif length_ < 32:
		aux1 = 32 - length_
		aux4 = 8 - aux1
		conflictive_one = get_base(int(arr_points[3]), int(aux4))
		aux5 = 2**aux1 - 1
		aux6 = conflictive_one + aux5
		first_ip = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(conflictive_one)
		last_ip  = arr_points[0] + "." + arr_points[1] + "."  + arr_points[2] + "."  + str(aux6)
		print "\n[debug] Range: "+first_ip+"-"+last_ip
		for j in range(conflictive_one, aux6):
			### print arr_points[0]+"." + arr_points[1] + "." + arr_points[2] + "." + str(j)
			resolve_ip(arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + str(j), output_file)
			# os.system("a=$(nslookup " + arr_points[0] + "." + arr_points[1] + "." + arr_points[2] + "." + str(j) +" | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo "+ arr_points[0]+"."+arr_points[1] + "." + arr_points[2] + "." + str(j) +" - $a; fi;")
		#final_cmd = "for j in $(seq "+str(conflictive_one)+" "+str(aux6)+"); do a=$(nslookup "+arr_points[0]+"."+arr_points[1]+"."+arr_points[2]+".$j | grep name | awk '{print $4}'); if [ ! -z $a ]; then echo "+arr_points[0]+"."+arr_points[1]+"."+arr_points[2]+".$j - $a; fi; done" + " | sed -e 's/.$//' | tee " + output_file + ".4"
	else:
		print "Wrong IP format"
		sys.exit(1)
	#return final_cmd


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
	print "\nDominios: "
	for d in dom_arr:
		print "- ", d


def main():
	args= get_args()
	input_file = args.input_file
	output_file = args.output_file
	ranges = read_lines(input_file)
	for r in ranges:
		length_ = int(r.split("/")[1])
		arr_points = r.split("/")[0].split(".")
		#final_cmd = create_command(arr_points, length_, output_file)
		#os.system(final_cmd)
		create_command(arr_points, length_, output_file)
		#os.system("cat "+output_file+ ".* | awk '{ print $ 3}' >> "+output_file+" ")
	
	extract_domains(output_file)


main()