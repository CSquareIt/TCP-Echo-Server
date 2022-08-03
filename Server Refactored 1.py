import socket
import threading


# Specify what port and grab my IP to run the server on automatically.
Port = 9879
Host = socket.gethostbyname(socket.gethostname())

# Format and store IP and Port in (IP, Port) format. 
Address = (Host, Port)

#Tells the socket that it is looking for a IPv4 address and describes the type of socket we're looking to use.
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Function to allow multiple attempts to use the port.
Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Binds the socket to my IP and port.
Server.bind(Address)

#Setting perameters that our server will allow messages through.
message_cap = 64
message_format = 'utf-8'

disconnect_message = "has disconnected."

print(Server)

#Thread handling what happens when a client connects. Each client will run this thread.
def handle_client(connection, address):
    print("user {address} connected.")
    #set's the connection to True
    connected = True

    #We wait for the client to send us information.
    while connected:
        #The server waits for a message, and then decodes the message into a string using utf-8 format.
        message_encoded = connection.recv(message_cap).decode(message_format)

        if message_encoded:
            #Tells the server how many bytes the message recieved is.
            message_encoded = int(message_encoded)
            #This tells the server how many bytes we are recieving from the client.
            message = connection.recv(message_encoded).decode(message_format)
            #Print's the client's message in the appropriate format.
            print(f"{address}: {message}")
            #Sends the same message back to the client.
            connection.send(message.encode(message_format))

            if message == disconnect_message:
                #prints a disconnect message to the client.
                print(f"{address}: {disconnect_message}")
                #Turns connection status to False, terminatiing connection
                connected = False

            

    connection.close()



#Socket starting the server and allowing connections
def start():
    #The server starts waiting for commands.
    Server.listen()

    #Print function to give verification that the server is running and what IP the server is using.
    print(f"The server is running on {Host}")

    #Infinite loop to allow accepting connections
    while True:
        #Function to wait for requests to access the server and saves their connection and IP.
        connection, address = Server.accept()
        #Setting up the thread to pass the argument to the handle_client function.
        thread =  threading.Thread(target=handle_client, args=(connection, address))
        #Starts the thread's activities
        thread.start()
        #Print function to manage active connections. This subracts our connection for accuracy.
        print(f"Active Connections: {threading.active_count() - 1}")


print("Server is starting...")
start()