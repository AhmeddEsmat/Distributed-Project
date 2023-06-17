import socket
import threading
from Objects import Objects
import pickle
from Racer import Racer


class CarRacingServer:

    def __init__(self):
        self.objects = Objects()
        self.host = "localhost"  # Server IP address
        self.port = 5050  # Server port
        self.server_socket = None
        self.players = []
        self.lock = threading.Lock()

    def sort_racers_by_distance(self, players):
        sorted_racers = sorted(players, key=lambda laeeb: laeeb.dist_covered, reverse=True)
        for i, player in enumerate(sorted_racers):
            player.position = i + 1
        return sorted_racers

    def update_racer(self, player):
        for i in range(len(self.players)):
            if self.players[i].username == player.username:
                self.lock.acquire()
                self.players[i] = player
                self.lock.release()
                return

    def register_racer(self, player):
        for i in self.players:
            if i.username == player.username:
                return "Username taken"
        self.lock.acquire()
        self.players.append(player)
        self.lock.release()
        return "Successfully joined the race!!!"

    def update_map(self):
        while True:
            if self.objects.game_ended:
                self.objects = Objects()
                self.players = []
            if len(self.players) > 1:
                self.objects.game_started = True
            self.lock.acquire()
            self.sort_racers_by_distance(self.players)
            self.lock.release()
            finished = True
            if len(self.players) < 1:
                finished = False
            for player in self.players:
                if not player.finished:
                    finished = False
                    break
            self.objects.game_ended = finished

    def receive_data(self, client_socket):
        while True:
            try:
                sterilized_object = client_socket.recv(2048)
                received_object = pickle.loads(sterilized_object)
                if isinstance(received_object, Racer):
                    self.update_racer(received_object)
                    break
            except Exception:
                client_socket.close()
                break

    def start(self):

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print('Server started on {}:{}'.format(self.host, self.port))
        updating_thread = threading.Thread(target=self.update_map)
        updating_thread.start()
        while True:
            client_socket, client_address = self.server_socket.accept()
            print('New connection from {}:{}'.format(client_address[0], client_address[1]))
            connection_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            connection_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(4096).decode()
                username = message.split(",")[1]
                player = Racer()
                player.username = username
                msg = self.register_racer(player)
                client_socket.send(msg.encode())
                if msg == "Successfully joined the race!!!":
                    break
            except socket.error:
                try:
                    client_socket.close()
                except:
                    print("x")
                break

        while True:
            try:
                if not self.objects.game_ended:
                    self.receive_data(client_socket)
                    serialized_data = pickle.dumps(self.objects)
                    try:
                        client_socket.send(serialized_data)
                    except OSError as e:
                        print(f"Error occurred while sending data: {e}")
                        break

                    # send racers
                    serialized_data = pickle.dumps(self.players)
                    try:
                        self.lock.acquire()
                        client_socket.send(serialized_data)
                        self.lock.release()
                    except OSError as e:
                        print(f"Error occurred while sending data: {e}")
                        break
            except socket.error:
                client_socket.close()
                break


if __name__ == '__main__':
    server = CarRacingServer()
    server.start()
