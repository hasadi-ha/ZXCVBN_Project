import os
from zxcvbn import zxcvbn
import time
from hashlib import sha1


def hashInput(inputData):
    inputData = inputData.encode("utf-8")
    hash_object = sha1(inputData)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def runSearch(inputFile, currentIndexFirst, currentIndexSecond):
    # instantiate storage lists
    results = []
    errorLoc = []

    # Begin count variable to uid
    count = 0

    # Start timer to know how long process took
    start = time.time()

    # Open file for reading from (Change based on if .txt is present or not by uncommenting)
    # fileIn = open(inputFile + str(currentIndexFirst) +
    #               str(currentIndexSecond).zfill(2) + ".txt", "r")
    fileIn = open(inputFile + str(currentIndexFirst) +
                  str(currentIndexSecond).zfill(2), "r")

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
            print("***** ERROR: __Remove & Strip__ FAIL at location: " +
                  str(count) + " :ERROR *****\n")

            # Add the location and reason for fail to errorLoc list
            errorLoc.append(
                "***** ERROR: __Remove & Strip__ FAIL at location: " +
                str(count) + " :ERROR *****"
            )

            # Continue on with loop since fail recorded
            continue

        # Try-Except for analyzing line through ZXCVBN
        try:
            # Tester to see what ZXCVBN says
            # print(zxcvbn(line))

            # Send to zxcvbn to get decryption results from
            results.append(zxcvbn(line))

            if count % 20000 == 0:
                end = time.time()
                print("\nAnalyzed " + str(count) + " passwords")
                print("@" + str(round(end - start, 3)) + " seconds\n")

        except:
            # Alert user
            print("***** ERROR: __ZXCVBN__ FAIL at location: " +
                  str(count) + " :ERROR *****\n")

            # Add the location and reason for fail to errorLoc list
            errorLoc.append(
                "***** ERROR: __ZXCVBN__ FAIL at location: " + str(count) + " :ERROR *****")

            # Continue on with loop since fail recorded
            continue

    # # Print out any errors for alerting user at end
    # print(errorLoc)

    # Stop using file
    fileIn.close()

    # Create output file title and location
    cwdOutputGen = ("output_data" +
                    str(currentIndexFirst) + str(currentIndexSecond) + ".txt")
    cwdOutputSHA = ("output_data_SHA" +
                    str(currentIndexFirst) + str(currentIndexSecond) + ".txt")

    # Start an output file to write to
    fileGeneralOut = open(cwdOutputGen, "w+")
    fileSHAOut = open(cwdOutputSHA, "w+")

    # Reset counter since resulsts loop already used it
    count = 0

    for i in results:
        # Setup counting by adding 1 each time there is a new result to output
        count += 1

        # Remove any result that is too weak to be useful for goal
        if i["guesses_log10"] < 8:
            # If result unuseful, move on to next
            continue

        try:
            # Acquire the hash for the password and remove spaces from array
            shaHash = hashInput(i["password"])

        except:
            # Alert user to fail in hashing
            print("***** ERROR: __ZXCVBN__ FAIL at location: " +
                  str(count) + " :ERROR *****\n")

            # Print out error in file
            shaHash = "error"

        # Error check
        # print("Password:," + i["password"].strip("\n") + "," + "Guesses_Log10:," + str(
        #     i['guesses_log10']) + "," + "Score:," + str(i["score"]) + "," + "uid:," + str(count) + ",\n")

        # Write to outputGen file using each line as new password and data about it
        # Also using a comma as a delimiter for possible conversion into excel sheet
        fileGeneralOut.write(
            "SHA1:,"
            + str(shaHash)
            + ","
            + "Password:,"
            + i["password"].strip("\n")
            + ","
            + "Guesses_Log10:,"
            + str(i["guesses_log10"])
            + ","
            + "uid:,"
            + str(count)
            + ",\n"
        )

        # Write to outputSHA file using each line as new SHA and frequency of it
        # Also using a comma as a delimiter for possible conversion into excel sheet
        fileSHAOut.write(
            "SHA1:,"
            + str(shaHash)
            + ","
            + "Frequency:,"
            + "1,\n"
        )

    # Loop to write all errors to file as well at bottom
    for i in errorLoc:
        # Write particular error to file
        fileGeneralOut.write(i)

    # Stop using file
    fileGeneralOut.close()
    fileSHAOut.close()

    # End time counter
    end = time.time()

    # Print out time result to alert user
    print("* Analysed Piece File #" +
          str(currentIndexSecond + 1) + " *")
    print("Finished @" + str(round(end - start, 3)) + " seconds\n")


if __name__ == "__main__":
    # Instruct user on how the program will read data
    print("\n\n ** To make this work, you need to first make sure that each file is broken up how you want. An example name for a broken up piece could be x000. MAKE SURE TO FOLLOW THIS NAMING STANDARD! Start name with x000 and go on with that. So one set for one master file could be x000 x001 x002 and the next master file would be x100 x101 x102. DO NOT DEVIATE FROM THIS! ** \n\n")

    # Allow user to leave before program runs if they don't understand
    if (str(input("Do you understand? Enter Y/N: ")).lower() != "y"):
        print("\n**** EXITING NOW ****\n")
        exit()

    print("\n")

    # User input for name of input data file
    inputFileName = str(
        input("Enter name of input data file (don't include final index nor .txt): "))

    print("\n")

    # User input for how many master files will be there
    inputIndexAmountFirst = int(
        input("Enter how many master files there are: "))

    print("\n")

    # User input for how many pieces of files will be there
    inputIndexAmountSecond = int(
        input("Enter how many pieces there are to run through: "))

    print("\n")

    print("*************** ANALYSIS STARTING ***************\n")

    # For particular test case
    # Need to go one up to retrieve input_data files
    os.chdir("..")

    for x in range(0, inputIndexAmountFirst):
        print("* Analyzing Master File #" + str(x + 1) + " *\n")
        for y in range(0, inputIndexAmountSecond):
            print("* Analyzing Piece File #" + str(y + 1) + " *\n")
            runSearch(inputFileName, x, y)
        print("* Finished Analyzing Master File #" + str(x + 1) + " *\n")

print("*************** ANALYSIS COMPLETE ***************\n")
