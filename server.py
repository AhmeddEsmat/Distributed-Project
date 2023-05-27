import socket
from _thread import *
import sys

server = "192.168.1.11"  # Enter the server IP address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")



def read_pos(str):
    str = str.split(",")
    return int(float(str[0])), int(float(str[1])), int(float(str[2]))


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])


pos = [(0,0,0),(100,100,0)]  # Update initial positions to include rotation angle
rotation_angle = [0, 0]  # Track rotation angle for each player

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = (data[0], data[1], rotation_angle[player])  # Update position and rotation angle

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = make_pos(pos[0])
                else:
                    reply = make_pos(pos[1])

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except Exception as e:
            print("Error:", str(e))
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
