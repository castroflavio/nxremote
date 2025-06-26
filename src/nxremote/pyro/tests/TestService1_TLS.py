#!/usr/bin/env python

import Pyro4
import sys
import threading
import time
import ssl

def shutdown():
    time.sleep(1)
    daemon.shutdown()

def message(msg):
    print("pyro TLS server: " + msg)

class TestService1:

    @Pyro4.expose
    def f1(self, a):
        message("f1(%s)" % str(a))
        return True

    @Pyro4.expose
    def __getitem__(self, key):
        message("__getitem__")
        return self.getitem(key)
    
    @Pyro4.expose
    def getitem(self, key):
        message("getitem inputs: " + str(key))
        t = 45
        message("getitem result: " + str(t))
        return t

    @Pyro4.expose
    def exit(self, code):
        message("Daemon exiting...")
        thread = threading.Thread(target=shutdown)
        thread.daemon = True
        thread.start()
        
service = TestService1()

# Use automated port number by default
port = 8443
if len(sys.argv) > 1:
    port = int(sys.argv[1])

# Make an empty Pyro daemon with SSL
Pyro4.config.SERIALIZERS_ACCEPTED.add("pickle")

# Create SSL context with PSK
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Set up PSK callback for server
def psk_server_callback(identity, hint):
    # Verify identity and return corresponding PSK
    if identity == b"client1":
        return bytes.fromhex("0123456789abcdef0123456789abcdef")
    return None

ssl_context.set_psk_server_callback(psk_server_callback)

daemon = Pyro4.Daemon(host="0.0.0.0", port=port, sslContext=ssl_context)

# Register the object as a Pyro object
uri = daemon.register(service, objectId="testservice")

# Print the URI so we can use it in the client later
print("URI: " + str(uri))
sys.stdout.flush()

# Start the event loop of the server to wait for calls
daemon.requestLoop()
daemon.close()
message("Daemon exited.")