import asyncio
import websockets
import yaml
#gets the proto file for logging in
import sys, os
sys.path.insert(0, os.path.abspath("proto"))

from proto.t4.v1.auth import auth_pb2
from tools.ClientMessageHelper import ClientMessageHelper
#port443

#heartbeat connection every 20 seconds (only have 3 consecutive heratbeats to send before the connection is termianted)
port = 443
API_KEY = "TEST"
WS_URL = "wss://wss-sim.t4login.com/v1" # connection to simulator

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
     print("Sending LoginRequest...")
     await ws.send(client_msg.SerializeToString())
     print(login.SerializeToString())

     #making a client mesasge helper.


     response = await ws.recv()
     print("Received:")
     print(response)


#heartbeat for every 20 seconds
async def heartbeat():
     pass
#authentication using login
async def authenticate():
     pass


async def main():
    config = load_config("config/config.yaml")
    url = config["websocket"]["url"]

    async with websockets.connect(url) as websocket:
        await connect_with_auth(websocket, config)



        

asyncio.run(main())
# config = load_config()
