


import commands as cmd # as to not touch any reserved keywords
import std
import os
import json


# Color Variables
BOLD = "\033[1m"
CYAN = "\033[96m"
RED = "\033[91m"
END = "\033[00m"

def make_words_array(line):
    return line.split()

def nextArgExists(i_now, array):
    target = i_now + 1
    return (target < len(array)) and target >= 0 

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

def isNotArgumented(words):
    contains_arguments = nextArgExists(0, words)
    std._err_ = "Please provide at least one argument\n See bash --help" if not contains_arguments else ""
    return not contains_arguments


def process_following_words(words, callback = None, rm_recursion_flag = None):
    i = 0
    content = ""
    while nextArgExists(i, words):
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
                content += next_word + " "

            i += 1

    return i, content

def count_flags(words):
    qty_flags = 0
    flags = []
    for i in range(len(words)):
        if nextArgExists(i, words) and words[i+1][0] == "-" and len(words[i+1]) > 1:
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

def parse_words(words):
    
    i = 0
    while i < len(words):

        # check whether any aliases are valid
        aliases = getAliases()
        word = words[i] if words[i] not in aliases.keys() else aliases[words[i]]


        if word == "exit": 
            cmd.exit()

        elif word == "pwd": 
            std._out_ = cmd.pwd()
        
        elif word == "cd":
            if isNotArgumented(words[i:]): break
            cmd.cd(words[i + 1])
            i += 1
        
        elif word == "mkdir":
            if isNotArgumented(words[i:]): break
            cmd.mkdir(words[i + 1])
            i += 1
        
        elif word == "rm":
            j = i
            
            # checks for -r flag
            isRecursive = nextArgExists(j, words) and words[j + 1] == "-r"
            
            # moves the "cursor" past the -r flag  
            if isRecursive: 
                j += 1 
                i += 1

            if isNotArgumented(words[j:]): break

            incr, std._out_ = process_following_words(words[j:], cmd.rm, isRecursive)

            i += incr 
            
        
        elif word == "mv": # TODO: path validation
            # Checks whether both SOURCE and DESTINATION mentionned and are valid
            if not (nextArgExists(i, words) and nextArgExists(i+1, words)):
                std._err_ = "Please respect the following format: mv SOURCE DESTINATION"
                break
            
            source = words[i+1]
            destination = words[i+2]
            cmd.mv(source, destination)

            i += 2
        
        elif word == "ls":
            containsPermissions = nextArgExists(i, words) and words[i + 1] == "-l"
            
            std._out_ = cmd.ls(containsPermissions)

            if containsPermissions:
                i += 1

        elif word == "echo":
            incr, std._out_ = process_following_words(words[i:]) 
            i += incr


        elif word == "cat":
            if isNotArgumented(words[i:]): break
            incr, std._out_ = process_following_words(words[i:], cmd.cat)
            i += incr

        elif word == "touch":
            if isNotArgumented(words[i:]): break
            incr, std._out_ = process_following_words(words[i:], cmd.touch)
            i += incr

        elif word == "cp":
            
            # checks for -r flag
            isRecursive = nextArgExists(i, words) and words[i + 1] == "-r"
            
            # moves the "cursor" past the -r flag  
            if isRecursive: 
                i += 1

            # Checks whether both SOURCE and DESTINATION mentionned and are valid
            if not (nextArgExists(i, words) and nextArgExists(i+1, words)):
                std._err_ = "Please respect the following format: cp [-r] SOURCE DESTINATION"
                break
            
            source = words[i+1]
            destination = words[i+2]
            cmd.cp(source, destination, isRecursive)

            i += 2
        
        elif word == "wc":
            flags = {'l': False, 'w': False, 'c': False}

            # check how many flags and return them
            qty_flags, extracted_flags = count_flags(words[i:])
            i += qty_flags
            if isNotArgumented(words[i:]): break

            # analyze the extracted flags - if found, change status
            if qty_flags > 0:
                possible_flags = flags.keys()
                for extracted_flag in extracted_flags:
                    for c in extracted_flag[1:]:
                        if c in possible_flags:
                            flags[c] = True
                        else:
                            std._err_ = "Invalid flag encountered for wc command: {}".format(c)
                            break
                if std._err_ != "": break
            # no flags - activate all
            elif qty_flags == 0 and words[i + 1] != ">" and words[i + 1] != "|":
                for flag in flags: flags[flag] = True
            else:
                std._err_ = "Please respect the following format: wc [-l] [-w] [-c] [-wlc] FILENAME"
                break
            
            i += 1

            # Depending on the active flags, return the count 
            data = std._in_ if std._in_ != "" else words[i]
            l, w, c = cmd.wc(data)# TODO: FIND OUT WHY FLAGS SEPARATELY-DIFF OUTPUT
            for flag in flags:
                if flags[flag]:
                    name = ": "
                    if flag == 'l': name = "Lines" + name + str(l)
                    if flag == 'w': name = "Words" + name + str(w)
                    if flag == 'c': name = "Chars" + name + str(c)
                    std._out_ += name + " "
            std._out_ += "\t" + words[i] + "\n"


        elif word == "alias":
            error_msg = "Please Respect the following format = alias WORD=COMMAND"
            if isNotArgumented(words[i:]): break
            subargs = words[i+1].split("=")
            if len(subargs) != 2:
                std._err_ = error_msg
                break
            else:
                alias = subargs[0]
                command = subargs[1]
                cmd.alias(alias, command)
            i += 1
        
        elif word == "tree": # TODO: tree
            cmd.pwd()
            if nextArgExists(i, words):
                cmd.cd(words[i + 1])
                i += 1
            path = std._out_
            cmd.tree(path)
        
        elif word == "find": # TODO: find
            pass
        
        elif word == "grep": # TODO: grep
            pass
        
        elif word == "same":
            if not (nextArgExists(i, words) and nextArgExists(i+1, words)):
                std._err_ = "Please respect the following format: same FILE1 FILE2"
                break
            
            first = words[i+1]
            second = words[i+2]
            std._out_ = cmd.same(first, second)

            i += 2
        
        elif word == "duplicate": 
            if isNotArgumented(words[i:]): break # TODO: include errorMessage into isNotArgumented() calls
            results = cmd.duplicate(words[i + 1])
            print(results)
            res_string = ""
            for result in results:
                res_string += str(result[-1]) + " "
                for k in range(len(result) - 1):
                    res_string += result[k] + " "
                res_string += "\n"



            std._out_ = res_string
            i += 1
        
        elif word == "|":
            std._in_ = std._out_
        
        elif word == ">":
            if isNotArgumented(words[i:]): break
            content = std._out_
            cmd.touch(words[i + 1], content)
            i += 1


        elif word == ";": # TODO: separator
            pass  

        elif word == "all-cmd":
            print("exit\npwd\ncd\nmkdir\nrm\nmv\nls [-l]\necho\ncat\ntouch\ncp\nwc\nalias\ntree\nfind\ngrep\nsame\nduplicate\n|\n>\n;\n")        

        else:
            std._err_ = "Invalid Command: {}\n".format(word)
            break
        
        i += 1
