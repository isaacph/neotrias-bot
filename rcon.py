import re
import random
import struct
import socket
from public_key import *
   
def request(command):
    log = "log start\n"
    sanitized_command = sanitize_command(command)
    # For authorization, you can use either your bot token
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)
    try:
        client.connect((SERVER_HOSTNAME,SERVER_RCON_PORT))
    except TimeoutError:
        return "Error: (0) timeout. Make sure the server is running first"

    # login
    request, request_id = format_request(3, bytes(SERVER_RCON_PASSWORD, 'utf-8'))
    client.send(request)
    log += "send (1)\n"
    response = client.recv(4)
    log += f"recv (1) length\n"
    try:
        response_len = struct.unpack("<i", response)[0]
        log += f"unpack (1) length {response_len}\n"
    except Exception as e:
        return f"Error: {str(e)}. Log:\n{log}"

    response = client.recv(response_len)
    if response_len < 8:
        return f"Error: (1) returned short packet ({response_len}) -- {str(response)}"
    log += f"recv (1) content -- {str(response)}\n"

    try:
        response_id, _ = struct.unpack("<ii", response[:8])
        log += "unpack (1) response\n"
    except Exception as e:
        return f"Error: {str(e)}. Log:\n{log}"
    payload = response[8:]
    
    if response_id != request_id:
        return "Error (1) authenticating: " + str(payload)
    log += "authenticated\n"

    # command
    request, request_id = format_request(2, sanitized_command)
    client.send(request)
    log += "send (2)\n"

    response = client.recv(4)
    log += f"recv (2) length\n"
    try:
        response_len = struct.unpack("<i", response)[0]
        log += f"unpack (2) length {response_len}\n"
    except Exception as e:
        return f"Error: {str(e)}. Log:\n{log}"

    response = client.recv(response_len)
    if response_len < 8:
        return f"Error: (2) returned short packet ({response_len}) -- {str(response)}"
    log += f"recv (2) content -- {response}\n"

    try:
        response_id, _ = struct.unpack("<ii", response[:8])
        log += "unpack (2) response\n"
    except Exception as e:
        return f"Error: {str(e)}. Log:\n{log}"
    payload = response[8:-1]

    if response_id != request_id:
        return "Error (2) authenticating: " + str(payload)
    
    return payload.decode('utf-8')

# typ must be int 3, 2, or 0
# payload must be byte string
def format_request(typ, payload):
    request_id = random.randint(0, 99999)
    packet = struct.pack("<ii", request_id, typ) + payload + b'\0\0'
    return (struct.pack("<i", len(packet)) + packet, request_id)

def sanitize_command(command):
    #TODO
    return bytes(command, "utf-8")

def sanitize_user(user):
    return re.split('\\s+', user)[0]
