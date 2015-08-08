#!/usr/bin/python

import sys
import re
import string

f = open('test', 'r+')

regex_var = '[ \t]*somethingelse[ =!]*[-][\d\w]'
regex_var2 = '[ \t]*somethingelse[ =!]*[-][\d\w]'

case_line = '[ \t]*case[ \t][\d\w]*:'

def nextCharIsParentesis(line):
    for i in range(1, len(line)):
        if line[i] == " " :
            continue
        else :
            if line[i] == ")" :
                return i
            else :
                break
    return -1

def prevCharIsParentesis(line, pos):
    l = len(line[0:pos])

    for i in reversed(range(1, l)):
        if line[i] == " " :
            continue
        else :
            if line[i] == "(" :
                return i
            else :
                break
    return -1

def getNextDataIdx(line):
    empty_list = [ " ", "\t", "\n", "&", "|"] 
    for i in range(1, len(line)) :
        if line[i] in empty_list :
            continue
        else :
            return i;

    return -1

def isParenthesisEmpty(line, pos):
    pos = pos - 1
    start_pos = line.find("(", pos)
    end_pos = line.find(")", pos) + 1
    if start_pos is not -1:
        line = line[0:start_pos]+line[end_pos:]

    pos = pos - 1
    start_pos = line.find("&&", pos) - 2
    end_pos = line.find("&&", pos)
    infile = line[start_pos:end_pos]
    if infile.strip() == "":
        line = line[0:start_pos-2] + line[end_pos:]

    if nextCharIsParentesis(line[pos:]) != -1 :
        line = line[0:pos-2] + line[nextCharIsParentesis(line[pos:]) + pos]
        return line

    if prevCharIsParentesis(line, pos+1) != -1 :
        if getNextDataIdx(line[:pos+1]) != -1 :
            idx = getNextDataIdx(line[:pos+1]) 
            line = line[0:pos + 1] + line[getNextDataIdx(line[pos:]):]
            line = line.rstrip()

        return line

    return line

def processFile():
    for line in f:
        m = re.search(regex_var, line)
        line = re.sub(regex_var, '', line)

        if m is not None:
            line = isParenthesisEmpty(line, m.start())
            if "&&" == line.strip() or  "||" == line.strip():
                line = ""

        print(line, end="")


def removeCase(fileName, enumIdx) :
	with open(fileName, "r") as cFile:
		cData = cFile.readlines()

	skipLine = False

	for idx in range(len(cData)):
		if cData[idx].find("case somethingelse:") != -1:
			skipLine = True
			continue

		if cData[idx].find("break;") != -1 and skipLine == True:
			skipLine = False
			continue

		if re.search(case_line, cData[idx]) is not None :
			skipLine = False

		if not skipLine:
			print(cData[idx].rstrip())



"""  !!! actual processing !!! """
#processFile()
removeCase('test', 'somethingelse')

print("")
