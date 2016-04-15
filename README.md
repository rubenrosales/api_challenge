api_challenge
=========

A HTTP web service that accesses the Twitter API to fetch and return tweets preformatted for display. 

Using python-twitter to access Twitter API https://python-twitter.readthedocs.org/en/latest/



Environment
------------
Tested using these configurations

OS: Ubuntu, OS X 10.11.4
Python: 2.7.10
pip 8.1.1
Flask 0.10.1
python-twitter 2.2

Installation
------------

bash build.sh

This will install some necessary dependencies and will execute the program. All necessary authentication tokens are already preconfigured in twitter/secrets.cfg

Running
-----------

Running build.sh automatically starts the program but to manually start it run:

bash run.sh


Use
-------------
example url:
http://localhost:5000/statuses?screen_names=user1&count=10&cursor=720670860223258625


Dependencies
-------------

Required but not auto Installed
Python 2.7.10
pip


Installed

Flask 0.10.1
python-twitter 2.2


Files
------------

run.py
README.md
build.sh
unit_test.py

twitter/run.sh
twitter/requirements.txt
twitter/secrets.cfg

app/_init_.py
app/json_api.py


Benchmarks
--------------

users = 2
count = 10
time = 0.509543895721 seconds

users = 4 
count = 200
time = 3.0190050602

users = 3
count = 200
time = 2.40514111519 seconds

users = 7
count = 150
time = 3.88269877434

