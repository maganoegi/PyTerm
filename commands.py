

import sys
import os
import inputHandler as ih
import std
import json

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
    separator = "\n" if perm else " "
    for item in items:
        isDir = os.path.isdir(item)

        if perm:
            perm_val = str( oct( os.stat(item).st_mode ) )[-3:]
            perm_str = ih.permission_val_2_string(perm_val, isDir)
            item = perm_str + " " + item


        if isDir:
            dir_string += item + "/" + separator
        else:
            file_string += item + separator

    output = dir_string + file_string

    if not perm: output+= "\n"
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
    result = "true" if first_content == second_content else "false"
    
    return result 


def duplicate(basePath):
    # initialization
    paths = []

    ignored = 0

    lines = []
    words = []
    chars = []

    potential_paths = []

    # get the paths, contents, lengths of all the files in the arborescence
    for root, dirs, files in os.walk("."):
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


    # get the "potential" matches by comparing the lengths
    for i in range(len(lines) - 1):
        similar = [ paths[i] ]
        for j in range(i+1, len(lines)):
            # once nb_lines match, we compare the nb_words, and if those match, we see the nb_characters
            if lines[i] == lines[j]:
                if words[i] == words[j]:
                    if chars[i] == chars[j]:
                        similar.append(paths[j])
                        potential_paths.append(similar)

        if len(similar) == 1: similar = []

    # print(potential_paths)
    # print("\n")

    # check the "potential" matches for real similarities
    # decided to open up those files again, in order to save stack space
    all_matches = []
    for potential_path in potential_paths:
        matches = [ potential_path[0] ]
        matches_for_this = 0
        comparator = potential_path[0]

        # f1 = open(potential_path[0], "r")
        # c1 = f1.read()
        # f1.close()
        for i in range(1, len(potential_path)):
            areSame = same(comparator, potential_path[i])
            if areSame == "true":
                matches_for_this += 1
                matches.append(potential_path[i])
      
        if matches_for_this != 0: 
            matches.append(matches_for_this)
            all_matches.append(matches)

    return all_matches


# def tree(path):
#     dirCount = 0
#     for root, dirs, files in os.walk(path):
#         level = root.replace(path, '').count(os.sep)
#         preindent = '├' if dirCount != 0 else ''
#         indent = ('─' * 4 * (level)) if dirCount != 0 else ''
        
#         basename = "." if level == 0 else (os.path.basename(root) + "/")

#         print('{}{}{}'.format(preindent + indent, "─" if dirCount != 0 else "", basename))
#         dirCount += 1
#         subindent = ' ' * 4 * (level)
#         for f in files:
#             pre = ""
#             post = "─ "
#             if level != 0 and dirCount: 
#                 pre = "│"
#                 if dirCount > 0:
#                     pre =  "├"
#             print('{}{}{}'.format(pre + subindent + preindent, post, f))
        
