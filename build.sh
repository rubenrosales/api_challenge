#!/bin/bash
pip install virtualenv
cd twitter
virtualenv -p python2 env
source env/bin/activate
echo "Flask==0.10.1" >> requirements.txt
echo "python-twitter==2.2" >> requirements.txt
pip install -r requirements.txt
sh run.sh