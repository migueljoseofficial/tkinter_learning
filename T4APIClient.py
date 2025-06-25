import asyncio
import time
import websockets
from tools.ClientMessageHelper import ClientMessageHelper
from tools.ProtoUtils import encode_message, decode_message
from proto.t4.v1.auth import auth_pb2
from proto.t4.v1 import service_pb2

class Client:

    #initializes core attributes
    def __init__(self, config):
        self.wsUrl = config['websocket']['url']
        self.apiUrl = config['websocket']['api']
        self.firm= config['websocket']['firm']
        self.username=config['websocket']['username']
        self.password=config['websocket']['password']
        self.app_name= config['websocket']['app_name']
        self.app_license= config['websocket']['app_license']
        self.priceFormat= config['websocket']['priceFormat']
        self.ws = None
        self.lastMessage = None
        self.running = False
        self.heartbeat_time = 20 

    #connects to api
    async def connect(self):
    
        try:
            async with websockets.connect(self.wsUrl) as self.ws:
                await asyncio.gather(
                    self.authenticate(),
                    self.send_heartbeat(),
                    self.listen()
            )
                 #authenitcation returns 
                
                if not self.running: #if authentication fails give error message
                    print("authentication failed")
        except Exception as e:
            print("Failure", e)
    
    #envelopes, encrypts, and sends message to the server
    async def send_message(self, message):
        request = ClientMessageHelper.create_client_message(message)
        encrypted_request = encode_message(request)
        await self.ws.send(encrypted_request)

    #sends login request
    async def authenticate(self):
        login_info = auth_pb2.LoginRequest(
          firm = self.firm,
          username = self.username,
          password =self.password,
          app_name = self.app_name,
          app_license = self.app_license
        )

        #envelope and encrypt request
        await self.send_message({"login_request": login_info})

        #check response
        #login_response = await self.ws.recv()
    
        self.running = True
        # if message.HasField("login_response"):
        #     login_response = message.login_response
        #     print(login_response)
        # 

       # return self.handle_login(login_response)

    def handle_login(self, message):
        


        return True
    
    async def listen(self): #listens for any websocket messages
        
        try:
            while self.running:
                msg = await self.ws.recv()
                self.proccess_server_message(msg)
    
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by server.")
            self.running = False
        except Exception as e:
            print("Error while listening:", e)
            self.running = False

    #this will be inside of the listen function.
    #sends each message to a handling funciton. Which will just parse the data that is needed
    def proccess_server_message(self, msg):
        msg = decode_message(msg)
        print(type(msg))
        if msg.login_response:
            print(msg.login_response)
            self.handle_login(msg)
    
        elif msg.heartbeat:
            print()

    async def send_heartbeat(self):
  
        while self.running:
            
            heartbeat_msg = service_pb2.Heartbeat(timestamp=int(time.time() * 1000))


            await self.send_message({"heartbeat": heartbeat_msg})
            print("Heartbeat sent.")

            await asyncio.sleep(self.heartbeat_time)



        


