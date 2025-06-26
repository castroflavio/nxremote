'''
STUNNEL.PY

stunnel-based SSL client proxy for NeXus Pyro services.
'''

import os
import tempfile
from subprocess import Popen, PIPE

class NXPyroSTunnel:

    def __init__(self, localPort=8081, remoteHost="remote-server.com", remotePort=8443, pskFile="stunnel.psk"):
        self.localPort = localPort         # Local plain port (where clients connect)
        self.remoteHost = remoteHost       # Remote SSL server
        self.remotePort = remotePort       # Remote SSL port
        self.pskFile = pskFile
        
        self.verify_stunnel()
        self.config_path = self.make_config()
        self.process = Popen(["/usr/local/bin/stunnel", self.config_path])

    def verify_stunnel(self):
        try:
            result = Popen(["/usr/local/bin/stunnel", "-version"], stdout=PIPE, stderr=PIPE)
            result.wait()
            if result.returncode != 0:
                raise Exception("stunnel not found or not working")
        except FileNotFoundError:
            raise Exception("stunnel not found at /usr/local/bin/stunnel")

    def make_config(self):
        fd, path = tempfile.mkstemp(suffix='.conf')
        with os.fdopen(fd, 'w') as f:
            f.write(f"PSKsecrets = {self.pskFile}\n")
            f.write("[pyro]\n")
            f.write("client = yes\n")
            f.write(f"accept = {self.localPort}\n")
            f.write(f"connect = {self.remoteHost}:{self.remotePort}\n")
            f.write("ciphers = PSK\n")
        return path

    def terminate(self):
        self.process.terminate()
        self.process.wait()
        os.unlink(self.config_path)