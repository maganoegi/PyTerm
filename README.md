
# Basic UNIX Shell with Python3
## Author: Sergey Platonov 
ITI 3rd semester, HEPIA, Geneva
System Dev Class with Adrien Lescourt

# Introduction
This project was done as a part of the SysDev class taught by Adrien Lescourt. The goal was to gain a deeper understanding of the UNIX Shell by implementing a basic version of it ourselves.

# Setup
The Shell is coded with Python3. Import the project with the following command:
```bash
git clone https://github.com/maganoegi/PyTerm.git
```
Next, you shall see the following files:
```
* commands.py           # bash commands definitions
* inputHandler.py       # input parsing functions definitions
* pyUnix.py             # main driver file
* README.md             # this file
* std.py                # config-style file with stdin, stdout, stderr globals
```
To start the shell, use execute __pyUnix.py__ with python3:
```bash
python3 pyUnix.py
```

You will see the following prompt (here used with __ls -l__ command):
```
Unix-like shell project
Author:		 Sergey Platonov
Professor:	 Adrien Lescourt
2019-2020	HEPIA, Geneva, CH	ITI 3 semester
For supported commands, type all-cmd
__________________________________________

?> ls -l
-rw-r--r-- README.md
-rw-r--r-- std.py
-rw-r--r-- .platonovrc
-rw-r--r-- pyUnix.py
-rw-r--r-- inputHandler.py
-rw-r--r-- commands.py

?> 
```

# General Organisation
The information flows in the following fashion:
```c
    +------------------------+
    | pyUnix.py              |
    +------------------------+
    | while True:            |
    |    wait for user input |
    |    split into words    |
+------+ parse words         |
|   |    print stdout/stderr <-----------------------+
|   +------------------------+                       |
|                                                    |
|                                                    |
|   +-------------------------------------------+    |
|   | inputHandler.py                           |    |
|   +-------------------------------------------+    |
|   | for each word:                            |    |
|   |   check if aliases exist                  |    |
|   |   check whether a word is a command       |    |
+--->      execute command                      |    |
|   |      update global stdin, stdout, stderr  <----+
|   +-------------------------------------------+    |
|                                                    |
|                                                    |
|                                                    |
|   +--------------------+            +---------+    |
|   | commands.py        |            | std.py  |    |
|   +--------------------+            +---------+    |
+--->      command       +------------>  stdin  +----+
    +--------------------+      +----->  stdout |---+
                                 +---->  stderr +--+
                                      +---------+
```
Another file, __.platonovrc__, imitates the function of __.bashrc__. It is generated upon first execution of the script, and contains _aliases_ in a __json__ format.

# Commands
Here is a list of commands that my shell supports, as well as a short description and possible configurations. __Note: since this is not a fully implemented shell! It has its limitations.__

* __exit:__ exits the shell 
* __pwd:__ returns the current working directory 
* __cd:__ changes directory
    * ``` cd PATH ``` 
* __mkdir:__ creates an empty directory
    * ``` mkdir PATH ```
* __rm:__ removes a file. Use the __-r__ flag to delete a directory recursively (meaning all of its contents).
    * ``` rm FILE ```
    * ``` rm -r DIRECTORY ```
* __mv:__ moves a file to a given path. Is also used to rename objects.
    * ``` mv SOURCE DESTINATION ```
* __ls:__ lists the contents of the current working directory. Use the __-l__ flag to also display the permissions of the files.
    * ``` ls [-l]```
* __echo:__ prints a message to the terminal.
    * ``` echo PARAM ```
* __cat:__ prints the contents of a file to the terminal.
    * ``` cat FILE ```
* __touch:__ creates a regular, empty file.
    * ``` touch PATH ```
* __cp:__ copies the contents of a file into another. Use the __-r__ flag to copy a directory recursively (meaning all of its contents).
    * ``` cp FILE DESTINATION ```
    * ``` cp -r DIRECTORY DESTINATION ```
* __wc:__ counts the lines/words/characters in a given file. Controlled with __-l, -w, -c__ flags respectively. My implementation allows for the same degree of freedom as bash (see below). If no flags used, all are activated.
    * ``` wc FILE ```
    * ``` wc -l -w -c FILE ```
    * ``` wc -lwc -lc FILE ```
    * ``` wc -lw -c FILE ```
* __alias:__ creates a nickname WORD for a COMMAND. Saved in __.platonovrc__, generated when first launched.
    * ``` alias WORD=COMMAND ```
* __tree:__ prints a tree representation of the contents of the current directory and its child elements.
    * ``` tree PATH ```
* __find:__ finds recursively all files and directories that contain a regular expression in their name.
    * ``` find REGEX PATH```
* __grep:__ Prints all the lines that match the regular expression in a given file.
    * ``` grep REGEX FILE ```
* __same:__ tells us whether two files are identical.
    * ``` same FILE FILE ```
* __duplicate:__ displays the paths of identical files in the arborescence.
    * ``` duplicate PATH ```
#### Special Connectors
* __|__ allows to create a pipeline for stdout of one expression to the stdin of another.
    * ``` cat hello.txt | wc -c ```
* __>__ writes/redirects the stdout of an expression into a file
    * ``` ls -l > contents.txt ```
* __;__ allows for separation of independent expressions, written in one line 

