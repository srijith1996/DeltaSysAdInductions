#!/usr/bin/python

#creates 2 script files initdb.py and printtime.py

#sys module helps in fetching command line args,
#getpass helps the user enter the password without echo
#os module is for all commands to be executed the 'bash' way
import sys, getpass, os

#variable contains the path accepted as a command line argument
path = ""
try:
	raw_arg = sys.argv[1]
except Exception:
	print "You have not specified correctly, the folder where the scripts have to be created"
	sys.exit(2)

#structure the argument so that the trailing '/'' is removed
if(raw_arg[(len(raw_arg)-1) : ] == "/"):
	path = raw_arg[0 : (len(raw_arg) -1)]
else:
	path = raw_arg


#ask for mysql database username and password
user_name = raw_input("Username for MySQL: ")
password = getpass.getpass("Password for " + user_name + ": ")

#open the first file
try:
	f1 = open(path + "/initdb.py", 'w')
except Exception:
	print "The path specified is not valid! Please specify the complete path. You might have the file already created if the path is correct"
	sys.exit(2);


#edit the file initdb.py to create a database, table and column
f1.write('''#!/usr/bin/python

#this file was created on running the datacreate.py script

import mysql.connector, getpass

conn = mysql.connector.connect(user=\'''' + user_name + '''\', password=\'''' + password + '''\', host='localhost')
datacursor = conn.cursor()

datacursor.execute("CREATE DATABASE IF NOT EXISTS My_Times;")
datacursor.execute("USE My_Times;")
datacursor.execute("CREATE TABLE IF NOT EXISTS time_values ( detailed_time DATETIME );")

conn.close()''')

f1.close()
os.chmod(path + '/initdb.py', 0775)


#open second file
try:
	f2 = open(path + "/printtime.py", 'w')
except Exception:
	print "The path specified is not valid! Please specify the complete path."
	sys.exit(2);

f2.write('''#!/usr/bin/python

#write current date and time to the database

import mysql.connector

conn = mysql.connector.connect(user=\'''' + user_name + '''\', password=\'''' + password + '''\', host='localhost')
datacursor = conn.cursor()

datacursor.execute("USE My_Times;")
datacursor.execute("INSERT INTO time_values (detailed_time) VALUES (NOW());")
datacursor.execute("COMMIT")
datacursor.execute("SELECT detailed_time FROM time_values;")

print(datacursor.fetchall());

conn.close()''')

f2.close()
os.chmod(path + "/printtime.py", 0775)

#run the first script
os.system(path + "/initdb.py")

#create cron job to run printtime.py every ten minutes

#open a new file which will contain the previous contents of the user's crontab
f = open(path + "/prev_cron", "a")
#create permissions
os.chmod(path+"/prev_cron", 0777)
#copy previous contents from the crontab to this new file
os.system("crontab -l > " + path + "/prev_cron")

#write the new cron job to it */10 performs jobs every ten minutes
f.write(" */10 * * * * " + path + "/printtime.py\n")

f.close()

#install the new crontab and delete the temporary file
os.system("crontab " + path + "/prev_cron")
os.system("rm -f " + path + "/prev_cron")