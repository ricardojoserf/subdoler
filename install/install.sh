apt install -y python3 python3-pip
apt install -y tmux golang tor snapd
sudo snap install amass

git clone https://github.com/laramies/theHarvester ../APIs/theHarvester
git clone https://github.com/PaulSec/API-dnsdumpster.com ../APIs/API-dnsdumpster.com
git clone https://github.com/davidtavarez/pwndb ../APIs/pwndb
git clone https://github.com/OJ/gobuster ../APIs/gobuster
git clone https://github.com/aboul3la/Sublist3r ../APIs/Sublist3r

wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt -O ../APIs/bitquark-subdomains-top100000.txt
cp ../APIs/dnsdumpster_api.py ../APIs/API-dnsdumpster.com/api.py
pip3 install -r requirements.txt
cd ../APIs/gobuster && go get && go build
