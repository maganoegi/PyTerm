

import sys
import os
import lib
import std
import json
import re

def pwd():
    return os.getcwd()


def exit():
    print("\nExiting PyUnix, goodbye!")
    sys.exit()


def cd(path):
    try:
        os.chdir(path)
    except FileNotFoundError():
        std._err_ = "Invalid Path: {}".format(path)
    except PermissionError():
        std._err_ = "You Do Not Have Permission To Access: {}".format(path)
    except NotADirectoryError():
        std._err_ = "{} Is Not A Directory".format(path)


def mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        std._err_ = "Directory Already Exists: {}".format(path)


def cp(source, destination, recursive):
    if recursive:
        if os.path.isdir(source):
            # create a copy of current directory
            base_source = os.path.abspath(source)
            mkdir(destination)
            base_destination = os.path.abspath(destination)

            # Analyze the contents of the dir
            items = os.listdir(base_source)
            for item in items:
                # Copy the contents recursively
                new_path_source = base_source + "/" + item
                new_path_dest = base_destination + "/" + item
                cp(new_path_source, new_path_dest, True)

        else:
            touch(destination, cat(source))
    else:
        touch(destination, cat(source))

def mv(source, destination):
    # extract the contents of the source file
    file2read = open(source, "r")
    content = file2read.read()  
    file2read.close

    # create and write to the destination file
    file2write = open(destination, "w+")
    file2write.write(content)    
    file2write.close

    # delete the source file
    rm(source, False)

def rm(path, recursive):
    if recursive:
        if os.path.isdir(path):
            base_path = os.path.abspath(path)
            # Analyze the contents of the dir
            items = os.listdir(base_path)
            for item in items:
                # Attack the contents recursively
                new_path = base_path + "/" + item
                rm(new_path, True)

            # Once done, remove the base path
            os.rmdir(base_path)

        else:
            # In case a recursive call is called on a file
            os.remove(path)
    else:
        os.remove(path)


def ls(perm = False):
    items = os.listdir()
    dir_string = ""
    file_string = ""
    separator = lib.ENDLINE if perm else lib.SPACE
    for item in items:
        isDir = os.path.isdir(item)

        if perm:
            perm_val = str( oct( os.stat(item).st_mode ) )[-3:]
            perm_str = lib.permission_val_2_string(perm_val, isDir)
            item = perm_str + lib.SPACE + item


        if isDir:
            dir_string += item + "/" + separator
        else:
            file_string += item + separator

    output = dir_string + file_string

    if not perm: output+= lib.ENDLINE
    return output


def touch(path, content = None):
    mode = 'a'
    if content and len(content) > 0:
        mode = 'w'

    with open(path, mode) as f:
        if mode == 'w':
            f.write(content)

        f.close()

def cat(path):
    content = ""
    with open(path, 'r') as f:
        content = f.read()
        f.close()
    return content

def wc(path, std = False):
    l_count = 0
    w_count = 0
    c_count= 0
    # if std:
    with open(path, 'r') as file:
        for line in file:
            l_count += 1
            words = line.split()
            for char in line:
                c_count += 1
            for word in words:
                w_count += 1
        file.close()
    return l_count, w_count, c_count

def alias(word, command):
    aliases = ""
    path = ".platonovrc"
    # extract existing
    with open(path, 'r') as file:
        aliases = json.load(file)
        file.close()

    # append new
    aliases[word] = command

    # write updated
    with open(path, 'w') as file:
        json_aliases = json.dumps(aliases)
        file.write(json_aliases)
        file.close()


def same(first_path, second_path):
    # extract the contents of the first_path file
    firstFile = open(first_path, "r")
    first_content = firstFile.read()  
    firstFile.close

    # extract the contents of the second_path file
    secondFile = open(second_path, "r")
    second_content = secondFile.read()  
    secondFile.close

    # compare the two
    return first_content == second_content 


