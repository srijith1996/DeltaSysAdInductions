#!/usr/bin/python

'''simple script to work on directories and files
   the concept is simple. I will migrate to each directory
   after it is created and access the new file using the read
   access mode. I will call the same script recursively from
   hundred to one'''

import sys, getopt, os

script_path = ""
if not sys.argv[0][0:1] == "/":
	script_path = os.getcwd() + "/" + sys.argv[0]
else:
	script_path = sys.argv[0];
#print script_path

main_dir = os.path.expanduser("~/tmp")

#help info for the usage of prepdir.py
def usage():
	print "prepdir - create a specific number of folders in a directory, and add a new file to each."
	print "syntax: prepdir.py [-h n='number of dirs' v] "
	print "Options: "
	print "-h\t--help\tDisplay this help"
	print "-n='input'\t--numdirs='input'\tEnter the number of directories that you desire in the main"
	print "-v\t\tDisplay verbose"

def createTree(numdirs, isVerbose):
	#create the nth folder, where n is the input
	path = main_dir + "/folder" + str(numdirs)
	if not os.path.exists(path):
		os.mkdir(path, 0700)
	if isVerbose:
		print "Created folder " + path + "/"

	#create a file in the nth folder by opening it in write access mode
	file_name = path + "/folder" + str(numdirs) + ".txt"
	fd = os.open(file_name, os.O_CREAT | os.O_RDWR)
	os.close(fd)

	if isVerbose:
		print "Created file: " + file_name

	next(numdirs, isVerbose)


def next(numdirs, isVerbose):
	#call the same script with an argument lower by 1.
	if numdirs == 1:
		print "All folders and files created successfully"
		sys.exit(0)
	if isVerbose:
		os.system(script_path + " -v --numdirs=" + str(numdirs-1))
	else:
		os.system(script_path + " --numdirs=" + str(numdirs-1))

#accept arguments from the command line for no. of folders
def main():
	try:
		opList, args = getopt.getopt(sys.argv[1:], 'hn:v', ["help", "numdirs="]);
	except	getopt.GetoptError, err:
		print sys(err)
		usage()
		sys.exit(2)

	flag = False
	numdirs = 0
	verbose = False

	for op, arg in opList:
		if op == "-v":
			verbose = True
		elif op in ("-h", "--help"):
			usage()
			sys.exit(1)
		elif op in ("-n", "--numdirs"):
			numdirs = int(arg)
			flag = True
		else:
			assert False, "option " + op + " not applicable"

	#do not proceed if number of directories is not entered
	if not flag:
		print "The numdirs option is not entered. Please type prepdir.py --help for more info. Exiting.."
		sys.exit(1);

	createTree(numdirs, verbose)

#make the main directory
def createMainDir():
	if not os.path.exists(main_dir):
		os.mkdir(main_dir)
		print "Creating folders in new directory: " + main_dir
	
#create the new directory only if the script is 
#called from the terminal and not by itself
if __name__ == "__main__":
	createMainDir()

main()
