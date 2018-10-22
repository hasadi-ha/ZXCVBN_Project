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
    # print(line[y:])
    # Send to zxcvbn to get decryption results from
    results.append(zxcvbn(line[hashSize:], user_inputs=['irrelevant', 'irrelevant']))

# Stop using file for good practice
file.close()

# Start an output file to write to
file = open(cwdOutput, "w+")

for i in results:
    # Write to output file using each line as new password and data about it
    # Also using a comma as a delimiter for possible conversion into excel sheet
    file.write("Password:," + i["password"].strip("\n") + "," + "Guesses Log10:," + str(i['guesses_log10']) + "," + "Score:," + str(i["score"]) + ",\n")

# Stop using file for good practice
file.close()
