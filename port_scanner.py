from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from sys import argv, exit

port_list = []
open_ports = []
thread_list = []
options = ["A", "M", "F", "0", "1", "2"]

def readStr(msg):
	"""
	handle input exceptions
	:param msg: str
	:return: str
	"""
	while True:
		try:
			n = str(input(msg))
		except KeyboardInterrupt:
			print("\nType 'exit' to exit the program")
		else:
			return n 


def l(n, s="-"):
	"""
	prints a new line
	:param n: int
	:param s: str
	:return: None
	"""
	print(n * s)


def header(msg):
	"""
	makes an header
	:param msg: str
	:return: None
	"""
	l(50)
	print(f"{msg:^50}")
	l(50)


def makeList(n):
	"""
	makes an list acording to the range of ports you want to check
	:param n: int
	:return: None
	"""
	for c in range(n):
		port_list.append(c)


def portScan(port):
	"""
	scans if a port is open or not
	:param port: int
	:return: bool
	"""
	try:
		s.connect((target, port))
		return True
	except:
		return False


def worker():
	"""
	checks if the range of ports is open
	:return: None
	"""
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
	"""
	prints the open ports
	:return: None
	"""
	header("Open Ports")
	if len(open_ports) != 0:
		for port in open_ports:
			print("Port open: " + str(port))
	else:
		print("No ports are open!")
	l(50)

# CHECKS IF THE TARGET WAS PASSED
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

# CHECKS IF THE OPTION WAS PASSED AND IF IT EXISTS
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

# CALLS MAKE LIST ACCORDING TO THE OPTION
if option.upper() == "A" or option == "2":
	makeList(65352)
elif option.upper() == "M" or option== "1":
	makeList(10000)
elif option.upper() == "F" or option == "0":
	makeList(1024)

# SETUP SOCKET
s = socket(AF_INET, SOCK_STREAM)

# PROGRAM
header(f"Scanning target: {target}")

for c in range(500):
	t = Thread(target=worker)
	thread_list.append(t)

for thread in thread_list:
	thread.start()

for thr in thread_list:
	thread.join()

l(50)