def duplicate(basePath):
    # initialization
    paths = []

    ignored = 0

    lines = []
    words = []
    chars = []

    matches = []
    myRoot = os.path.abspath(basePath)
    rootlen = len(myRoot)
    # get the paths, contents, lengths of all the files in the arborescence
    for root, dirs, files in os.walk(myRoot):
        for file_path in files:
            path = os.path.abspath(root) + "/" + file_path
            
            try:
                f = open(path, "r")
                content = f.read()
                paths.append(path)

                nb_lines, nb_words, nb_chars = wc(path)
                lines.append(nb_lines)
                words.append(nb_words)
                chars.append(nb_chars)

                f.close()

            except: # if files cannot be parsed by .read() - we skip them.
                ignored += 1
                pass 


    validated = [False] * len(lines) # allows us to avoid double recalculation and double results
    for i in range(len(lines) - 1):
        if not validated[i]:
            nb_matched = 0
            similar = [ (paths[i])[rootlen:] ]
            for j in range(i+1, len(lines)):
                if not validated[j]:
                # once nb_lines match, we compare the nb_words, and if those match, we see the nb_characters
                    if lines[i] == lines[j]:
                        if words[i] == words[j]:
                            if chars[i] == chars[j]:
                                # open those files again with same function() - saves stack space for big requests
                                # think is to be valid since we only do that for potential matches
                                if same(paths[i], paths[j]):
                                    nb_matched += 1
                                    validated[i] = True
                                    validated[j] = True
                                    similar.append((paths[j])[rootlen:])
            if nb_matched > 0:
                similar.append(len(similar)) 
                matches.append(similar)

    return matches

def grep(regex, path):
    pattern = regex
    result = ""

    f = open(path, "r")
    for line in f:
        lineContains = re.search(regex, line)
        if lineContains: result += line
    f.close()
    return result
    std._err_ = "Invalid Path: {}".format(path) 


def find(regex, path):
    myRoot = os.path.abspath(path)
    rootlen = len(myRoot)

    result = ""

    for root, dirs, files in os.walk(path):
        for file_path in files:
            pathContains = re.search(regex, file_path)
            if pathContains: result += (root + "/" + file_path + lib.ENDLINE)
    
    return result


def getPrefix(isLast, middleModifiers):
    # different symbols used in tree generation
    T = "├"
    L = "└"
    I = "│"
    B = "─"

    prefix = ""
    middle_prefix = (I + 3 * lib.SPACE)
    outer_prefix = (4 * lib.SPACE)

    for l in range(len(middleModifiers)):
        has_element_behind_it = middleModifiers[l]
        if has_element_behind_it:
            prefix += middle_prefix
        else:
            prefix += outer_prefix

    return prefix + (L if isLast else T) + (2 * B) + lib.SPACE


def tree(path, middleModifiers):
    result = ""

    # avoid listing folders which need permissions
    try:
        myMods = middleModifiers # allow us to track what's "behind" the sub-item: allows us to assemble the right prefix
        raw_contents = os.listdir(path)
        contents = []
        
        # avoids listing files and directories that start with . ( .gitignore, .bashrc, .git, etc...)
        for rc in raw_contents:
            if rc[0] != ".":
                contents.append(rc)


        if len(contents) != 0:
            for i in range(len(contents)):
                current_item = contents[i]
                current_path = os.path.join(path, current_item) 

                # checks where the current sub-element is with relation to its peers position-wise:
                # if he has other elements behind it, or not
                # NOTE: relations are visible with bigger trees
                isLast = i == (len(contents) - 1)
                isFirst = (i == 0)
                isMiddle = False # just for init - keeps the value if the sub-element is alone in a dir

                
                if len(contents) > 2: # when 3 or more elements, last one does not have to be connected to the one under it
                    isMiddle = not isLast
                elif len(contents) == 2: # same for 2 elements
                    isMiddle = isFirst


                if os.path.isdir(current_path):
                    # when the item is a directory, we print IT, and recursively ITS contents...
                    result += getPrefix(isLast, myMods) + lib.BOLD + current_item + lib.END + lib.ENDLINE

                    futureMods = myMods.copy()
                    futureMods.append(isMiddle)
                    result += tree(current_path, futureMods)
                else:
                    # and the regular files are printed normally
                    result += getPrefix(isLast, myMods) + current_item + lib.ENDLINE
    except:
        pass

    return result
    