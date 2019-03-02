import os
import time
from hashlib import sha1
import psutil
from zxcvbn import zxcvbn


def hashInput(inputData):
    inputData = inputData.encode("utf-8")
    hash_object = sha1(inputData)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def runSearch(inputFile, currentIndexFirst, currentIndexSecond):
    # Attempt opening files for reading
    try:
        # Open file for reading from (Change based on if .txt is present or not by uncommenting)
        fileIn = open(inputFile + str(currentIndexFirst) +
                      str(currentIndexSecond).zfill(2) + ".txt", "r")
        # fileIn = open(inputFile + str(currentIndexFirst) +
        #               str(currentIndexSecond).zfill(2), "r")

    except:
        # Alert user of failure to open file
        print('***** ERROR: __OpenFile__ "' + inputFile+str(currentIndexFirst) +
              str(currentIndexSecond) + '" Does not exist :ERROR*****\n')

        # Exit file analysis
        return

    # Create output file title and location
    cwdOutputGen = ("output_data" +
                    str(currentIndexFirst) + str(currentIndexSecond) + ".txt")
    cwdOutputSHA = ("output_data_SHA" +
                    str(currentIndexFirst) + str(currentIndexSecond) + ".txt")

    # instantiate storage lists
    results = []
    errorLoc = []

    # Begin count variable to uid
    count = 0

    # Start an output file to write to
    fileGeneralOut = open(cwdOutputGen, "w+")
    fileSHAOut = open(cwdOutputSHA, "w+")

    # Start timer to know how long process took
    start = time.time()

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

        # Check for keyboard interrupt because try-except goes around it if not accounted for
        except KeyboardInterrupt:
            # Alert user
            print("KEYBOARD INTERRUPT DETECTED")
            print("\n**** EXITING NOW ****\n")

            # Leave Program
            exit()

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

            # Initialize jSON to store zxcvbn info
            data = {}

            # Get zxcvbn to analyze and place in temp complete value
            temp = zxcvbn(line)

            # Checks if 20,000 lines have been passed through
            if count % 20000 == 0:
                # Get end time to calculate current time
                end = time.time()

                # Alerts user about pass through
                print("\nAnalyzed " + str(count) + " passwords")
                print("@" + str(round(end - start, 3)) + " seconds")

                # Gets ID of current python program
                process = psutil.Process(os.getpid())

                # Alerts user of current memory usage
                print(
                    "* " + str(round(process.memory_info().rss / 1024/1024, 4)) + "MB *\n")

            # Remove any result that is too weak to be useful for goal
            if temp["guesses_log10"] < 8:
                # If result unuseful, move on to next
                continue

            # Parse through JSON and pull out necessary info
            data['password'] = temp['password']
            data['guesses_log10'] = temp['guesses_log10']

        # Check for keyboard interrupt because try-except goes around it if not accounted for
        except KeyboardInterrupt:
            # Alert user
            print("KEYBOARD INTERRUPT DETECTED")
            print("\n**** EXITING NOW ****\n")

            # Leave Program
            exit()

        except:
            # Alert user
            print("***** ERROR: __ZXCVBN__ FAIL at location: " +
                  str(count) + " :ERROR *****\n")

            # Add the location and reason for fail to errorLoc list
            errorLoc.append(
                "***** ERROR: __ZXCVBN__ FAIL at location: " + str(count) + " :ERROR *****")

            # Continue on with loop since fail recorded
            continue

        # Try-except for hasing attempt of password
        try:
            # Acquire the hash for the password and remove spaces from array
            shaHash = hashInput(data["password"])

        # Check for keyboard interrupt because try-except goes around it if not accounted for
        except KeyboardInterrupt:
            # Alert user
            print("KEYBOARD INTERRUPT DETECTED")
            print("\n**** EXITING NOW ****\n")

            # Leave Program
            exit()

        except:
            # Alert user to fail in hashing
            print("***** ERROR: __ZXCVBN__ FAIL at location: " +
                  str(count) + " :ERROR *****\n")

            # Print out error in file
            shaHash = "error"

        # Write to outputGen file using each line as new password and data about it
        # Also using a comma as a delimiter for possible conversion into excel sheet
        fileGeneralOut.write(
            "SHA1:,"
            + str(shaHash)
            + ","
            + "Password:,"
            + data["password"].strip("\n")
            + ","
            + "Guesses_Log10:,"
            + str(data["guesses_log10"])
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

    # # Print out any errors for alerting user at end
    # print(errorLoc)

    # Loop to write all errors to file as well at bottom
    for i in errorLoc:
        # Write particular error to file
        fileGeneralOut.write(i)

    # Stop using In file
    fileIn.close()

    # Stop using Out file
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
    print("\n\n**To make this work, you need to first make sure that each file is broken up how you want. An example name for a broken up piece could be x000. MAKE SURE TO FOLLOW THIS NAMING STANDARD! Start name with x000 and go on with that. So one set for one master file could be x000 x001 x002 and the next master file would be x100 x101 x102. DO NOT DEVIATE FROM THIS! **\n\n")

    # Allow user to leave before program runs if they don't understand
    if (str(input("Do you understand? Enter Y/N: ")).lower() != "y"):
        print("\n**** EXITING NOW ****\n")
        exit()

    print("\n")

    inputFilesLocation = str(
        input("Enter the location of files to be read: ")).replace("/", "\\")

    # Easy testing on personal computer
    # Comment out on production version
    inputFilesLocation = "c:\\users\\bigh\\downloads"

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
    os.chdir(inputFilesLocation)

    for x in range(0, inputIndexAmountFirst):
        print("* Analyzing MASTER File #" + str(x + 1) + " *\n")
        for y in range(0, inputIndexAmountSecond):
            print("* Analyzing Piece File #" + str(y + 1) + " *\n")
            runSearch(inputFileName, x, y)
        print("* Finished Analyzing MASTER File #" + str(x + 1) + " *\n")

print("*************** ANALYSIS COMPLETE ***************\n")
