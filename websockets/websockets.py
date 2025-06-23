import asyncio
from websockets.sync.client import connect
#port443

#heartbeat connection every 20 seconds (only have 3 consecutive heratbeats to send before the connection is termianted)
port = 443
API_KEY = "TEST"
WS_URL = "wss://wss-sim.t4login.com/v1" # connection to simulator


#the actual websocket connection
async def connect():
     
     pass


#heartbeat for every 20 seconds
async def heartbeat():
     pass

#authentication using login
async def authenticate():

