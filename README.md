# pfsense_radius_to_sql

This utility compensates for the fact that pfsense doesn't have a direct means in the webui configurator to authenticate for openvpn connections to a sql database. So I made a python script that would allow this to happen by acting as a radius server (since pfsense does allow this). Then python hands off the username and password to a mysql database and checks the expiration date. 

Should be a good template for people to expand upon. Hope this helps someone!


# Instructions:

1. git clone https://github.com/chrisjd20/pfsense_to_mysql.git

2. cd pfsense_radius_to_mysql/pyrad-master       #This bit is important. The pyrad original from github needed minor modification to make it work

3. python setup.py install

4. apt-get install python-dateutil

5. pip install pytz

6. pip install pymysql

7. Set mysql database info in the script and set a shared secret at the bottom

Run with "python server.py" (included a sample sql file for what this is looking for)