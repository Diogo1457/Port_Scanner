try:
    from socket import AF_INET, SOCK_STREAM, socket
    from threading import Thread
    import argparse
    import os
    from random import choice
    import time
    from datetime import datetime
except Exception as e:
    print("[EXCEPTION] ", e)
    exit()

numbers = "1234567890"

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ports", help="Ports you want to check. Syntax -> -p 22, 80, 443")
parser.add_argument("-m", "--mode", help="Mode -A -> 65432 ports, -M -> 10000 ports, -F -> 1024 ports")
parser.add_argument("-o", "--outfile", action="store_true", help="Write the output in a file")
parser.add_argument("-v", "--verbose", action="store_true", help="Show the process while running")
parser.add_argument("--threads", type=int, help="Set the Number of threads default=500")
parser.add_argument("target", help="IP of the target")
parser.add_argument("--version", action="version", version="1.0")
args = parser.parse_args()

ports_passed = args.ports
mode = args.mode
filename = args.outfile
verbose = args.verbose
target = args.target
threads = args.threads

open_ports = []

SERVER = socket(AF_INET, SOCK_STREAM)


class Files():
    def __init__(self, filename):
        self.filename = filename


    def fileExist(self):
        try:
            a = open(self.filename, "rt")
        except:
            return False
        else:
            return True


    def createFile(self):
        try:
            a = open(self.filename, "wt+")
        except Exception as e:
            return f"[EXCEPTION] {e}"
        else:
            return True


    def writeFile(self, msg):
        try:
            a = open(self.filename, "at")
            a.write(f"{msg}\n")
        except:
            return False
        else:
            return True


def makeListPorts(number):
    ports = []
    for c in range(1, number + 1):
        ports.append(c)
    return ports


def selectPorts(type):
    if type == "A":
        ports = makeListPorts(65432)
    elif type == "M":
        ports = makeListPorts(10000)
    elif type == "F":
        ports = makeListPorts(1024)
    return ports


def getPorts(type):
    global ports_passed
    if ports_passed == None:
        ports_passed = selectPorts(type)
    else:
        ports_passed = ports_passed.split(",")
        for p in ports_passed:
            try:
                int(p)
            except:
                print(f"Invalid Port {p}")
                exit()
    return ports_passed


def l(n, s="-"):
    print(n * s)


def header(msg):
    l(50)
    print(f"{msg:^50}")
    l(50)


def printOpenPorts():
    if len(open_ports) > 0:
        header("Open ports")
        for port in open_ports:
            print(f"Port: {port}")
        l(50)
    else:
        header("No open ports")



def createLog(filename, ports):
    f = Files(filename)
    if not f.fileExist():
        file_created = f.createFile()
        if file_created == True:
            response = ""
            for p in ports:
                if f.writeFile(f"Port {p} is open"):
                    response = f"File {filename} created"
                else:
                    response = f"Error writing in the file {filename}"
                    break
            return response
        else:
            return file_created
    else:
        return f"File {filename} already Exists"



def generateFilename():
    filename = ""
    for c in range(5):
        filename += choice(numbers)
    filename = filename + ".txt"
    return filename


def createNameOfFile():
    current_dir = os.getcwd()
    filename_generate = generateFilename()
    f = Files(filename_generate)
    while f.fileExist():
        f = Files(filename_generate)
        filename_generate = generateFilename()
    return os.path.join(current_dir, filename_generate)


def portScan(port):
    global target
    ADDR = (target, port)
    try:
        SERVER.connect(ADDR)
    except Exception as e:
        return False
    else:
        return True


def scan():
    global ports
    while True:
        if len(ports) > 0:
            port = ports[0]
            ports = ports[1::1]
            if portScan(port):
                open_ports.append(port)
                if verbose:
                    print(f"Port {port} is open")
        else:
            break


def selectMode(mode):
    if mode == None:
        mode = "F"
    else:
        mode = mode.upper()
        if mode not in "FMA":
            print("Invalid Mode")
            exit()
    return mode


if __name__ == "__main__":
    if threads == None:
        threads = 500
    mode = selectMode(mode)
    ports = getPorts(mode)
    start_time = time.time()
    header(f"Scanning {target}")
    time_scan_start = str(datetime.today().time())
    print(f"Scan started at {time_scan_start}")
    l(50)
    for c in range(threads):
        THREAD = Thread(target=scan)
        THREAD.start()
        THREAD.join()
    end_time = time.time()
    time_delta = end_time - start_time
    l(50)
    print(f"Scan time: {str(time_delta)[0:4:1]}s")
    printOpenPorts()
    if filename == True:
        filename = createNameOfFile()
        log = createLog(filename, open_ports)
