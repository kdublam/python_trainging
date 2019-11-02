import os
import sys
import paramiko

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


def setup_sftp_sesstion(sshclient):
  print("inside setup_sftp_session function")

  success = True
  
  try:
    ftpclient = sshclient.open_sftp()
    print("ftp set up successful!")
  except:
    print("ftp not successful...")
    success = False

  return success, ftpclient


def get_file(ftpclient, filename):
  print("inside get_file function")

  success = True

  try:
    ftpclient.stat(filename)
  except:
    print("File not found...")
    success = False
    return success
  
  ftpclient.get(filename, filename)

  return success

def close_ssh_connection(sshclient):
  print("inside close connection function")
  sshclient.close()
  print("ssh closed...")

# print("Start of Program")

# if len(sys.argv) != 2:
#   exit("Please enter an argument")

# input_filename = sys.argv[1]


# HOST = "54.80.104.5"
# USER = "student"
# KEY = "dnp423_student.pem"

# if not os.path.isfile(KEY):
#   exit("RSA key not found")
# else:
#   print("RSA key found!")

# SUCCESS, SSHCLIENT = setup_ssh_connection(HOST, USER, KEY)

# print(SUCCESS, SSHCLIENT)

# if SUCCESS:
#   SUCCESS, FTPCLIENT = setup_sftp_sesstion(SSHCLIENT)

#   if SUCCESS:
#     SUCCESS = get_file(FTPCLIENT, input_filename)


# close_ssh_connection(SSHCLIENT)

# print("End of Program")