import os
from zxcvbn import zxcvbn
import multiprocessing

# Make first list
results = []

index = 0


def runSearch(inputFile, currentIndex):
    # Open file for reading from
    file = open(inputFile + str(currentIndex) + ".txt", "r")

    for line in file:
        line = line[41:].strip()
        # print(line)

        # Send to zxcvbn to get decryption results from
        results.append(zxcvbn(line))

    # Stop using file for good practice
    file.close()

    cwdOutput = "output_data" + currentIndex + ".txt"

    # Start an output file to write to
    file = open(cwdOutput, "w+")

    # To make uid
    count = 0

    for i in results:
        # Setup counting by adding 1 each time there is a new result to output
        count = count + 1

        if (i['guesses_log10'] < 8):
            continue

        # Write to output file using each line as new password and data about it
        # Also using a comma as a delimiter for possible conversion into excel sheet

        file.write("Password:," + i["password"].strip("\n") + "," + "Guesses_Log10:," + str(
            i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid:," + str(count) + ",\n")

    # Stop using file for good practice
    file.close()


if __name__ == '__main__':
    # # User input for name of input data file
    inputFileName = str(input(
        "Enter name of input data file (don't include final index nor .txt): "))

    inputIndexAmount = int(input("Enter how many files to run through: "))

    # Get location for input
    # cwdInput = "input_data_example.txt"

    for i in range(inputIndexAmount):
        p = multiprocessing.Process(
            target=runSearch, args=(inputFileName, inputIndexAmount))
        p.start()
