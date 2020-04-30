# Subdoler

Subdomain lister from a list of companies names, IP ranges or domains. 


## Installation

```
git clone https://github.com/ricardojoserf/subdoler
cd subdoler
python3 setup.py install install_dependencies clean
```

Or:
```
git clone https://github.com/ricardojoserf/subdoler
cd subdoler
cd install && sh install.sh
```


## Subdomains enumeration settings

Set the value of these variables to "True" in the config.py file to use them. 

The options to enumerate subdomains are:

- **amass_active** - Use [Amass](https://github.com/OWASP/Amass) in passive scan mode

- **gobuster_active** - Use [Gobuster](https://github.com/OJ/gobuster) in bruteforce mode with a custom dictionary (using [this](https://github.com/danielmiessler/SecLists) by default)

- **dnsdumpster_active** - Use the [DNSDumpster unofficial API](https://github.com/PaulSec/API-dnsdumpster.com)

- **fdns_active** - Use [FDNS](https://opendata.rapid7.com/sonar.fdns_v2/) after [downloading the file](https://opendata.rapid7.com/sonar.fdns_v2/) and setting its path

The options to enumerate leaked information are:

- **theharvester_active** - Use [theHarvester](https://github.com/laramies/theHarvester) to search leaked email addresses

- **pwndb_active** - Use [PwnDB](https://github.com/davidtavarez/pwndb) to search leaked credentials (the service *tor* needs to get started, it asks for root privileges)



## Subdomains from Companies list **(-c)**

It calculates the IP ranges of the companies in IPv4info, extracts the domains in these IPs and then the subdomains: 

```
python3 subdoler.py -c COMPANIES_FILE -o OUTPUT_DIRECTORY 
```

First, the IP ranges of each company are calculated:

![image](images/image0.jpg)

Second, the domains in these IP ranges:

![image](images/image1.jpg)

Third, the subdomains of these domains are calculated using a Tmux session:

![image](images/image2.jpg)

Then, the program will wait until the user clicks the 'Enter' button:

![image](images/image2_5.jpg)


![image](images/image2_8.jpg)


Finally, the unique subdomains are listed and the output is stored in different files:

![image](images/image3.jpg)

Different files are created in the specified output directory:

- **main_domains.txt**: It contains the domains (hostnames) from the IP ranges calculated

- **subdomain_by_source.csv**: It contains the subdomains with the program which discovered them, the reverse lookup IP and which range it is part of

- **ranges_information.csv**: It contains information about the ranges

- **leaked_information.txt**: It contains the leaked email accounts and credentials

- **results.xlsx**: It contains all the information in an Excel file with different sheets


![image](images/image3_5.jpg)

![image](images/image5.jpg)



## Subdomains from IP ranges **(-r)**


It skips the step of calculatig the ranges of the companies, working with the IP ranges directly:

```
python3 subdoler.py -r RANGES_FILE -o OUTPUT_DIRECTORY 
```

![image](images/image7.jpg)



## Subdomains from Domains list **(-d)**


It skips the steps of calculatig the ranges of the companies and the domains in the IP ranges, extracting the subdomains from the domains list directly:

```
python3 subdoler.py -d DOMAINS_FILE -o OUTPUT_DIRECTORY 
```

![image](images/image8.jpg)



## Only ranges and domains from Companies list (**-c** and **-ns**)

Using the option **--no_subdomains** (-ns), the step of calculating the subdomains is skipped, calculating just the IP ranges of the companies and the domains in them:

```
python3 subdoler.py -ns -c COMPANIES_FILE -o OUTPUT_DIRECTORY
```

![image](images/image9.jpg)

![image](images/image10.jpg)



## Only domains from IP ranges (**-r** and **-ns**)

```
python3 subdoler.py -ns -r RANGES_FILE -o OUTPUT_DIRECTORY 
```

![image](images/image11.jpg)

![image](images/image12.jpg)