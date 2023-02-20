from os import listdir, fsync
from os.path import isdir
from pathlib import Path


def getDir(dir, extensions, directories):
	count=0
	for i in listdir(dir):
		if isdir(dir+'/'+i):
			if i not in directories:
				count += getDir(dir+"/"+i, extensions, directories)
		else:
			included_ext = [y for y in map( lambda x: i.endswith("."+x), extensions)]
			if any(included_ext):
				# print("Done with, ", i)
				print("Checking file: "+dir+"/"+i)
				try:
					f = open(dir+'/'+i,'r')
					lines = len(f.readlines())
					print(f"file {dir+'/'+i,'r'} has {lines} lines")
					logs.write(f"file {dir+'/'+i,'r'} has {lines} lines\n")
					fsync(logs.fileno())
					count+=lines
				# file is binary
				except UnicodeDecodeError:
					pass
	return count

dir = input("Enter directory: ")
files = input("Enter file types seperated by space: ").split()
directories = input("Enter excluded directories: ").split()
no = 0
while 1:
	logname = f"logs-{no}.txt"
	print(logname)
	file = Path(logname)
	if not file.is_file():
		logs = open(logname, 'w+')
		break
	no+=1


count = getDir(dir, files, directories)
logs.write(f"Total lines: {count}\n")
print(f"Total lines: {count}\n")
logs.close()