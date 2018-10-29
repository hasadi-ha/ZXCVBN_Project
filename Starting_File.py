#*********** WARNING ***********#
# This version of the starting file has a bug
# where adding 5 or more numbers to the end of the
# array will make ZXCVBN crash. Unsure why.
# It will only work if input file only has that single
# password it wants to check. Still searching for issue!

import os
from zxcvbn import zxcvbn
from zxcvbn.matching import add_frequency_lists

add_frequency_lists({
    ##### INSERT DICTIONARY WORDS HERE TO IMPROVE BREAKING SPEEDS #####
    'my_list': ['carolina', 'Carolina', 'tarheel', 'Tarheel'],
})

# Make first list
results = []

# User input for name of input data file
inputFileName = "\\" + str(input("Enter name of input data file (Don't include .txt): ")) + ".txt"

# Get location for input and output using os
cwdInput = str(os.getcwd()) + inputFileName
cwdOutput = str(os.getcwd()) + "\output_data.txt"

# Open file for reading from
file = open(cwdInput, "r")

# Ask user for input on amount of lines and character size to ignore
#fileLinesCount = int(input("Enter amount of lines in file: "))
hashSize = int(input("Enter amount of characters in  hash (i.e. NTLM have 30 [I think] characters in their hash): "))

for line in file:
    # print(line[hashSize:])
    # Send to zxcvbn to get decryption results from
    results.append(zxcvbn(line[hashSize:], user_inputs=['irrelevant', 'irrelevant']))

# Stop using file for good practice
file.close()

# Start an output file to write to
file = open(cwdOutput, "w+")

# To make uid
count = 0

for i in results:
    # Setup counting by adding 1 each time there is a new result to output
    count = count + 1
    # Write to output file using each line as new password and data about it
    # Also using a comma as a delimiter for possible conversion into excel sheet

    file.write("Password:," + i["password"].strip("\n") + "," + "Guesses Log10:," + str(i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid: ," + str(count) + ",\n")

# Stop using file for good practice
file.close()
