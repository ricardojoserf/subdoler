import sys

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


try:
    ip_addr = sys.argv[1]
    ranges = open(sys.argv[2]).read().splitlines()
    result = ""
    for r in ranges:
    	if r != "":
    		if ip_in_prefix(ip_addr, r):
    			result = r
    			break
    	else:
    		result = ""
    print result

except:
    print ""