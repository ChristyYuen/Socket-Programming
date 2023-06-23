from socket import *
import sys 
import csv
import os

#-------------Writing to file stuff below--------------

def  writing(content, dest_file) :
        path = dest_file[1:] #everything after the first element
        f = open(path, "wb")  #wb cuz discord and binary
        contentList = content.split('\r\n\r\n')[1] #only the second elem, aka message #[1] is the message and [0] is the header stuff
        contentIN = ""
        for i in range (0,len(contentList)): #recreating after the split
                contentIN = contentIN + contentList[i] #put everything in
        f.write(bytes(contentIN, 'UTF-8')) #discord help
        f.close()

def clienting(clientSocket):
        args1 = sys.argv[1].split("//")[1].split('/')  #getting the host name 
        #print(args1)
        
        fileName = "" 
        for i in range (1 ,len(args1)): #making the entire file name after splitting in args
                fileName += "/" + args1[i] #remaking it after the split
                #print(fileName)
        if fileName == "" : #if blank the add a / cuz bug
                fileName = "/"

        #creating the GET request
        request = "GET " + fileName + " " + "HTTP/1.1\r\n" + "Host: " 
        request += sys.argv[1].split("//")[1].split('/')[0] + "\r\n\r\n" #split by //, get the second elem, then split by / and get the first elem of splited

        #Sending the request to socket
        clientSocket.send(request.encode()) 
        r = clientSocket.recv(10240000) #added a couple zeros due to source code(1024) being too short
        
        #-------------more writing stuff here --------------
        #such as success and writing to log 
        
        print(r.decode().split('\r\n\r\n')[0].split('\n')[0]) #HTTP REQUEST

        HTTPRequestDecoded = r.decode().split('\r\n\r\n')[0].split('\n')[0] 
        
        #Going to hard code Log.csv the maybe make a function later
        f2 = open("/" + os.getcwd() + "/Log.csv", "wb")
        firstLineofLOG = "Successful or Unsuccessful, Requested URL , Hostname, source IP, destination IP, source port, destination port, Server Response line(including code and phrase)\n"  

        statueSucc = ''
        RequestedURL = sys.argv[1]
        HostName = args1
        sourceIP = ''
        destPort = '' 
        ServerResponseLine = HTTPRequestDecoded 
        #idea is to use decode to get parts of the data and then merag it back into the log file


        if (HTTPRequestDecoded == ''): #should I just check the 200? or the entire thing
                statueSucc = Successful
        else:
                statueSucc = Unsuccessful

        #easier to see in parts
        LogContentIN = statueSucc + ", " + \
                       RequestedURL + ", " + \
                       HostName + ", " + \
                       sourceIP + ", " + \
                       destPort + ", " + \
                       ServerResponseLine 

        f2.write(bytes(LogContentIN, 'UTF-8')) #discord help
        f2.close()
        
        print(statueSucc)

        writing(r.decode(), "/" + os.getcwd() + "/HTTPoutput.html") #write to http file 
        print("Program Finished") #done message

#----------------Setting up the socket --------------------------

serverName = gethostbyname(sys.argv[1].split("//")[1].split('/')[0].split(':')[0]) #socket stuff below

#need to make a port number split  

print (sys.argv[1].split("//")[1].split('/')[0].split(':')[0]) #socket stuff below 

serverPort = 80 #default port #change into if 80 then leave else change to split 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clienting(clientSocket)

clientSocket.close() 
