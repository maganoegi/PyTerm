
from lib import *
from inputHandler import *
from commands import *
import std

# Imported Code Sources:
# https://stackoverflow.com/questions/12654772/create-empty-file-using-python

if __name__ == '__main__':

    startup_message()
    std.root = os.getcwd()

    while True:

        reset_std_vars()

        _input_ = input("?> ")
        
        lines = split_lines(_input_)

        for line in lines:
            words = make_words_array(line)

            parse_words(words)

            print_output()



