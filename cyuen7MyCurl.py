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

def clienting(clientSocket, soIP, deIP, soP, destP):
        fullHostName = sys.argv[1].split("//")[1].split('/')  
        #print(fullHostName)
        
        fileName = "" 
        for i in range (1 ,len(fullHostName)): 
                fileName += "/" + fullHostName[i] 
        if fileName == "" :
                fileName = "/"

        # Creating the GET request
        request = "GET " + fileName + " " + "HTTP/1.1\r\n" + "Host: " 
        request += sys.argv[1].split("//")[1].split('/')[0] + "\r\n\r\n"

        #buffI = 4096 #initial buffer
        #buffI = 100 #initial buffer

        # Sending the request to socket
        clientSocket.send(request.encode()) 
        #r = clientSocket.recv(buffI)
        r = clientSocket.recv(1024000000)

        #print("r decode below")
        #print(r.decode()) 
        #print("------------------------------------------")

        #-------------------Header and bytes reading--------------------------

        HTTPRequestDecoded = r.decode().split('\r\n\r\n')[0].split('\n')[0]
        content_lengthH = int(r.decode().split('\r\n\r\n')[0].split('\n')[2].split(':')[1]) 
        
        #print("Content_length = ")
        #print(content_lengthH)
        #print("HTTP decoded")
        #print(HTTPRequestDecoded)


        HTTPRequestDecoded = r.decode().split('\r\n\r\n')[0].split('\n')[0]
        #might need to split againi into the 200
        HTTPCode = r.decode().split('\r\n\r\n')[0].split('\n')[0].split(" ")[1]
        #print(HTTPRequestCode)
        #print(HTTPRequestDecoded)

        #content_lengthH = content_lengthH - buffI 
        
        #---------------------Attempt to read byte by byte below--------------------

        #messageI = b"" 

        #while True: 
        #        if content_lengthH <= 0: break
        #        data = clientSocket.recv(10000)
        #        messageI += data
        #        content_lengthH = content_lengthH - len(data)


        #print("Content length calculations")
        #print(messageI)
        #print(content_lengthH)

        #-------------------Writing to Log.csv file--------------------------
        
        firstLineofLOG = "Successful or Unsuccessful, Requested URL, Hostname, source IP, destination IP, source port, destination port, Server Response line(including code and phrase)\n"  

        statueSucc = ''
        RequestedURL = sys.argv[1]
        HostName = fullHostName[0]
        sourceIP = soIP
        destIP = deIP 
        sourcePort = soP
        destPort = destP
        ServerResponseLine = HTTPRequestDecoded 
        
        
        pathLog = "/" + os.getcwd() + "/Log.csv"

        if (HTTPCode == "200"):
                statueSucc = "Successful"
                #print(statueSucc + " "  + HostName + " " + ServerResponseLine)
                sys.stdout.write(statueSucc + " "  + HostName + " " + ServerResponseLine + "\n")
        else:
                statueSucc = "Unsuccessful" 

        if os.path.exists(pathLog):
                f2 = open(pathLog, "a")
                LogContentIN = statueSucc + ", " + \
                               RequestedURL + ", " + \
                               HostName + ", " + \
                               sourceIP + ", " + \
                               destIP + ", " + \
                               sourcePort + ", " + \
                               destPort + ", " + \
                               ServerResponseLine + "\n" 

        else:
                f2 = open(pathLog, "w")
                LogContentIN = firstLineofLOG + \
                               statueSucc + ", " + \
                               RequestedURL + ", " + \
                               HostName + ", " + \
                               sourceIP + ", " + \
                               destIP + ", " + \
                               sourcePort + ", " + \
                               destPort + ", " + \
                               ServerResponseLine + "\n"

        f2.write(LogContentIN) #discord help
        f2.close()

        #-------------------Writing to HTTPoutput.html file--------------------------
        writing(r.decode(), "/" + os.getcwd() + "/HTTPoutput.html") 
        

        #print(statueSucc)
        #print("Program Finished") 

#----------------Setting up the socket --------------------------

serverName = (sys.argv[1].split("//")[1].split('/')[0])
serverIP = gethostbyname(sys.argv[1].split("//")[1].split('/')[0])

#print(sys.argv[1].split("//")[1].split('/')[0])

#print(serverName)

#need to make a port number split  

#print (sys.argv[1].split("//")[1].split('/')[0].split(':')[0]) 

serverPort = 80 #default port #change into if 80 then leave else change to split 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))
#print(gethostname() + " 1")
#print(clientSocket.getsockname()[0] + " 2")
#print(str(serverPort) + " 3")

hostName = gethostname()
hostIP = gethostbyname(hostName) 
#print(hostIP + " hostIp")

clienting(clientSocket, serverIP , hostIP, str(clientSocket.getsockname()[1]), str(serverPort))
#print( serverIP + " " + hostIP + " " + str(clientSocket.getsockname()[1]) + " " +str(serverPort))

clientSocket.close() 
