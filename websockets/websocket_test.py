import asyncio
import websockets
import yaml

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
     login_msg = {
     "firm": config["websocket"]["firm"],
     "username": config["websocket"]["username"],
     "password": config["websocket"]["password"],
     "app_name": config["websocket"]["app_name"],
     "app_license": config["websocket"]["app_license"]
     }
     
     ##must send the information using the protocol buffers not json.
     await ws.send()
     response = await ws.recv()
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

        # Example: send another message after login

        # Receive message
        reply = await websocket.recv()
        print("Server says:", reply)

asyncio.run(main())
