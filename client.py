import socket

print("Welcome to the KeyValue Service Client")

s = socket.socket()

# ask for IP address or Hostname until valid
while True:
    hostname = input("Enter the IP address or Hostname of the server: ")
    try:
        s.connect((hostname, 3000))
        break
    except:
        print(f"IP address or Hostname \"{hostname}\" is not valid\n")
        continue

print("Please wait while I connect you...")
print(s.recv(1024).decode())

while True:

    try:
        inp = input("KeyValue Service> ").lower().split()

        # check for null input
        if not inp:
            print(f"Invalid command: ''\n")
            continue
        else:
            action, *args = inp

        if action == "help":
            print("help \nget key \nput key value \nvalues \nkeyset \nmappings \nbye\n")

        elif action == "get":
            s.send(str([action, *args]).encode())
            response = s.recv(1024).decode()
            print(response, end='\n\n')

        elif action == "put":
            s.send(str([action, *args]).encode())
            response = s.recv(1024).decode()
            print(response, end='\n\n')

        elif action == "mappings":
            s.send(str([action, *args]).encode())
            # convert response into python dictionary
            response = eval(s.recv(1024).decode())
            for k, v in response.items():
                print(k, v)
            print()

        elif action == "keyset":
            s.send(str([action, *args]).encode())
            response = s.recv(1024).decode()
            print(response, end='\n\n')

        elif action == "values":
            s.send(str([action, *args]).encode())
            response = s.recv(1024).decode()
            print(response, end='\n\n')

        elif action == "bye":
            s.send(str([action, *args]).encode())
            response = s.recv(1024).decode()
            print(response)
            s.close()
            break

        # for an invalid command
        else:
            command = f"\"{action} {' '.join(args).strip()}\"" if args else f"\"{action}\""
            print(f"Invalid command: {command}\n")

    except:
        s.close()
        break
