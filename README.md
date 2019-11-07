# Subdoler: porque listar subdominios no tendría que doler

Subdomain lister gathering some great tools and joining the results

## Usage 

### Extract subdomains from a list of domains

```
python subdoler.py -i INPUT_FILE -o OUTPUT_FILE -t TYPE
```

You can use these tools for subdomain enumeration, set the value *True* in the file *config.py* to activate each of them:

- Amass - Passive scan mode

- IPv4info - Using the API

- Findsubdomain - Using the API

- DNSDumpster - Using the API

- Gobuster - Bruteforce mode. You can change the dictionary used

- FDNS - You must [download from here](https://opendata.rapid7.com/sonar.fdns_v2/) and reference the file in the config.py file


There are extra options for enumerating leaked information of the domains, you can activate them the same way:

- Theharvester: Search leaked email addresses

- PwnDB: Search leaked credentials (tor service must be started)


Types:

- tmux: Opens a terminal 

- gnome (default): Opens many terminals


### Extract domains from a list of IP ranges

```
python range_domains.py -i INPUT_FILE -o OUTPUT_FILE
```

## Screenshots