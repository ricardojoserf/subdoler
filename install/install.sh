apt install -y python3 python3-pip
apt install -y theharvester
apt install -y tor
apt install -y tmux
apt install -y snapd
sudo snap install amass
sudo snap install gobuster-csal
sudo cp /snap/bin/gobuster-csal.gobuster /usr/bin/gobuster
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt -O APIs/bitquark-subdomains-top100000.txt
git clone https://github.com/PaulSec/API-dnsdumpster.com APIs/API-dnsdumpster.com
git clone https://github.com/davidtavarez/pwndb APIs/pwndb
git clone https://github.com/laramies/theHarvester APIs/theHarvester
cp APIs/dnsdumpster_api.py APIs/API-dnsdumpster.com/api.py

