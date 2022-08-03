import socket

#Server Variables
Port = 9879
Host = socket.gethostbyname(socket.gethostname())
Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Address = (Host, Port)

#Message Variables
message_cap = 64
message_format = 'utf-8'
disconnect_message = "has disconnected."

#Connect to server.
Client.connect(Address)

#Format message
def send(message):

    #Encode the message into a byte format.
    message = message.encode(message_format)
    #Find length of the message
    message_length = len(message)
    #Encode message into utf-8 format.
    send_length = str(message_length).encode(message_format)
    #Add spaces to create a padding to the 64 bytes.
    send_length += b' ' * (message_cap - len(send_length))
    Client.send(send_length)
    Client.send(message)
    print(Client.recv(2000).decode(message_format))

send("Hello")