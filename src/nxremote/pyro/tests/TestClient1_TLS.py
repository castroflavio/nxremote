#!/usr/bin/env python

"""
TLS client for prototyping Pyro with SSL
"""

import sys
import Pyro4
import ssl

def message(msg):
    print("pyro TLS client: " + str(msg))

if len(sys.argv) == 1:
    uri = input("Enter URI: ")
elif len(sys.argv) == 2:
    uri = sys.argv[1] 
else:
    print("usage: client.py <URI>")
    exit(1)

# Create SSL context for client with PSK
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Set up PSK callback
def psk_client_callback(hint, identity):
    # Return identity and PSK key
    return b"client1", bytes.fromhex("0123456789abcdef0123456789abcdef")

ssl_context.set_psk_client_callback(psk_client_callback)

# Get a Pyro proxy to the remote object with SSL
Pyro4.config.SERIALIZER = "pickle"
message("proxy connect")
proxy = Pyro4.Proxy(uri)
proxy._pyroSslContext = ssl_context
message("proxy init")
proxy._pyroTimeout = 20.0
b = True

# Use proxy object normally
try:
    print(proxy.__dict__)
    print(dir(proxy))
    # Works:
    b = proxy.f1("hello")
    # Works:
    key1 = "key1"
    value1 = proxy.getitem(key1)
    message("got: %s:%s" % (key1, value1))
    # Works:
    key2 = "key2"
    value2 = proxy.__getitem__(key2)
    message("got: %s:%s" % (key2, value2))
except Exception as e:
    print("Caught exception during remote operations!")
    print("Exception message: " + str(e))
    print("Pyro remote traceback:")
    print("".join(Pyro4.util.getPyroTraceback()))

message("Shutting down service...")
proxy.exit(0)
if b:
    message("Success.")
else:
    message("Failed!")
    exit(1)
exit(0)