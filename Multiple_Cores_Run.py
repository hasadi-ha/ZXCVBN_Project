import os
from zxcvbn import zxcvbn
import multiprocessing
import time


def runSearch(inputFile, currentIndex):
    results = []
    start = time.time()
    count = 0
    errorLoc = []

    # Open file for reading from
    file = open(inputFile + str(currentIndex) + ".txt", "r")
    # file = open(inputFile + str(currentIndex), "r")

    for line in file:
        count += 1

        try:
            line = line[41:].strip()
            # print(line)
        except:
            errorLoc.append(
                "***__Remove & Strip__ fail at location: " + str(count) + "***")
            continue

        try:
            # Send to zxcvbn to get decryption results from
            # print(zxcvbn(line))

            results.append(zxcvbn(line))
        except:
            errorLoc.append(
                "***__ZXCVBN__ fail at location: " + str(count) + "***")
            continue

    # Stop using file for good practice
    print(errorLoc)
    file.close()

    cwdOutput = "output_data" + str(currentIndex) + ".txt"

    # Start an output file to write to
    file = open(cwdOutput, "w+")

    count = 0

    for i in results:
        # Setup counting by adding 1 each time there is a new result to output
        count += 1

        if (i['guesses_log10'] < 8):
            continue

        # Write to output file using each line as new password and data about it
        # Also using a comma as a delimiter for possible conversion into excel sheet
        # print("Password:," + i["password"].strip("\n") + "," + "Guesses_Log10:," + str(
        #     i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid:," + str(count) + ",\n")

        file.write("Password:," + i["password"].strip("\n") + "," + "Guesses_Log10:," + str(
            i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid:," + str(count) + ",\n")

    for i in errorLoc:
        file.write(i)

    # Stop using file for good practice
    file.close()

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    # # User input for name of input data file
    inputFileName = str(input(
        "Enter name of input data file (don't include final index nor .txt): "))

    inputIndexAmount = int(input("Enter how many files to run through: "))

    # Get location for input
    # cwdInput = "input_data_example.txt"

    os.chdir("..")

    # procs = []

    for i in range(0, inputIndexAmount):
        p = multiprocessing.Process(
            target=runSearch, args=(inputFileName, i))
        # procs.append(p)
        p.start()
