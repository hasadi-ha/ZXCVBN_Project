### The purpose of this python file is to search through output
### and find similar words and take a count of them for
### for research purposes. This program will take into consideration
### leet words and account for it through code.

import os

# User input for name of input data file
# inputFileNamemaster = "\\" + str(input("Enter name of input data file (Don't include .txt): ")) + ".txt"
inputFileName = "\\tests\\" + str(input("Enter name of input data file (Don't include .txt): ")) + ".txt"

# Get location for input and output using os
cwdInput = str(os.getcwd()) + inputFileName

# Bring in file for reading and read the file for data
file = open(cwdInput, 'r')
inputData = file.read()
file.close()

# Seperate the word and put them inside a list
def tokenize():
    # Check if there is a word
    if inputData is not None:
        words = inputData.lower().split()
        return words
    else:
        return None
        
# Pull up the map that contains former words to begin counting
def map_inputData(tokens):
    hash_map = {}

    # Make sure something is in token
    if tokens is not None:
        for element in tokens:
            # Check for leet
            leet = str.maketrans('@361109$7', 'aegiloqst')
            word = str.translate(element, leet)

            # Word Exist?
            if word in hash_map:
                hash_map[word] = hash_map[word] + 1
            else:
                hash_map[word] = 1

        return hash_map
    else:
        return None


# Tokenize the Book
words = tokenize()

# Create a Hash Map (Dictionary)
map = map_inputData(words)

# Show Word Information
for word in map:
    print('Word: [' + word + '] Frequency: ' + str(map[word]))