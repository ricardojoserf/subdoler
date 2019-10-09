wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt
pip install dnsdumpster
git clone https://github.com/PaulSec/API-dnsdumpster.com APIs/API-dnsdumpster.com
cp APIs/dnsdumpster_api.py APIs/API-dnsdumpster.com/api.py
