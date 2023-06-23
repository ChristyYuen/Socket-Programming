from socket import *
import sys 
import csv
import os

#-------------Writing to file stuff below--------------

def  writing(content, dest_file) :
        path = dest_file[1:] 
        f = open(path, "wb")  
        contentList = content.split('\r\n\r\n')[1] 
        contentIN = ""
        for i in range (0,len(contentList)):
                contentIN = contentIN + contentList[i]
        f.write(bytes(contentIN, 'UTF-8')) 
        f.close()

def clienting(clientSocket):
        args1 = sys.argv[1].split("//")[1].split('/')  
        
        fileName = "" 
        for i in range (1 ,len(args1)): 
                fileName += "/" + args1[i] 
        if fileName == "" :
                fileName = "/"

        # Creating the GET request
        request = "GET " + fileName + " " + "HTTP/1.1\r\n" + "Host: " 
        request += sys.argv[1].split("//")[1].split('/')[0] + "\r\n\r\n"

        # Sending the request to socket
        clientSocket.send(request.encode()) 
        r = clientSocket.recv(10240000) #times out due to big buffer #should impletment a timer to deadend sockets 

        #-------------------Writing to Log.csv file--------------------------

        HTTPRequestDecoded = r.decode().split('\r\n\r\n')[0].split('\n')[0]
        #might need to split again into the 200

        firstLineofLOG = "Successful or Unsuccessful, Requested URL, Hostname, source IP, destination IP, source port, destination port, Server Response line(including code and phrase)\n"  

        statueSucc = ''
        RequestedURL = sys.argv[1]
        HostName = args1[0]
        sourceIP = ''
        destPort = '' 
        ServerResponseLine = HTTPRequestDecoded 
        
        pathLog = "/" + os.getcwd() + "/Log.csv"

        if (HTTPRequestDecoded == ''):
                statueSucc = "Successful"
        else:
                statueSucc = "Unsuccessful" 

        if os.path.exists(pathLog):
                f2 = open(pathLog, "a")
                LogContentIN = statueSucc + ", " + \
                               RequestedURL + ", " + \
                               HostName + ", " + \
                               sourceIP + ", " + \
                               destPort + ", " + \
                               ServerResponseLine 

        else:
                f2 = open(pathLog, "w")
                LogContentIN = firstLineofLOG + \
                               statueSucc + ", " + \
                               RequestedURL + ", " + \
                               HostName + ", " + \
                               sourceIP + ", " + \
                               destPort + ", " + \
                               ServerResponseLine

        f2.write(LogContentIN) #discord help
        f2.close()

        #-------------------Writing to HTTPoutput.html file--------------------------
        writing(r.decode(), "/" + os.getcwd() + "/HTTPoutput.html") 
        

        print(statueSucc)
        print("Program Finished") 

#----------------Setting up the socket --------------------------

serverName = gethostbyname(sys.argv[1].split("//")[1].split('/')[0].split(':')[0])

#need to make a port number split  

#print (sys.argv[1].split("//")[1].split('/')[0].split(':')[0]) 

serverPort = 80 #default port #change into if 80 then leave else change to split 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

clienting(clientSocket)

clientSocket.close() 
