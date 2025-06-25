import asyncio
import websockets
import yaml
#gets the proto file for logging in
import sys, os
from google.protobuf.timestamp_pb2 import Timestamp
sys.path.insert(0, os.path.abspath("proto"))
import time
from proto.t4.v1.auth import auth_pb2
from proto.t4.v1 import service_pb2
from tools.ClientMessageHelper import ClientMessageHelper
from tools.ProtoUtils import encode_message, decode_message
import threading
#port443

#heartbeat connection every 20 seconds (only have 3 consecutive heratbeats to send before the connection is termianted)
port = 443
heartbeat = 20
API_KEY = "TEST"
WS_URL = "wss://wss-sim.t4login.com/v1" # connection to simulator
running = False
#getting info from the config file
def load_config(path="config/config.yaml"):
     with open(path, "r") as file:
          return yaml.safe_load(file)



#the actual websocket connection
async def connect_with_auth(ws, config): #arguments are the websocket and the config file
     
  
     login = auth_pb2.LoginRequest(
          firm=config["websocket"]["firm"],
          username=config["websocket"]["username"],
          password=config["websocket"]["password"],
          app_name=config["websocket"]["app_name"],
          app_license=config["websocket"]["app_license"]
     )

     #client message helper:
     client_msg = ClientMessageHelper.create_client_message({"login_request": login})
     client_msg = encode_message(client_msg)
     print("Sending LoginRequest...")
     await ws.send(client_msg)
     print(client_msg)
     global running
     running = True
     #making a client mesasge helper.


    # response = await ws.recv()
     #print(decode_message(response))
   #  return response
     

#handle the login response
async def handle_login(response):
     response = decode_message(response)

     #grab token

     #grab all the other important information


#handle the heartbeat response
async def handle_heartbeat(response):
     pass

#heartbeat for every 20 seconds
async def send_message(ws, message):
     request = ClientMessageHelper.create_client_message(message)
     encrypted_request = encode_message(request)
     await ws.send(encrypted_request)

async def send_heartbeat(ws):
     global running
     while running:
          
          heartbeat_msg = service_pb2.Heartbeat(timestamp=int(time.time() * 1000))


          await send_message(ws, {"heartbeat": heartbeat_msg})
          print("Heartbeat sent.")

          await asyncio.sleep(heartbeat)   
#authentication using login
async def authenticate():
     pass

async def listen(ws):
    global running
    try:
        while running:
            msg = await ws.recv()
            #print("Received:", decode_message(msg))
            if decode_message(msg).HasField("login_response"):
               login_response = decode_message(msg).login_response
               print(login_response)
            else:
                print("no sir")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by server.")
        running = False
    except Exception as e:
        print("Error while listening:", e)
        running = False

async def main():
    config = load_config("config/config.yaml")
    url = config["websocket"]["url"]

    try:
        async with websockets.connect(url) as websocket:
            await asyncio.gather(
                connect_with_auth(websocket, config),
                send_heartbeat(websocket),
               listen(websocket)
            )
    except Exception as e:
        print("WebSocket error:", e)




asyncio.run(main())
# config = load_config()
