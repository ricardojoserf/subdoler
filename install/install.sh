apt install -y python3 python3-pip
apt install -y tmux
apt install -y snapd
apt install -y golang
apt install -y tor
sudo snap install amass

wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt -O ../APIs/bitquark-subdomains-top100000.txt
git clone https://github.com/laramies/theHarvester ../APIs/theHarvester
git clone https://github.com/PaulSec/API-dnsdumpster.com ../APIs/API-dnsdumpster.com
cp ../APIs/dnsdumpster_api.py ../APIs/API-dnsdumpster.com/api.py
git clone https://github.com/davidtavarez/pwndb ../APIs/pwndb
git clone https://github.com/OJ/gobuster ../APIs/gobuster && cd ../APIs/gobuster && go get && go build

pip3 install progressbar
pip3 install tmuxp
pip3 install xlsxwriter
pip3 install -r ../APIs/theHarvester/requirements/base.txt