import os
from multiprocessing import Process
import time
from argparse import ArgumentParser
from hashlib import sha1
# import psutil
from zxcvbn import zxcvbn


def hashInput(inputData):
    inputData = inputData.encode("utf-8")
    hash_object = sha1(inputData)
    hex_dig = hash_object.hexdigest()
    return hex_dig


def runSearch(inputFile, currentIndex, hashSize):
    # Attempt opening files for reading
    try:
        # Open file for reading from (Change based on if .txt is present or not by uncommenting)
        # fileIn = open(inputFile + str(currentIndex).zfill(2) + ".txt", "r")
        fileIn = open(inputFile + str(currentIndex).zfill(2), "r")

    except:
        # Alert user of failure to open file
        print('***** ERROR: __OpenFile__ "' + inputFile +
              str(currentIndex).zfill(2) + '" Does not exist :ERROR*****\n')

        # Exit file analysis
        return

    # Create output file title and location
    cwdOutputGen = ("output_data" + str(currentIndex).zfill(2) + ".txt")
    cwdOutputSHA = ("output_data_SHA" + str(currentIndex).zfill(2) + ".txt")

    # instantiate storage lists
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
            line = line[hashSize:].strip()

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

            # # Initialize jSON to store zxcvbn info
            # data = {}

            # Get zxcvbn to analyze and place in temp complete value
            temp = zxcvbn(line)

            # Checks if 20,000 lines have been passed through
            if count % 20000 == 0:
                # Get end time to calculate current time
                end = time.time()

                # Alerts user about pass through
                print("\nAnalyzed " + str(count) + " passwords")
                print("@" + str(round(end - start, 3)) + " seconds")

                # # Gets ID of current python program
                # process = psutil.Process(os.getpid())

                # # Alerts user of current memory usage
                # print(
                #     "* " + str(round(process.memory_info().rss / 1024/1024, 4)) + "MB *\n")

            # Remove any result that is too weak to be useful for goal
            if temp["guesses_log10"] < 8:
                # If result unuseful, move on to next
                continue

            # # Parse through JSON and pull out necessary info
            # data['password'] = temp['password']
            # data['guesses_log10'] = temp['guesses_log10']

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
            shaHash = hashInput(temp["password"])

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
            + temp["password"].strip("\n")
            + ","
            + "Guesses_Log10:,"
            + str(temp["guesses_log10"])
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
    # Alert user of end
    print("*************** ANALYSIS COMPLETE ***************\n")
    print("Finished @" + str(round(end - start, 3)) + " seconds\n")


if __name__ == "__main__":

    # Create an argument parser for CLI
    parser = ArgumentParser()

    # Add arguments with their help descriptions
    parser.add_argument(
        "-v", "--verbose", help="display instructions, settings, and increase output", action="store_true")
    parser.add_argument(
        "-l", "--location", help="insert where the location of the input files are (REQUIRED if not verbose)")
    parser.add_argument(
        "-n", "--name", help="inital name of files to be run through not including index nor .txt (REQUIRED if not verbose)")
    parser.add_argument("-f", "--file", type=int,
                        help="input for how many files there are to run through (REQUIRED if not verbose)")
    parser.add_argument("-H", "--hash", type=int,
                        help="size of the hash plus colon that will be ignored")

    # Pull in values of arguments
    args = parser.parse_args()

    # Check for verbose flag
    if args.verbose is True:

        # Instruct user on how the program will read data
        print("\n\n**To make this work, you need to first make sure that the file is broken up how you want. An example name for a broken up piece could be x00. MAKE SURE TO FOLLOW THIS NAMING STANDARD! Start name with x00 and go on with that. So one set for the master file could be x00 x01 x02 and the next master file would be. DO NOT DEVIATE FROM THIS! **\n\n")

        # Allow user to leave before program runs if they don't understand
        if (str(input("Do you understand? Enter Y/N: ")).lower() != "y"):
            print("\n**** EXITING NOW ****\n")
            exit()

        print("\n")

        # User input for location of files to read
        inputFilesLocation = str(
            input("Enter the location of files to be read: ")).replace("/", "\\")

        print("\n")

        # User input for name of input data file
        inputFileName = str(
            input("Enter name of input data file (don't include final index nor .txt): "))

        print("\n")

        # User input for how many master files will be there
        inputIndexAmount = int(input("Enter how many files there are: "))

        print("\n")

    # Force flag check
    else:

        # Instantiate holder list for flags
        flags = []

        # Check for if location flag is missing
        if args.location is None:
            # Insert missing flag into holder list
            flags.append("location,")

        # Check for if name flag is missing
        if args.name is None:
            # Insert missing flag into holder list
            flags.append("name,")

        # Check for if files flag is missing
        if args.file is None:
            # Insert missing flag into holder list
            flags.append("file,")

        # Check for if there are any flags in list
        if not flags:
            # Pass if good
            pass

        # Force stop for flags missing
        else:
            # Remove last comma for good looks
            flags[len(flags) - 1] = flags[len(flags) - 1].strip(",")

            # Alert user for missing flag and indicate which
            print(
                "Multiple_Cores_Process.py: error: the following arguments are required:", *flags)

            # Exit program
            exit()

        # Put flag values into variables
        inputFileName = args.name
        inputFilesLocation = args.location
        inputIndexAmount = args.file

    # Check for if hash flag present
    if args.hash is not None:
        # Put flag value into variable
        inputHashSize = args.hash

    # Force a standard hash size
    else:
        # Put standard size into variable
        inputHashSize = 41

    # Easy testing on personal computer
    # Comment out on production version
    # inputFilesLocation = "c:\\users\\bigh\\downloads"

    # For particular test case
    # Need to go one up to retrieve input_data files
    os.chdir(inputFilesLocation)
    # os.chdir("/home/hasadi/temp")

    print("*************** ANALYSIS STARTING ***************\n")

    # Instantiate list of all running processes
    # Could be used
    # procs = []

    # A loop to create all processes depending on index amount
    for i in range(0, inputIndexAmount):
        # Alert User
        print("* Analyzing File #" + str(i).zfill(2) + " *\n")

        # Opens up a single process running the search and passing arguments
        p = Process(target=runSearch, args=(inputFileName, i, inputHashSize))

        # Could add processes to a list to check back on later
        # procs.append(p)

        # Starts off current process to run
        p.start()
