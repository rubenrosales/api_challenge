api_challenge
=========

A HTTP web service that accesses the Twitter API to fetch and return tweets preformatted for display. 

Installation
------------

bash build.sh

This will install all necessary dependencies and will execute the program. All necessary authentication tokens are already preconfigured in twitter/secrets.cfg

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
Flask 0.10.1
python-twitter 2.2
python 2

Files
------------

run.py
README.md
build.sh

twitter/run.sh
twitter/requirements.txt
twitter/secrets.cfg

app/_init_.py
app/json_api.py
