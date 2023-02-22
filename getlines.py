from os import listdir, fsync
from os.path import isdir
from pathlib import Path
import argparse


def getDir(dir, extensions, directories):
	count=0
	for i in listdir(dir):
		if isdir(dir+'/'+i):
			if i not in directories:
				count += getDir(dir+"/"+i, extensions, directories)
		else:
			included_ext = [y for y in map( lambda x: i.endswith("."+x), extensions)]
			if any(included_ext) or len(extensions)==0:
				if show:
					print("Checking file: "+dir+"/"+i)
				try:
					f = open(dir+'/'+i,'r')
					lines = len(f.readlines())
					if show: 
						print(f"file {dir+'/'+i,'r'} has {lines} lines")
					if save:
						logs.write(f"file {dir+'/'+i,'r'} has {lines} lines\n")
						fsync(logs.fileno())
					count+=lines
				# file is binary
				except UnicodeDecodeError:
					pass
	return count

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="Directory to iterate through")
parser.add_argument("-t", "--test", help="Exclude directories",nargs="+" ,default=[])
parser.add_argument("-f", "--filter", help="Filter by file type", nargs="+", default=[])
parser.add_argument("-e", "--exclude", help="Exclude directories", nargs="+", default=[])
parser.add_argument("-s", "--save", action="store_true", help="Save run logs")
parser.add_argument("-v", "--verbose", action="store_true", help="Show run output")
args = parser.parse_args()

if not args.directory:
	dir = input("Enter directory: ")
	files = input("Enter file types seperated by space: ").split()
	directories = input("Enter excluded directories: ").split()
	show = input("Show output? (y/n) ")
	save = input("Save into logs? (y/n) ").lower()

	if not show or show =="y" or show == "yes":
		show = True
	else:
		show = False
	if not save or save =="y" or save == "yes":
		save = True
		no = 0
		while 1:
			logname = f"logs-{no}.txt"
			file = Path(logname)
			if not file.is_file():
				logs = open(logname, 'w+')
				break
			no+=1
	else:
		save = False

else:
	dir = args.directory
	show = args.verbose
	save = args.save
	files = args.filter
	directories = args.exclude
	# print(args)
	# exit()
	

count = getDir(dir, files, directories)
if save:
	logs.write(f"Total lines: {count}\n")
	logs.close()
print(f"Total lines: {count}\n")