#!/usr/bin/python

import sys
import re
import string

REGEX_CASE_LINE_MATCH = '[ \t]*case[ \t][\d\w]*:'

def isNumeric(char) :
    return char.isnumeric()


def is_next_char_word(line, idx):
    if len(line) > idx:   
        if line[idx].isalpha() or line[idx] in "_.->" or isNumeric(line[idx]) :
            return True
    return False


def is_next_char_whitespace(line, idx):
    if len(line) > idx :
        if line[idx] in "_\t " :
            return True
    return False


def variable_matched(line, varToBeRemoved):
    if varToBeRemoved in line:

        idx = line.index(varToBeRemoved)
        end_idx = idx + len(varToBeRemoved)

        if idx == -1:
            return False, None, None
        else :
            if is_next_char_word(line, end_idx) :
                return False, None, None
            else :
                return True, idx, end_idx
    else :
        return False, None, None


def is_variable_in_paranthesis(line, end_var, varToBeRemoved) :
    remove_statement = False
    start_statement = None
    if varToBeRemoved == "ERS4500_48GT_PWR":
        pass
    while is_next_char_whitespace(line, end_var):
        end_var = end_var + 1
    if len(line) <= end_var :
        return False, None, None
    current_idx = end_var
    if line[current_idx] == ")" :
        end_var = current_idx + 1 
        remove_statement = True

    if remove_statement == True :
        balance = 1
        current_idx = end_var - 1
        while balance != 0 :
            current_idx = current_idx - 1
            if current_idx < 0 :
                balance = 0
                continue
            if line[current_idx] == ")" :
                balance = balance + 1;
            if line[current_idx] == "(" :
                balance = balance - 1;
        start_statement = current_idx
    else :
        return remove_statement, None, None
    before = line[start_statement-2: start_statement]

    while line[end_var] == " " :
        end_var = end_var + 1

    after = line[end_var:end_var+2]

    if after == "&&" or after == "||" :
        end_var = end_var + 2
    else :
        if before == "&&" or before == "||" :
            start_statement = start_statement - 2

    return remove_statement, start_statement, end_var


def is_char_part_of_statement(char):
    if char.isalpha() or char == "_" or isNumeric(char) or char == " " :
        return True
    return False


def get_start_of_statement(line, start_var):
    while is_char_part_of_statement(line[start_var]) == True:
        start_var = start_var - 1

    operator = line[start_var - 1: start_var + 1]
    if operator == "==" or operator == "!=" :
        start_var = start_var - 1
        while is_char_part_of_statement(line[start_var-1]) == True:
            start_var = start_var - 1
    
    return start_var


def get_end_of_statement(line, end_var):
    if len(line) > end_var :
        while line[end_var] == " " :
            end_var = end_var + 1
        after = line[end_var:end_var + 2]
        if after == "&&" or after == "||" :
            end_var = end_var + 2
    return end_var


def processFile(cData, varToBeRemoved):
    changed_file = []

    for line in cData:
        line_was_empty = line.strip() == ""
        line_is_empty = False
        skipline = False
        var_matched, start_var, end_var = variable_matched(line, varToBeRemoved)

        if var_matched == True :
            if varToBeRemoved == "BS_Hornet" :
                pass
            recalculate_start_end, start, end = is_variable_in_paranthesis(line, end_var, varToBeRemoved)    

            if recalculate_start_end == True :
                start_statement = start
                end_statement = end
            else :
                start_statement = get_start_of_statement(line, start_var)
                end_statement = get_end_of_statement(line, end_var)

            line = line[:start_statement] + line[end_statement:]
            if "&&" == line.strip() or  "||" == line.strip():
                skipline = True
            else :
                tmp_line = line[start_statement-1:].strip()
                if "&&" == tmp_line or "||" == tmp_line :
                    line = line[:start_statement-1]
            line = line.rstrip()
            line_is_empty = line.strip() == ""

        if skipline == False:
            if line_is_empty == True :
                if line_was_empty == True :
                    changed_file.append(line.rstrip("\n"))
            else :
                changed_file.append(line.rstrip("\n"))

                    
    return changed_file


def removeCase(cData, enumIdx) :
    skipLine = False
    fCase = 'case ' + enumIdx + ':'

    changed_file = []
    for idx in range(len(cData)):
        if cData[idx].find(fCase) != -1:
            skipLine = True
            continue

        if cData[idx].find("break;") != -1 and skipLine == True:
            skipLine = False
            continue

        if cData[idx].find("default") != -1 and skipLine == True:
            skipLine = False

        if re.search(REGEX_CASE_LINE_MATCH, cData[idx]) is not None :
            skipLine = False

        if not skipLine:
            changed_file.append(cData[idx].rstrip("\n"))
    return changed_file

