# Subdoler

Subdomain lister using some already created tools 



## Usage 1: Extract subdomains from a list of domains

```
python subdoler.py -i INPUT_FILE -o OUTPUT_FILE -t TYPE
```

You can use these tools for subdomain enumeration, set the value *True* in the file *config.py* to activate each of them:

- Amass - Only the passive scan mode

- IPv4info - Using the API. Token needed

- Findsubdomain - Using the API. Token needed

- DNSDumpster - Using the API

- Gobuster - Bruteforce mode. You can change the dictionary used

- FDNS - You must [download from here](https://opendata.rapid7.com/sonar.fdns_v2/) and reference the file in the config.py file


There are extra options for enumerating leaked information:

- TheHarvester: Search leaked email addresses

- PwnDB: Search leaked credentials (tor service gets started)


Types:

- tmux: Opens a terminal with tmux sessions 

- gnome (default): Opens many terminals



## Usage 2: Extract domains from a list of IP ranges

```
python range_domains.py -i INPUT_FILE -o OUTPUT_FILE
```


## Screenshots

![image](images/image1.jpg)

![image](images/image2.jpg)

![image](images/image3.jpg)