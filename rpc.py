import xmlrpc.client

def main():
    proxy =xmlrpc.client.ServerProxy("http://localhost:1234/RPC2")
    
    x=float(input("Enter the first number(x):"))
    y=float(input("Enter the second number(y):"))
    
    result_add=proxy.add(x,y)
    result_subtract =proxy.subtract(x,y)
    
    print(f"Addition result:{result_add}")
    print(f"Substraction result:{result_subtract}")
    
    
if __name__=="__main__":
    main()


#server
from xmlrpc.server import *

class MathOperations:
    def add(self,x,y):
        return x + y
    def subtract(self,x,y):
        return x - y
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths= ('/RPC2',)
    
def main():
    server=SimpleXMLRPCServer(('localhost',1234),requestHandler=RequestHandler)
    server.register_instance(MathOperations())
    
    print("RPC server is listening on port 1234...")
    server.serve_forever()
    
    
if __name__=="__main__":
   main()