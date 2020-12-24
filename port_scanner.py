from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from sys import argv, exit

port_list = []
open_ports = []
thread_list = []
options = ["A", "M", "F", "0", "1", "2"]

def readStr(msg):
	while True:
		try:
			n = str(input(msg))
		except KeyboardInterrupt:
			print("\nType 'exit' to exit the program")
		else:
			return n 


def l(n, s="-"):
	print(n * s)


def header(msg):
	l(50)
	print(f"{msg:^50}")
	l(50)


def makeList(n):
	for c in range(n):
		port_list.append(c)


def portScan(port):
	try:
		s.connect((target, port))
		return True
	except:
		return False


def worker():
    c = 0
    while True:
        if len(port_list) > 0:
            port = port_list[c]
            port_list.remove(port)
            if portScan(port):
                print(f"Port {port} is open!")
                open_ports.append(port)
        else:
            break


def preatyPrint():
	header("Open Ports")
	if len(open_ports) != 0:
		for port in open_ports:
			print("Port open: " + str(port))
	else:
		print("No ports are open!")
	l(50)


while True:
	try:
		target = argv[1]
	except:
		target = readStr("TARGET: ")
		if target.lower() == "exit":
			exit()
		break
	else:
		break


while True:
	try:
		option = argv[2]
		if option.strip().upper() in options:
			break
		else:
			print("Invalid Option")
			raise Exception
	except:
		option = readStr("Option: ")
		if option.lower() == "exit":
			exit()
		if option.strip().upper() in options:
			break
		else:
			print("Invalid option")


if option.upper() == "A" or option == "2":
	makeList(65352)
elif option.upper() == "M" or option== "1":
	makeList(10000)
elif option.upper() == "F" or option == "0":
	makeList(1024)

s = socket(AF_INET, SOCK_STREAM)

header(f"Scanning target: {target}")

for c in range(500):
	t = Thread(target=worker)
	thread_list.append(t)

for thread in thread_list:
	thread.start()

for thr in thread_list:
	thread.join()

l(50)
