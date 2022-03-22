import socket
import threading

s = socket.socket()
s.bind(('', 3000))
# listens for 3 connections max
s.listen(3)

store = {}


def on_new_client(conn, addr):
    conn.send("Welcome to the KeyValue Service".encode())
    # "addr[1]" is client address
    print(f"{addr[1]} connected")

    while True:
        try:
            # unpack action and args from client message
            action, *args = eval(conn.recv(1024).decode())

            if action == "get":
                if len(args) != 1:
                    conn.send(f"Invalid command: \"get {' '.join(args)}\"".encode())
                    continue
                if args[0] in store:
                    conn.send(str(store[args[0]]).encode())
                    print(f"{addr[1]}: \"get {args[0]}\"")
                else:
                    conn.send(f"Cannot find key \"{args[0]}\" in the data store.".encode())
                continue

            elif action == "put":
                if len(args) != 2:
                    conn.send(f"Invalid command: \"put {' '.join(args)}\"".encode())
                    continue
                key, value = args
                try:
                    store[key] = int(value)
                    conn.send("Ok.".encode())
                    print(f"{addr[1]}: \"put {key} {value}\"")
                except ValueError:
                    conn.send(f"Value \"{value}\" is not valid ".encode())
                continue

            elif action == "mappings":
                conn.send(str(store).encode())
                print(f"{addr[1]}: \"mappings\"")
                continue

            elif action == "keyset":
                conn.send(str(list(store.keys())).encode())
                print(f"{addr[1]}: \"keyset\"")
                continue

            elif action == "values":
                conn.send(str(list(store.values())).encode())
                print(f"{addr[1]}: \"values\"")
                continue

            elif action == "bye":
                conn.send("See you later.".encode())
                conn.close()
                print(f"{addr[1]} disconnected")
                break

        except:
            conn.close()
            print(f"{addr[1]} disconnected")
            break


# accept client connections and create a new thread for each connection
while True:
    conn, addr = s.accept()
    threading.Thread(target=on_new_client, args=(conn, addr)).start()
