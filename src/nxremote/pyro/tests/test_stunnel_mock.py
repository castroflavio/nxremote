#!/usr/bin/env python

import sys
import time
import os
import tempfile
from subprocess import Popen, PIPE

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from stunnel import NXPyroSTunnel

def create_psk_file():
    fd, path = tempfile.mkstemp(suffix='.psk')
    with os.fdopen(fd, 'w') as f:
        f.write("client1:0123456789abcdef0123456789abcdef\n")
    return path

def test_stunnel_startup():
    psk_path = create_psk_file()
    tunnel = NXPyroSTunnel(localPort=8091, remoteHost="example.com", remotePort=8443, pskFile=psk_path)
    time.sleep(2)
    tunnel.terminate()
    os.unlink(psk_path)

def test_with_openssl_server():
    psk_path = create_psk_file()
    server = Popen(["openssl", "s_server", "-accept", "8444", "-psk", "0123456789abcdef0123456789abcdef", "-nocert", "-quiet"], stdout=PIPE, stderr=PIPE)
    time.sleep(2)
    tunnel = NXPyroSTunnel(localPort=8092, remoteHost="localhost", remotePort=8444, pskFile=psk_path)
    time.sleep(2)
    tunnel.terminate()
    server.terminate()
    server.wait()
    os.unlink(psk_path)

def main():
    test_stunnel_startup()
    test_with_openssl_server()
    print("Done")

if __name__ == "__main__":
    main()