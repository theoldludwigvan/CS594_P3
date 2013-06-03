#Ian Van Houdt
#CS 494

#server.py

#This progam will simulate an HTTP server. It will setup up and wait to recieve
#requests for files local to the server.

#The server needs to:
#   listen on the TCP port specified on the command line (python server.py -p <port>)
#   Serve files from local dir.
#   Send a valid HTTP response, including headers and the complete file data
#   Return status code "200 OK" for files that exist
#   Return status code "404 File Not Found" for filenames that do not exist
#   Support retrieving files larger than a few KB, requiring multiple calls to your socket's send() method


import socket
import os
import sys


#Bring in command line args
port = sys.argv[2] #port number to listen on
port = int(port)


#Set IP and PORT to listen on:
TCP_IP = '127.0.0.1' # localhost
TCP_PORT = port  
BUFFER_SIZE = 1024


#Bind ports and listen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5) #max number of queued connections


#loop to continue recieving messages
while 1:
  conn, addr = s.accept()
  print 'Connection address: ', addr
  
  while 1:

    #Bring in data
    data = conn.recv(BUFFER_SIZE)

    #Test for successful reception
    if not data:
      break

    #Get header
    hSize = data.find("\r\n\r\n")+4
    header = data[:hSize]
    print header


    #Get requested fileName
    fileEnd = header.find(" HTTP/1.1")
    fileName = header[4:fileEnd]
    print fileName

    if (header[0:3] == "GET"):
      print "recieved data: ", data


      #Set path for directory and add requested filename:
      path = "C:\,Users,Ian,Documents,PSU,CS494 spr'13,Proj3," + fileName
      path = path.split(",")
      path = os.path.join(*path)
      print path


      #See if file exists
      if (os.path.exists(path)):
        print "file exists"
        fileSize = os.path.getsize(path)
        fileSize = int(fileSize)
        print fileSize
        Message = "HTTP/1.1 200 OK\r\nConnection: close\r\n"
        Message += "Host: Ian's Server\r\n"
        Message += "Content-Length: " + `fileSize` + "\r\n\r\n"
        conn.send(Message)



        #Send file. If bigger than Buffer, multiple sends
        if (fileSize <= BUFFER_SIZE):
          f = open(path)
          data = f.read()
          conn.send(data)
        else:
          f = open(path)
          while (fileSize > 0):
            data = f.read(BUFFER_SIZE)
            conn.send(data)
            fileSize -= BUFFER_SIZE

      else:
        print "file doesnt exist"
        Message = "HTTP/1.1 404 File Not Found\r\nConnection: close\r\n"
        Message += "Host: Ian's Server\r\n"
        conn.send(Message)

conn.close()
