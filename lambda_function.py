import json
import boto3

client = boto3.client('ec2')

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from public_key import PUBLIC_KEY

PING_PONG = {"type": 1}
RESPONSE_TYPES =  { 
                    "PONG": 1, 
                    #"ACK_NO_SOURCE": 2, 
                    #"MESSAGE_NO_SOURCE": 3, 
                    "MESSAGE_WITH_SOURCE": 4, 
                    "ACK_WITH_SOURCE": 5
                  }
#PUBLIC_KEY = '' # found on Discord Application -> General Information page


def verify_signature(event):
    raw_body = event.get("rawBody")
    auth_sig = event['params']['header'].get('x-signature-ed25519')
    auth_ts  = event['params']['header'].get('x-signature-timestamp')
    
    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    verify_key.verify(message, bytes.fromhex(auth_sig)) # raises an error if unequal

def ping_pong(body):
    if body.get("type") == 1:
        return True
    return False

def process_instance_state_object(obj, typ):
    ls = obj.get(typ, [])
    if len(ls) == 0:
        return ('Unknown', 'Unknown')
    return (ls[0].get('CurrentState', {}).get('Name', 'Unknown'),
            ls[0].get('PreviousState', {}).get('Name', 'Unknown'))
    
def lambda_handler(event, context):
    print(f"event {event}") # debug print
    # verify the signature
    try:
        verify_signature(event)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    resp = {
        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
        "data": {
            "tts": False,
            "content": "Somehow there's no response!",
            "embeds": [],
            "allowed_mentions": []
        }
    };

    # check if message is a ping
    body = event.get('body-json')
    if ping_pong(body):
        resp = PING_PONG
    else:
        command = "No command"
        options = "No options"
        try:
            command = body.get('data').get('name')
            options = body.get('data').get('options')
            if len(options) > 0:
                option = options[0].get('value')
                if option == "start":
                    response = client.start_instances(InstanceIds=['i-04df84ad62747443e'])
                    (current_state, previous_state) = process_instance_state_object(response, 'StartingInstances')
                    resp = {
                        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
                        "data": {
                            "tts": False,
                            "content": f"Starting server. Previous state: {previous_state}. Current state: {current_state}",
                            "embeds": [],
                            "allowed_mentions": []
                        }
                    };
                elif option == "stop":
                    response = client.stop_instances(InstanceIds=['i-04df84ad62747443e'])
                    (current_state, previous_state) = process_instance_state_object(response, 'StoppingInstances')
                    resp = {
                        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
                        "data": {
                            "tts": False,
                            "content": f"Stopping server. Previous state: {previous_state}. Current state: {current_state}",
                            "embeds": [],
                            "allowed_mentions": []
                        }
                    };
                else:
                    resp = {
                        "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
                        "data": {
                            "tts": False,
                            "content": f"Failed to parse command. Got unknown option: {option}",
                            "embeds": [],
                            "allowed_mentions": []
                        }
                    };
        except Exception as e:
            resp = {
                "type": RESPONSE_TYPES['MESSAGE_WITH_SOURCE'],
                "data": {
                    "tts": False,
                    "content": f"Error running command.\nCommand: {command}\nOptions: {options}\nError: {e}",
                    "embeds": [],
                    "allowed_mentions": []
                }
            };

    print(f"response {resp}") #debug print
    return resp;
   
