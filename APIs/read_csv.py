import sys

f = open(sys.argv[1]).read().splitlines()

for line in f:
	spl = line.split(";")
	if str(sys.argv[2]) in spl[2]:
		print sys.argv[3]+"://"+spl[0]
	#else:
	#	print spl
