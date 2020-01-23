import paramiko
import os.path
import time
import sys
import re


#checking username/password file
#Prompting user for input-Username/password file


user_file = input("\n* Enter user file path and name (ex. /root/niku/Desktop/file.txt): ")

#verfying the validity of username/password file
if os.path.isfile(user_file) == True:
    print("\n* Username/password is valid :) \n")

else:
    print("\n* File {} does not exist Please checck again. \n" .format(user_file))
    sys.exit()


#checking commands file
#prompting user for input -COMMANDS FILE

cmd_file = input("\n* Enter commands file path and name (ex. /root/niku/Desktop/file.txt): ")

#veryfing the validity
if os.path.isfile(cmd_file) == True:
    print("\n*command file is valid :) \n" )

else:
    print("\n* File {} does not exist Please checck again. \n" .format(cmd_file))
    sys.exit()
      

#Open SSHv2 connection to the device
def ssh_connection(ip):
    global user_file
    global cmd_file

    #creating ssh connection
    try:

        #define SSH parameters
        selected_user_file =open(user_file, 'r')

        #starting from the beginning of the file
        selected_user_file.seek(0)

        #reading the username from the file
        username = selected_user_file.readlines()[0].split('.')[0].rstrip("\n")

        #starting from the  begining of the file
        selected_user_file.seek(0)

        #reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")

        #logging into device 
        session = paramiko.SSHClient()
        #for testing purposes this allows unkown host keys do not use it in real life
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy() )

        #Connect to the device using username and password
        session.connect(ip.rstrip("\n"), username= username, password= password)
        

        #start an interactive shell session on the router
        connection = session.invoke_shell()


        #setting terminal length for entire  output
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)

        #entering global config mode 
        connection.send("\n")
        connection.send("configure terminal1\n")
        time.sleep(1)

        #OPEN cmd file 
        selected_cmd_file = open(cmd_file, 'r')

        #starting from the start
        selected_cmd_file.seek(0)

        #writing each line in the device file
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)

        #closing the user file
        selected_user_file.close()

        #closing cmd
        selected_cmd_file.close()

        #checking command output dor IOS errors
        router_output = connection.recv(65535)

        if re.search(b"% invalid input" , router_output):
            print("* there was an ios syntax error {} :(" .format(ip))

        else:
            print("\nDone for device {} \n" .format(ip))

        #test for reading command output
        print(str(router_output) + "\n")


        #closing the connection
        session.close()

    except paramiko.AuthenticationException:
        print("* Invalid username or password :( \n* Please check the username/password file or the device configuration.")
        print("* Closing program... Bye!")