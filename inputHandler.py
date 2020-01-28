


import commands as cmd # as to not touch any reserved keywords
import std
from lib import *
import os
import json



notArgumentedErrorMessage = "Not Enough Arguments. Please see README.md\n"

def parse_words(words):
    
    try:
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
                nextArgExists(i, words, notArgumentedErrorMessage)
                cmd.cd(words[i + 1])
                i += 1
            
            elif word == "mkdir":
                nextArgExists(i, words, notArgumentedErrorMessage)
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

                # if CheckIfArgumented(words[j:]): break

                incr, std._out_ = process_following_words(words[j:], cmd.rm, isRecursive)

                i += incr 
                
            
            elif word == "mv": # TODO: path validation
                # Checks whether both SOURCE and DESTINATION mentionned and are valid
                nextArgExists(i, words, "Please provide 2 arguments: SOURCE + DESTINATION")
                nextArgExists(i+1, words, "Please provide second argument: DESTINATION")
                
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
                nextArgExists(i, words, notArgumentedErrorMessage)
                incr, std._out_ = process_following_words(words[i:], cmd.cat)
                i += incr

            elif word == "touch":
                nextArgExists(i, words, notArgumentedErrorMessage)
                incr, std._out_ = process_following_words(words[i:], cmd.touch)
                i += incr

            elif word == "cp":
                
                # checks for -r flag
                isRecursive = nextArgExists(i, words) and words[i + 1] == "-r"
                
                # moves the "cursor" past the -r flag  
                if isRecursive: 
                    i += 1

                # Checks whether both SOURCE and DESTINATION mentionned and are valid
                nextArgExists(i, words, "Please five a SOURCE and DESTINATION")
                nextArgExists(i+1, words, "Please give a DESTINATION")
                
                source = words[i+1]
                destination = words[i+2]
                cmd.cp(source, destination, isRecursive)

                i += 2
            
            elif word == "wc":
                flags = {'l': False, 'w': False, 'c': False}

                # check how many flags and return them
                qty_flags, extracted_flags = count_flags(words[i:])
                i += qty_flags
                nextArgExists(i, words, notArgumentedErrorMessage)

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
                l, w, c = cmd.wc(data)
                for flag in flags:
                    if flags[flag]:
                        name = ": "
                        if flag == 'l': name = "Lines" + name + str(l)
                        if flag == 'w': name = "Words" + name + str(w)
                        if flag == 'c': name = "Chars" + name + str(c)
                        std._out_ += name + SPACE
                std._out_ += TAB + words[i] + ENDLINE


            elif word == "alias":
                error_msg = "Please Respect the following format = alias WORD=COMMAND"
                nextArgExists(i, words, error_msg)
                subargs = words[i+1].split("=")
                if len(subargs) != 2:
                    std._err_ = error_msg
                    break
                else:
                    alias = subargs[0]
                    command = subargs[1]
                    cmd.alias(alias, command)
                i += 1
            
            elif word == "tree":
                path = ""
                incr = 0

                doesNextExist = nextArgExists(i, words)

                if not doesNextExist or (doesNextExist and (words[i + 1] == ">" or words[i + 1] == "|")): # argumentless
                    path = "."
                else:
                    path = words[i + 1]
                    incr = 1

                std._out_ = path + ENDLINE + cmd.tree(path, [])
                i += incr
            
            elif word == "find":
                # Checks whether both REGEX and FILE mentionned and are valid
                nextArgExists(i, words, "Please respect the following format: find REGEX FILE")
                nextArgExists(i+1, words, "Missing the FILENAME argument")
                
                unPeeled, regEnd_index = extractRegex(words, i) # with ""
                
                if regEnd_index == 0: 
                    std._err_ = "Please respect the following format: find \"REGEX\" FILE"
                    break

                path = words[-1]
                isValid, peeled = regexValidation(unPeeled) # without ""
                
                if not isValid: 
                    std._err_  = "the regular expression is not valid. Please enclose the an expression to look for in simple or double quotes."
                    break
                
                std._out_ = cmd.find(peeled, path)

                i += 2 + regEnd_index
            

            elif word == "grep":
                # Checks whether both REGEX and FILE mentionned and are valid
                nextArgExists(i, words, notArgumentedErrorMessage)
                nextArgExists(i+1, words, notArgumentedErrorMessage)
                
                unPeeled, regEnd_index = extractRegex(words, i) # with ""
                
                if regEnd_index == 0: 
                    std._err_ = "Please respect the following format: grep \"REGEX\" FILE"
                    break

                path = words[-1]
                isValid, peeled = regexValidation(unPeeled) # without ""
                
                if not isValid: 
                    std._err_  = "the regular expression is not valid. Please enclose the an expression to look for in simple or double quotes."
                    break
                
                std._out_ = cmd.grep(peeled, path)

                i += 2 + regEnd_index

            
            elif word == "same":
                nextArgExists(i, words, notArgumentedErrorMessage)
                nextArgExists(i+1, words, notArgumentedErrorMessage)
                
                first = words[i+1]
                second = words[i+2]
                result = cmd.same(first, second)
                std._out_ = "true" if result else "false"

                i += 2
            
            elif word == "duplicate": 
                nextArgExists(i, words, notArgumentedErrorMessage)
                results = cmd.duplicate(words[i + 1])

                res_string = ""
                for result in results:
                    res_string += "Duplicates: " + str(result[-1]) + SPACE
                    for k in range(len(result) - 1):
                        res_string += result[k] + SPACE
                    res_string += ENDLINE

                std._out_ = res_string
                i += 1
            
            elif word == "|":
                std._in_ = std._out_
            
            elif word == ">":
                nextArgExists(i, words, notArgumentedErrorMessage)
                content = std._out_
                cmd.touch(words[i + 1], content)
                i += 1


            elif word == ";":
                pass  

            elif word == "all-cmd":
                print("exit\npwd\ncd\nmkdir\nrm\nmv\nls [-l]\necho\ncat\ntouch\ncp\nwc\nalias\ntree\nfind\ngrep\nsame\nduplicate\n|\n>\n;\n")        

            else:
                std._err_ = "Invalid Command: {}\n".format(word)
                break
            
            i += 1

    except NotArgumentedException as e:
        std._err_ += e.args[0]
    except FileNotFoundError:
        std._err_ += "Error: File not found."
    except PermissionError:
        std._err_ += "Error: Permission denied!"
    except FileExistsError:
        std._err_ += "Error: File already exists."
    except NotADirectoryError:
        std._err_ = "Error: argument is not a directory"
    except IsADirectoryError:
        std._err_ = "Error: this the file is a directory"
        
