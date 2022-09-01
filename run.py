#!/usr/bin/env python3

import os
import subprocess
import json

import threading

def runServer():
    import backend.main

def runClient():
    os.chdir(os.getcwd() + "/frontend")
    port = 0
    with open("backend-config.json") as f:
        config = json.load(f)
        port = config["frontend-port"]
    subprocess.run("python3 -m http.server " + str(port), shell=True)

serverThread = threading.Thread(target=runServer)
clientThread = threading.Thread(target=runClient)

clientThread.start()
serverThread.start()

clientThread.join()
serverThread.join()
