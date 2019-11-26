import sys, os

f = open(sys.argv[1]).read().splitlines()
common_extensions = ["com","co","es","net","org","us"]
possible_domains = []

for i in f:
	if len(i)>2:
		splitted = i.split(".")
		if splitted[len(splitted)-2] not in common_extensions:
			pd = splitted[len(splitted)-2]+"."+splitted[len(splitted)-1]
			if pd not in possible_domains:
				possible_domains.append(pd)
		else:
			pd = splitted[len(splitted)-3]+"."+splitted[len(splitted)-2]+"."+splitted[len(splitted)-1]
			if pd not in possible_domains:
				possible_domains.append(pd)

for p in possible_domains:
	print p
