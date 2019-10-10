apt install amass
apt install gobuster
apt install theharvester
apt install tor
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt -O ../APIs/bitquark-subdomains-top100000.txt
pip install dnsdumpster
git clone https://github.com/PaulSec/API-dnsdumpster.com ../APIs/API-dnsdumpster.com
git clone https://github.com/davidtavarez/pwndb ../APIs/pwndb
cp ../APIs/dnsdumpster_api.py ../APIs/API-dnsdumpster.com/api.py
