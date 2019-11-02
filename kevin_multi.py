# python 3 - SHELL MULTI program

# import the needed modules
import os
import sys
import datetime
import openpyxl
import kevin_xshell

# my_main function
def my_main():

	# time stamp the start time
  START_TIME = datetime.datetime.now()

	# today's date
  TODAY = datetime.date.today()
  print("TODAY --", str(TODAY), str(START_TIME))

	# 1. get user input - 2 parameters - MODE, CMD/FILE
  if len(sys.argv) != 3:
    exit("Please enter 2 arguments")

  MODE = sys.argv[1]
  CMD_LIST = []
  if MODE == "SINGLE":
    CMD = sys.argv[2]
    CMD_LIST.append(CMD)
  else:
    FILE = sys.argv[2]
    if not os.path.isfile(FILE):
      exit("file not in working folder...")
    if not FILE.endswith(".txt"):
      exit("file does not have .txt extension...")
    CMD_FILE = open(FILE, "r")
    for CMD in CMD_FILE:
      CMD = CMD.rstrip()
      CMD_LIST.append(CMD)
    CMD_FILE.close()
  print(CMD_LIST)

	# 2. validate the the user input is correct for each mode

	# 3. create a list of the commands to be run using SHELL

	# 4. setup the configuration for the remote server
  HOST = "54.80.104.5"
  USER = "student"
  KEY = "dnp423_student.pem"
	# 5. validate whether the RSA key file that was configured in step 4 is in
	#    the working folder
  if not os.path.isfile(KEY):
    exit("RSA key not found")
  else:
    print("RSA key found!")

	# 6. create the .log file for logging
	#    create the .xlsx file for logging
  log_filename = "SHELL_MULTI_" + str(TODAY) + ".log"
  LOG = open(log_filename,"a")


	# 7. create the signature for time stamp and write to log file
  SIGN = "## ++ >> LOG start time is " + str(START_TIME) + "\n"
  LOG.write(SIGN)

	# 8. setup the SSH connection
  SSH_SUCCESS, SSH_CLIENT = kevin_xshell.setup_ssh_connection(HOST,USER,KEY)
  print("reponse for ssh connection --", SSH_SUCCESS)

	# 9. setup the shell client
  if SSH_SUCCESS:
    SHELL_SUCCESS, SHELL = kevin_xshell.setup_shell_sesstion(SSH_CLIENT, LOG)

	# 10. run the command/commands
    if SHELL_SUCCESS:
      for command in CMD_LIST:
        kevin_xshell.run_command(SHELL,command,LOG)

	# 11. close the SSH connection
  kevin_xshell.close_ssh_connection(SSH_CLIENT)
  print("close ssh connection... DONE")
	# 12. save and close log files
  LOG.close()
# END OF FUNCTION

# actual main body
if __name__ == "__main__":
	my_main()
# end of if

# END OF FILE