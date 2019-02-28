import os
from zxcvbn import zxcvbn
from multiprocessing import Process
import time
from hashlib import sha1


def hashInput(inputData):
    hash_object = sha1(inputData)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def runSearch(inputFile, currentIndex):
    # instantiate storage lists
    results = []
    errorLoc = []

    # Begin count variable to uid
    count = 0

    # Start timer to know how long process took
    start = time.time()

    # Open file for reading from (Change based on if .txt is present or not by uncommenting)
    fileIn = open(inputFile + str(currentIndex) + ".txt", "r")
    # file = open(inputFile + str(currentIndex), "r")

    # Run loop to read each line of file to run ZXCVBN against
    for line in fileIn:
        # Increment counter for creating identification
        count += 1

        # Try-Except for reading line
        try:
            # Removes the first 41 characters and any spaces
            # Using 41 because it is hash size + :
            line = line[41:].strip()
            # print(line)

        except:
            # Alert user
            print("***__Remove & Strip__ fail at location: " + str(count) + "***")

            # Add the location and reason for fail to errorLoc list
            errorLoc.append(
                "***__Remove & Strip__ fail at location: " + str(count) + "***")

            # Continue on with loop since fail recorded
            continue

        # Try-Except for analyzing line through ZXCVBN
        try:
            # Tester to see what ZXCVBN says
            # print(zxcvbn(line))

            # Send to zxcvbn to get decryption results from
            results.append(zxcvbn(line))

            if (count % 1000 == 0):
                print("Pass" + str(count))

        except:
            # Alert user
            print("***__ZXCVBN__ fail at location: " + str(count) + "***")
            # Add the location and reason for fail to errorLoc list
            errorLoc.append(
                "***__ZXCVBN__ fail at location: " + str(count) + "***")

            # Continue on with loop since fail recorded
            continue

    # Print out any errors for alerting user
    print(errorLoc)

    # Stop using file
    fileIn.close()

    # Create output file title and location
    cwdOutput = "output_data" + str(currentIndex) + ".txt"

    # Start an output file to write to
    fileGeneralOut = open(cwdOutput, "w+")

    # Reset counter since resulsts loop already used it
    count = 0

    for i in results:
        # Setup counting by adding 1 each time there is a new result to output
        count += 1

        # Remove any result that is too weak to be useful for goal
        if (i['guesses_log10'] < 8):
            # If result unuseful, move on to next
            continue

        # Error check print
        # print("Password:," + i["password"].strip("\n") + "," + "Guesses_Log10:," + str(
        #     i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid:," + str(count) + ",\n")

        # Write to output file using each line as new password and data about it
        # Also using a comma as a delimiter for possible conversion into excel sheet
        fileGeneralOut.write("Password:," + i["password"].strip("\n") + "," + "Guesses_Log10:," + str(
            i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid:," + str(count) + ",\n")

    # Loop to write all errors to file as well at bottom
    for i in errorLoc:
        # Write particular error to file
        fileGeneralOut.write(i)

    # Stop using file
    fileGeneralOut.close()

    # End time counter
    end = time.time()

    # Print out time result to alert user
    print(end - start)


if __name__ == '__main__':
    # User input for name of input data file
    inputFileName = str(input(
        "Enter name of input data file (don't include final index nor .txt): "))

    # User input for how many files will need a process assigned for it
    inputIndexAmount = int(input("Enter how many files to run through: "))

    # Test location for input
    # cwdInput = "input_data_example.txt"

    # For particular test case
    # Need to go one up to retrieve input_data files
    os.chdir("..")

    # Instantiate list of all running processes
    # Could be used
    # procs = []

    # A loop to create all processes depending on index amount
    for i in range(0, inputIndexAmount):
        # Opens up a single process running the search and passing arguments
        p = Process(
            target=runSearch, args=(inputFileName, i))

        # Could add processes to a list to check back on later
        # procs.append(p)

        # Starts off current process to run
        p.start()
