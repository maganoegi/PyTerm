

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
#             else:
#                 pre = 
#             print('{}{}{}'.format(pre + subindent + preindent, post, f))
        
