import asyncio
import time
import websockets
from tools.ClientMessageHelper import create_client_message
from tools.ProtoUtils import encode_message, decode_message
from proto.t4.v1.auth import auth_pb2
from proto.t4.v1 import service_pb2

class T4APIClient:

    #initializes core attributes
    def __init__(self, config):
        self.wsUrl = config['websocket']['url']
        self.apiUrl = config['websocket']['api']
        self.firm: config['websocket']['firm']
        self.username: config['websocket']['username']
        self.password: config['websocket']['password']
        self.app_name: config['websocket']['app_name']
        self.app_license: config['websocket']['app_license']
        self.priceFormat: config['websocket']['priceFormat']
        self.ws = None
        self.lastMessage = None
        self.running = False
        self.heartbeat_time = 20 

    async def connect(self):
    
        try:
            async with websockets.connect(self.wsUrl) as websocket:
                self.running = await self.authenticate() #authenitcation returns 
                
                if not self.running: #if authentication fails give error message
                    print("authentication failed")


        except Exception as e:
            print("Failure", e)
    
    #envelopes, encrypts, and sends message to the server
    def send_message(self, message):
        request = create_client_message(message)
        encrypted_request = encode_message(request)
        self.ws.send(encrypted_request)

    async def authenticate(self):
        login_info = auth_pb2.LoginRequest(
          firm= self.firm,
          username= self.username,
          password=self.password,
          app_name=self.app_name,
          app_license=self.app_license
        )

        #envelope and encrypt request
        self.send_message(login_info)

        #check response
        login_response = await self.ws.recv()

        return self.handleLogin(login_response)

    def handleLogin(self, message):
        message = decode_message(message) #decodes message

        #what it means if it's sucessful
        imp_var = message['something']
        
        #if false return False and end
        if imp_var == "test":
            return False

        #getter functions responsiblities


        return True



        


