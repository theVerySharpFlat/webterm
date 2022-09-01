#!/usr/bin/env python3

import os
import subprocess
import json

import threading

import http.server, socketserver

def runServer():
    import backend.main

def runClient():
    if not os.path.lexists(os.getcwd() + "/frontend/backend-config.json"):
        os.symlink(os.getcwd() + "/backend-config.json", os.getcwd() + "/frontend/backend-config.json")
    os.chdir(os.getcwd() + "/frontend")
    PORT = 0
    with open("backend-config.json") as f:
        config = json.load(f)
        PORT = config["frontend-port"]
    
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

serverThread = threading.Thread(target=runServer)
clientThread = threading.Thread(target=runClient)

clientThread.start()
serverThread.start()

clientThread.join()
serverThread.join()