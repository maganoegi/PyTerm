
from inputHandler import *
from commands import *
import std

# Imported Code Sources:
# https://stackoverflow.com/questions/12654772/create-empty-file-using-python

if __name__ == '__main__':

    startup_message()

    while True:

        reset_std_vars()

        line = input("?> ")

        words = make_words_array(line)

        parse_words(words)

        print_output()

