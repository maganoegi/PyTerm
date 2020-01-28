


import commands as cmd # as to not touch any reserved keywords
import std
import os
import json

class NotArgumentedException(Exception):
    pass



# Color Variables
BOLD = "\033[1m"
CYAN = "\033[96m"
RED = "\033[91m"
END = "\033[00m"
ENDLINE = "\n"
TAB = "\t"
SPACE = " "

def make_words_array(line):
    return line.split()

def nextArgExists(i_now, array, message = None):
    target = i_now + 1
    exists = (target < len(array)) and target >= 0
    if not exists and message:
        raise NotArgumentedException(message)
    else: 
        return exists


def isPathValid(path):
    pass

def this_after_redirect_pipe(i, words):
    sentence_length = len(words)
    if next_x_ArgsExist(i, -2, words):
        print("Check")
    # if (i-1) >= 0:
    #     if words 

def permission_val_2_string(str, isDir = False):
    permission = "d" if isDir else "-"
    for i in range(3):
        val = int(str[i])

        if val >= 4:
            permission += "r"
            val -= 4
        else: permission += "-"

        if val >= 2:
            permission += "w"
            val -= 2
        else: permission += "-"

        if val >= 1:
            permission += "x"
        else: permission += "-"

    return permission

def startup_message():
    print("Unix-like shell project")
    print("Author:\t\t {}Sergey Platonov{}".format(BOLD, END))
    print("Professor:\t {}Adrien Lescourt{}".format(BOLD, END))
    print("{}{}2019-2020\tHEPIA, Geneva, CH\tITI 3 semester{}".format(RED, BOLD, END))
    print("For supported commands, type all-cmd")
    print("__________________________________________\n")

def print_output():
    if std._err_ != "":
        print("{} {}{}".format(RED, std._err_, END))
    elif std._out_ != "": print(std._out_)

def reset_std_vars():
    std._in_ = ""
    std._out_ = ""
    std._err_ = ""



def process_following_words(words, callback = None, rm_recursion_flag = None):
    i = 0
    content = ""
    while nextArgExists(i, words, ""):
        j = i+1
        next_word = words[j]

        if next_word == ">" or next_word == "|":
            break
        else:
            if callback: 
                func_name = callback.__name__
                if func_name == "rm":
                    callback(next_word, rm_recursion_flag)
                elif func_name == "touch":
                    callback(next_word, None)
                else: # cat 
                    content += callback(next_word)
            else: # echo 
                content += next_word + TAB

            i += 1

    return i, content

def count_flags(words):
    qty_flags = 0
    flags = []
    for i in range(len(words)):
        if nextArgExists(i, words, "") and words[i+1][0] == "-" and len(words[i+1]) > 1:
            qty_flags += 1
            flags.append(words[i+1])
        else: 
            break
    return qty_flags, flags

def getAliases():
    aliases = ""
    path = std.root + "/.platonovrc"
    if not os.path.isfile(path):
        cmd.touch(path, "{}")
    # extract existing
    with open(path, 'r') as file:
        aliases = json.load(file)
        file.close()
    return aliases

def regexValidation(regex):
    doubleQuote = "\""
    simpleQuote = "'"

    # control variables
    validLength = len(regex) > 1
    hasDoubleQuotes = validLength and (regex[0] == doubleQuote) and (regex[-1] == doubleQuote)
    hasSimpleQuotes = validLength and (regex[0] == simpleQuote) and (regex[-1] == simpleQuote)

    isValid = validLength and (hasDoubleQuotes or hasSimpleQuotes)

    content = ""
    if isValid:
        content = regex[1:-1] # strip the quotes
    
    return isValid, content


def extractRegex(words, i):
    regEnd_index = 0

    # allows us to find the end of the regular expression.
    # further error handling later on in the process
    for l in range(i+1, len(words) - 1):
        last_char = words[l][-1]
        if last_char == "\"" or last_char == "'":
            regEnd_index = l
            break

    unPeeled = TAB.join(words[i+1: regEnd_index + 1])

    return unPeeled, regEnd_index

