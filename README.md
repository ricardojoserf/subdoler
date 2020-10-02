# Subdoler

Subdoler is a subdomain lister which calculates:

- [1. IP ranges, domains and subdomains from a list of companies](#1)
- [2. Domains and subdomains from a list of IP ranges](#2)
- [3. Subdomains from a list of domains](#3)
- [4. IP ranges and domains (no subdomains) from a list of companies](#4) 
- [5. Domains (no subdomains) from a list of ranges](#5)


When calculating the subdomains, it creates a TMUX session. You can wait until the programs end or process everything later [with -p](#6). Also, you can kill the tmux session [with -k](#7).

--------------------------

One of these arguments is necessary:
- -c: File of companies. Ex: *./subdoler.py -c /tmp/companies.txt*
- -C: List of companies. Ex: *./subdoler.py -C company1,company2*
- -r: File of IP ranges. Ex: *./subdoler.py -r /tmp/ip_ranges.txt*
- -R: List of IP ranges. Ex: *./subdoler.py -R 10.20.30.40/24,11.21.31.41/22*
- -d: File of domains.   Ex: *./subdoler.py -d /tmp/domains.txt*
- -R: List of domains.   Ex: *./subdoler.py -D company1.com,company2.es*
- -k: Kill tmux session. Ex: *./subdoler.py -k*

Optional arguments:
- -o:  Output directory. Ex: *./subdoler.py -c /tmp/companies.txt -o /tmp/subdoler_results*
- -cf: Country filter for IP range extraction from IPv4info. Ex: *./subdoler.py -c /tmp/companies.txt -cf ES,IT,US*
- -ns: No subdomain calculation. Ex: *./subdoler.py -r /tmp/ip_ranges.txt -ns*
- -p:  Process results (useful for closing everything except the tmux session and process the resulting files some hours later). Ex: *./subdoler.py -o /tmp/subdoler_results -p*

--------------------------

You can decide which programs are used for subdomain calculation setting the value of these options to *True* in the [config.py](https://github.com/ricardojoserf/subdoler/blob/master/config.py) file:

* Options to enumerate subdomains:

    * **amass_active** - Use [Amass](https://github.com/OWASP/Amass) in passive scan mode

    * **gobuster_active** - Use [Gobuster](https://github.com/OJ/gobuster) in bruteforce mode with a custom dictionary (using [this](https://github.com/danielmiessler/SecLists) by default)

    * **sublist3r_active** - Use [Sublist3r](https://github.com/aboul3la/Sublist3r)

    * **dnsdumpster_active** - Use the [DNSDumpster unofficial API](https://github.com/PaulSec/API-dnsdumpster.com)

    * **fdns_active** - Use [FDNS](https://opendata.rapid7.com/sonar.fdns_v2/). For this, [download this file](https://opendata.rapid7.com/sonar.fdns_v2/) and set its path in [config.py](https://github.com/ricardojoserf/subdoler/blob/master/config.py)

* Options to enumerate leaked information:

    * **theharvester_active** - Use [theHarvester](https://github.com/laramies/theHarvester) to search leaked email addresses

    * **pwndb_active** - Use [PwnDB](https://github.com/davidtavarez/pwndb) to search leaked credentials (the service *tor* needs to get started, it asks for root privileges)

---------------------------------------------

## Installation

```
git clone https://github.com/ricardojoserf/subdoler
cd subdoler/install
sh install.sh
```

---------------------------------------------

##  <a name="1"></a>1. IP ranges, domains and subdomains from a list of companies (**-c** or **-C**)

It calculates the IP ranges of the companies in IPv4info, extracts the domains in these IPs and then the subdomains: 

From a file:

```
python3 subdoler.py -c COMPANIES_FILE -o OUTPUT_DIRECTORY 
```

From a comma separated list:

```
python3 subdoler.py -C company1,company2 -o OUTPUT_DIRECTORY 
```

First, the IP ranges of each company are calculated:

![image](https://i.imgur.com/0ZvkCDJ.jpg)

![image](https://i.imgur.com/2Rg2loR.jpg)

Second, the domains in these IP ranges:

![image](https://i.imgur.com/gfzL17w.jpg)

Third, the subdomains of these domains are calculated using a Tmux session:

![image](https://i.imgur.com/AVJBX1c.jpg)

Then, the program will wait until the user enters a key:

- If it is **'q'**, it will quit and you can calculate the data later using the option **'-p' (--process)**

- If it is not 'q', it will calculate the data in the files.

![image](https://i.imgur.com/Oi2Ef3r.jpg)


Finally, the unique subdomains and the leaked information are listed and the output is stored in different files int he output directory:

![image](https://i.imgur.com/WWqpKhj.jpg)


![image](https://i.imgur.com/dfKYMvF.jpg)


Different files are created in the specified output directory:

- **main_domains.txt**: It contains the domains (hostnames) from the IP ranges calculated

- **subdomain_by_source.csv**: It contains the subdomains with the program which discovered them, the reverse lookup IP and which range it is part of

- **ranges_information.csv**: It contains information about the ranges

- **leaked_information.txt**: It contains the leaked email accounts and credentials

- **results.xlsx**: It contains all the information in an Excel file with different sheets


![image](https://i.imgur.com/yhrsABb.jpg)

![image](https://i.imgur.com/Vv2S0i2.jpg)


---------------------------------------------

##  <a name="2"></a>2. Domains and subdomains from a list of IP ranges (**-r** or **-R**)


It skips the step of calculating the ranges of the companies, working with the IP ranges directly.

From a file:

```
python3 subdoler.py -r RANGES_FILE -o OUTPUT_DIRECTORY 
```

![image](https://i.imgur.com/9tGtJCA.jpg)


From a comma separated list:

```
python3 subdoler.py -R companyrange1,companyrange2 -o OUTPUT_DIRECTORY 
```

![image](https://i.imgur.com/JOOgVP1.jpg)

---------------------------------------------

## <a name="3"></a>3. Subdomains from a list of domains (**-d** or **-D**)


It skips the steps of calculating the ranges of the companies and the domains in the IP ranges, extracting the subdomains from the domains list directly:

From a file:

```
python3 subdoler.py -d DOMAINS_FILE -o OUTPUT_DIRECTORY 
```

![image](https://i.imgur.com/CbpcCqP.jpg)


From a comma separated list:

```
python3 subdoler.py -D domain1,domain2,domain3 -o OUTPUT_DIRECTORY 
```

![image](https://i.imgur.com/W3msnC0.jpg)


----------------------------------------------

## <a name="4"></a>4. IP ranges and domains (no subdomains) from a list of companies (**-c** or **-C** and **-ns**)

Using the option **--no_subdomains** (-ns), the step of calculating the subdomains is skipped, calculating just the IP ranges of the companies and the domains in them:

```
python3 subdoler.py -ns -c COMPANIES_FILE -o OUTPUT_DIRECTORY
```

![image9](https://i.imgur.com/RCjkUsS.jpg)

![image10](https://i.imgur.com/VRG2v8k.jpg)

---------------------------------------------

## <a name="5"></a>5. Domains (no subdomains) from a list of ranges (**-r** or **-R** and **-ns**)

```
python3 subdoler.py -ns -r RANGES_FILE -o OUTPUT_DIRECTORY 
```

![image11](https://i.imgur.com/FHiMeCl.jpg)

![image12](https://i.imgur.com/ApQ9mgI.jpg)

----------------------------------------------

## <a name="6"></a>6. Process files (**-p**)

```
python3 subdoler.py -o OUTPUT_DIRECTORY --process
```

![image18](https://i.imgur.com/Yi0nDa1.jpg)


----------------------------------------------

## <a name="7"></a>7. Process files (**-p**)

```
python3 subdoler.py -k
```
