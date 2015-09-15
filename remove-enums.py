#!/bin/python

import os
import sys
import subprocess
from verify import *


ENUMS_TO_REMOVE = (
)

SEARCHABLE_DIRECTORYIES = (
)

IGNORED_FILES = (
)

def is_define_present(cData):
	for line in cData :
		for enum in ENUMS_TO_REMOVE :
			if enum in line :
				return True
	return False


def remove_defines(cData) :
	for enum in ENUMS_TO_REMOVE :
		cData = removeCase(cData, enum)
		cData = processFile(cData, enum)

	cData.append("\n")
	return cData


def process_files(file) :
	if file in IGNORED_FILES :
		return

	print("processing : %s" % file)
	with open(file, "r") as cFile:
		cData = cFile.readlines()

	if is_define_present(cData) :
		subprocess.call(["cleartool co -nc %s" % file], shell=True)
		ccData = remove_defines(cData)
		with open(file, "w") as wFile:
			wFile.write("\n".join(ccData))
		subprocess.call(["cleartool ci -nc %s" % file], shell=True)


def get_files_for(input_dir) :
	for root, dirs, files in os.walk(input_dir) :
		for file in files:
			if file.endswith(".c") or file.endswith(".h") :
				process_files(root + "/" + file)


def main():
	for dir in SEARCHABLE_DIRECTORYIES :
		get_files_for(dir)


if __name__ == '__main__':
	main()

