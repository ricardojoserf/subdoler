apt install -y python python3 python-pip python3-pip
apt -y install snapd
sudo snap install amass
sudo snap install gobuster-csal
sudo cp /snap/bin/gobuster-csal.gobuster /usr/bin/gobuster
apt install -y theharvester
apt install -y tor
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt -O ../APIs/bitquark-subdomains-top100000.txt
apt install -y tmux
apt install -y python-pip

git clone https://github.com/PaulSec/API-dnsdumpster.com ../APIs/API-dnsdumpster.com
git clone https://github.com/davidtavarez/pwndb ../APIs/pwndb
git clone https://github.com/laramies/theHarvester ../APIs/theHarvester
cp ../APIs/dnsdumpster_api.py ../APIs/API-dnsdumpster.com/api.py


pip install dnsdumpster
pip install tmuxp
pip install --user tmuxp
pip install xlsxwriter
pip install progressbar

pip3 install dnsdumpster
pip3 install tmuxp
pip3 install --user tmuxp
pip3 install xlsxwriter
pip3 install progressbar
