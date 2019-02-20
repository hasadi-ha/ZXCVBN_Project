import os
from zxcvbn import zxcvbn
from zxcvbn.matching import add_frequency_lists
import time

# Make first list
results = []

start = time.time()

# # User input for name of input data file
# inputFileName = "\\" + \
#     str(input("Enter name of input data file (Don't include .txt): ")) + ".txt"

# User input for name of input data file
inputFileName = "passwords" + ".txt"

# Get location for input and output using os
cwdInput = "C:\\Users\\BigH\\Downloads\\ZXCVBN_Project-master\\passwords.txt"
cwdOutput = str(os.getcwd()) + "\output_data.txt"

# Open file for reading from
file = open(cwdInput, "r")

for line in file:
    # Send to zxcvbn to get decryption results from
    results.append(zxcvbn(line))


# Stop using file for good practice
file.close()

# Start an output file to write to
file = open(cwdOutput, "w+")

for i in results:
    file.write("Password:," + i["password"].strip("\n") + "," + "Guesses Log10:," + str(
        i['guesses_log10']) + "," + "Score:," + str(i["score"]) + ",\n")

# Stop using file for good practice
file.close()

end = time.time()

print(end - start)
