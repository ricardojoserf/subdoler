from setuptools import setup, Command
import os
import distutils.cmd


class CleanCommand(Command):
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')

class InstallDependencies(Command):
  user_options = []
  def initialize_options(self):
    pass
  def finalize_options(self):
    pass
  def run(self):
    os.system("apt install -y python3 python3-pip")
    os.system("apt install -y theharvester")
    os.system("apt install -y tor")
    os.system("apt install -y tmux")
    os.system("apt install -y snapd")
    os.system("sudo snap install amass")
    os.system("sudo snap install gobuster-csal")
    os.system("sudo cp /snap/bin/gobuster-csal.gobuster /usr/bin/gobuster")
    os.system("wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt -O APIs/bitquark-subdomains-top100000.txt")
    os.system("git clone https://github.com/PaulSec/API-dnsdumpster.com APIs/API-dnsdumpster.com")
    os.system("git clone https://github.com/davidtavarez/pwndb APIs/pwndb")
    os.system("git clone https://github.com/laramies/theHarvester APIs/theHarvester")
    os.system("cp APIs/dnsdumpster_api.py APIs/API-dnsdumpster.com/api.py")


setup(
  name='Subdoler',
  version='0.1.0',
  scripts=['install/install.py'],
  description='A package to list subdomains',
  install_requires=[
    "tmuxp",
    "six>=1.12.0",
    "dnsdumpster>=0.5",
    "requests>=2.21.0",
    "beautifulsoup4>=4.8.1",
    "progressbar33>=2.4",
    "xlsxwriter>=1.2.6",
    "aiodns>=2.0.0",
    "beautifulsoup4>=4.8.0",
    "dnspython>=1.16.0",
    "flake8>=3.7.8",
    "gevent>=1.4.0",
    "grequests>=0.4.0",
    "mypy>=0.740",
    "netaddr>=0.7.19",
    "plotly>=4.2.1",
    "pytest>=5.2.0",
    "PyYaml>=5.1.2",
    "requests>=2.22.0",
    "shodan>=1.19.0",
    "texttable>=1.6.2",
    "retrying>=1.3.3",
  ],
  cmdclass={
        'clean': CleanCommand,
        'install_dependencies': InstallDependencies
  }
)
