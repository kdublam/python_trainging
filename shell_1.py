import os
import sys
import paramiko
import time
import datetime
import openpyxl

def setup_ssh_connection(host, user, key):
  print("inside setup_ssh_connection function")
  success = True
  # sshclient = None

  sshclient = paramiko.SSHClient()

  sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  sshclient.load_system_host_keys()

  try:
    sshclient.connect(host, username=user, key_filename=key)
    print("SSH connection setup... successful")
  except:
    print("SSH Connection setup... Not successful")
    success = False

  return success, sshclient


def setup_shell_sesstion(sshclient, LOG):
  print("inside setup_shell_session function")
  success = True
  shellclient = None

  sshtrans = sshclient.get_transport()

  try:
    sshsession = sshtrans.open_session()
    print("open session.... successful")
  except:
    print("open session... failed...")
    success = False
    return success, shellclient

  try:
    shellclient = sshclient.invoke_shell()
    print("invoke shell successful")
  except:
    print("invoke shell failed...")
    success = False
    return success, shellclient

  time.sleep(5)
  rx = shellclient.recv(600).decode(encoding="utf-8")
  print("buffer size rx--", len(rx))
  print("\n\n", rx, "\n\n")

  LOG.write("\n")
  for my_line in rx.split("\n"):
    LOG.write(my_line)
  LOG.write("\n")

  return success, shellclient
  

def run_command(shellclient, command, LOG):
  print("inside run_command function")
  success = True
  print("running command---", command)

  command = command.strip()
  command = command + "\n"

  shellclient.send(command)

  time.sleep(5)

  while not shellclient.recv_ready():
    time.sleep(0.2)

  rx = shellclient.recv(100000).decode(encoding="utf-8")
  print("buffer size rx--", len(rx))
  print("\n\n", rx, "\n\n")

  LOG.write("\n")
  for my_line in rx.split("\n"):
    LOG.write(my_line)
  LOG.write("\n")

  return success
  

def close_ssh_connection(sshclient):
  print("inside close connection function")
  sshclient.close()
  print("ssh closed...")

# print("Start of Program")

# START_TIME = datetime.datetime.now()
# TODAY = datetime.date.today()
# print("TODAY --", str(TODAY))

# if len(sys.argv) != 2:
#   exit("Please enter an argument")

# command = sys.argv[1]


# HOST = "54.80.104.5"
# USER = "student"
# KEY = "dnp423_student.pem"

# if not os.path.isfile(KEY):
#   exit("RSA key not found")
# else:
#   print("RSA key found!")

# log_filename = "SHELL_ONE_" + str(TODAY) + ".log"
# xlsx_filename = "SHELL_ONE_" + str(TODAY) + ".xlsx"

# LOG = open(log_filename, "a")
# XLOG = open(xlsx_filename, "a")

# SIGN = "\n### --> LOG start time --" + str(START_TIME)
# XSIGN = "LOG start time -- " + str(START_TIME)

# LOG.write(SIGN)
# # XLOG.write(XSIGN)

# XLOG_WB = openpyxl.Workbook()
# XLOG = XLOG_WB.active
# XLOG.title = "LOG"

# SUCCESS, SSHCLIENT = setup_ssh_connection(HOST, USER, KEY)

# print(SUCCESS, SSHCLIENT)

# if SUCCESS:
#   SUCCESS, SHELLCLIENT = setup_shell_sesstion(SSHCLIENT, LOG)

#   if SUCCESS:
#     SUCCESS = run_command(SHELLCLIENT, command, LOG)


# close_ssh_connection(SSHCLIENT)

# LOG.close()
# # XLOG.close()

# XLOG_WB.save(xlsx_filename)
# XLOG_WB.close()


# END_TIME = datetime.datetime.now()

# print("Program run time --", END_TIME - START_TIME)

# print("End of Program")