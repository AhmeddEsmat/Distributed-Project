from time import sleep
import tkinter as tk
import pygame
from PIL import Image, ImageTk
from Objects import Objects
from Racer import Racer
import socket
import pickle
import random
from Chat import Client


class CarRacing:

    def __init__(self):
        self.Chat_IP = 'localhost'
        self.Chat_PORT = 7000
        self.max_bg_speed = 40
        self.max_enemy_speed = 42
        self.Signin_windowactive = None
        self.host_racer = None
        pygame.init()
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 5050))
        self.racers = []




    def Signin_Window(self):
        # Create the sign in window

        self.Signin_Window = tk.Tk()
        self.Signin_Window.title("Sign in")
        self.Signin_Window.geometry("800x600")
        self.Signin_windowactive = True

        image = Image.open("./img/LoginBg.jpg")
        resized_image = image.resize((800, 600), Image.ANTIALIAS)
        background_image = ImageTk.PhotoImage(resized_image)

        background_label = tk.Label(self.Signin_Window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        login_frame = tk.Frame(self.Signin_Window, bg="white")
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create labels
        self.label_username = tk.Label(login_frame, text="Please enter username:", font=("Arial", 16))
        self.label_username.pack()
        self.entry_username = tk.Entry(login_frame)
        self.entry_username.pack()

        # Create label for displaying the result
        self.label_result = tk.Label(login_frame, text="")
        self.label_result.pack()

        # Create login button
        self.button_login = tk.Button(login_frame, text="Join Race", command=self.username_verfication)
        self.button_login.pack()

        # Create error label
        self.error_label = tk.Label(login_frame, text="", font=("Arial", 12), fg="red", bg ="white")
        self.error_label.pack()

        self.label_username.configure(bg="white", highlightthickness=0)
        self.entry_username.configure(bg="white", highlightthickness=0)
        login_frame.configure(bg="white", highlightthickness=0)

        # Run the main window loop
        self.Signin_Window.mainloop()

    def username_verfication(self):
        username = self.entry_username.get()
        if(username == ""):
            self.show_error_label("Please enter a username!")
            return
        else:
            self.show_error_label("")         
        sendtoserver = "Verify," + username
        self.client_socket.send(sendtoserver.encode())
        server_message = self.client_socket.recv(1024).decode()
        if server_message == "Successfully joined the race!!!":
            Client(self.Chat_IP, self.Chat_PORT, username)
            self.host_racer = Racer()
            self.host_racer.username = username
            self.initialize()
            self.label_result.config(text="Successfully joined the race!!!", fg="green")
            self.Signin_Window.after(1500, self.racing_window)

        if server_message == "Username taken":
            self.label_result.config(text="Invalid entry username already taken", fg="red")

        if server_message == "Enter a username":
            self.label_result.config(text="Enter a username", fg="red")

    def show_error_label(self, message):
        self.error_label.config(text = message)

    def initialize(self):
        # object inits
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.enemy_car_height = 100
        self.enemy_car_speed = 2
        self.min_enemy_speed = 1
        self.bg_speed = 0
        self.dummy_init = False
        random.seed(self.host_racer.dist_covered)
        self.enemy_car_startx = random.randint(310, 450)
        self.enemy_car_starty = -600
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.timer = 60
        self.host_objects = Objects()
        self.host_racer.crashed = False
        self.host_racer.offroad = False
        self.host_car_img = pygame.image.load('./img/car.png')
        self.rival_car_img = pygame.image.load('./img/rival_car.png')
        self.upward_arrow_img = pygame.image.load('./img/upward_arrow.png')
        self.downward_arrow_img = pygame.image.load('./img/downward_arrow.png')
        self.finish_img = pygame.image.load('./img/finish.png')
        self.host_racer.car_x_coordinate = (self.display_width * 0.45)
        self.host_racer.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49
        # enemy_car
        self.enemy_car = pygame.image.load('.\\img\\enemy_car_1.png')
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load(".\\img\\back_ground.jpg")

    def receive_data(self):
        sterilized_object = self.client_socket.recv(2048)
        received_object = pickle.loads(sterilized_object)
        if isinstance(received_object, Objects):
            self.host_objects = received_object

        elif isinstance(received_object[0], Racer):
            self.racers = received_object
            for racer in self.racers:
                if racer.username == self.host_racer.username:
                    self.host_racer.position = racer.position
        else:
            print("Not correct data type received by the Client(surroundings,racers)")

    def car(self, car_x_coordinate, car_y_coordinate, ifhost):
        if ifhost:
            self.gameDisplay.blit(self.host_car_img, (car_x_coordinate, car_y_coordinate))
        else:
            self.gameDisplay.blit(self.rival_car_img, (car_x_coordinate, car_y_coordinate))



    def racing_window(self):
        if self.Signin_windowactive:
            self.Signin_windowactive = False
            self.Signin_Window.destroy()
        self.gameDisplay = pygame.display.set_mode(
            (self.display_width, self.display_height))
        pygame.display.set_caption('Multiplayer Race')

        self.run_car()

    def run_car(self):
        self.clock.tick()
        self.move_left = False
        self.move_right = False

        while True:
            if not self.dummy_init and self.host_objects.game_started:
                self.display_message("Race Begin", 2)
                self.dummy_init = True

            if self.host_racer.crashed and self.host_objects.game_started:
                self.enemy_car_starty = 0 - self.enemy_car_height
                random.seed(self.host_racer.dist_covered)
                self.enemy_car_startx = random.randint(310, 450)
                self.enemy_car_speed = 5
                self.bg_speed = 4
                self.host_racer.car_x_coordinate = (self.display_width * 0.45)
                if self.host_racer.offroad:
                    self.display_message("Offroad", 2)
                else:
                    self.display_message("Crashed", 2)
                self.host_racer.crashed = False
                self.host_racer.offroad = False

            serialized_data = pickle.dumps(self.host_racer)
            # Send the player object to the server
            self.client_socket.send(serialized_data)

            self.receive_data()
            self.receive_data()

            if self.host_objects.game_started:
                self.host_racer.dist_covered += self.bg_speed * 1.2
                self.enemy_car_starty += self.enemy_car_speed
                self.bg_y1 += self.bg_speed
                self.bg_y2 += self.bg_speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    pygame.quit()
                    self.client_socket.close()
                    print("Game closed")


                if self.host_objects.game_started:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if (self.enemy_car_speed < self.max_enemy_speed) and (self.bg_speed < self.max_bg_speed):
                                self.enemy_car_speed += 2
                                self.bg_speed += 2

                        if event.key == pygame.K_DOWN:
                            if (self.enemy_car_speed > self.min_enemy_speed) and (self.bg_speed >= 2):
                                self.enemy_car_speed -= 2
                                self.bg_speed -= 2

                        if event.key == pygame.K_LEFT:
                            self.move_left = True

                        if event.key == pygame.K_RIGHT:
                            self.move_right = True

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.move_left = False
                        elif event.key == pygame.K_RIGHT:
                            self.move_right = False

            if self.host_objects.game_started:

                if self.move_left:
                        self.host_racer.car_x_coordinate -= 5  # Move one lane to the left
                        print("CAR X COORDINATE:", self.host_racer.car_x_coordinate)
                elif self.move_right:
                        self.host_racer.car_x_coordinate += 5  # Move one lane to the right
                        print("CAR X COORDINATE:", self.host_racer.car_x_coordinate)
            if self.bg_y1 >= self.display_height:
                self.bg_y1 = -600

            if self.bg_y2 >= self.display_height:
                self.bg_y2 = -600

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                random.seed(self.host_racer.dist_covered)
                self.enemy_car_startx = random.randint(310, 450)

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)

            if self.host_racer.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.host_racer.car_x_coordinate > self.enemy_car_startx and self.host_racer.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.host_racer.car_x_coordinate + self.car_width > self.enemy_car_startx and self.host_racer.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.host_racer.crashed = True

            if self.host_racer.car_x_coordinate < 270 or self.host_racer.car_x_coordinate > 480:
                self.host_racer.crashed = True
                self.host_racer.offroad = True
            self.Distance_travelled(self.host_racer.dist_covered)
            self.Car_Rank(self.host_racer.position)
            self.Car_Speed(self.bg_speed)
            self.view_racers(self.racers)
            self.display_timer()
            if not self.host_objects.game_started:
                self.wait_for_other_racers()

            if self.host_objects.game_started:
                self.timer -= self.clock.tick(60) / 1000  # Update the timer based on the elapsed time

            if self.timer <= 0:
                self.display_message("Time's up!", 7)
                self.host_racer.finished = True
                print("Race Finished")
                pygame.QUIT
                pygame.quit()
            pygame.display.update()
            self.clock.tick(60)

    def view_racers(self, racers):
        for racer in racers:
            if racer.car_x_coordinate and racer.car_y_coordinate:
                if_host_racer = racer.username == self.host_racer.username
                if if_host_racer:
                    self.car(racer.car_x_coordinate, racer.car_y_coordinate, True)
                    self.display_racer_username(racer.username, racer.car_x_coordinate, racer.car_y_coordinate)
                    continue

                verticalOffset = int(racer.dist_covered / 100) - int(self.host_racer.dist_covered / 100)

                if 0 < verticalOffset < 6:
                    new_y_coordinate = self.host_racer.car_y_coordinate - verticalOffset * 100
                    self.car(racer.car_x_coordinate, new_y_coordinate, False)
                    self.display_racer_username(racer.username, racer.car_x_coordinate, new_y_coordinate)
                elif verticalOffset > 6:
                    self.upward_arrow(racer.car_x_coordinate)
                    self.display_racer_username(racer.username, racer.car_x_coordinate, 1)
                elif verticalOffset < 0:
                    self.downward_arrow(racer.car_x_coordinate)
                    self.display_racer_username(racer.username, racer.car_x_coordinate, 420)
                elif verticalOffset == 0:
                    self.car(racer.car_x_coordinate, self.host_racer.car_y_coordinate, if_host_racer)
                    self.display_racer_username(racer.username, racer.car_x_coordinate,
                                                self.host_racer.car_y_coordinate)

    def upward_arrow(self, x_coordinate):
        self.gameDisplay.blit(self.upward_arrow_img, (x_coordinate, 25))

    def downward_arrow(self, x_coordinate):
        self.gameDisplay.blit(self.downward_arrow_img, (x_coordinate, 560))
    def display_message(self, msg, time):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.update()
        self.clock.tick(60)
        sleep(time)


    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))
        
        if self.bg_y1 >= self.display_height:
            self.bg_y1 = self.bg_y2 - self.bgImg.get_height()

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = self.bg_y1 - self.bgImg.get_height()

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def Distance_travelled(self, distance):
        distance = int(distance / 100)
        if distance > 1000:
            distance = 1000
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Distance travelled:" + str(distance) + "m", True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def Car_Speed(self, Speed):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Speed:" + str(Speed) + "m/s", True, self.white)
        self.gameDisplay.blit(text, (0, 50))

    def Car_Rank(self, car_rank):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Rank:" + str(car_rank), True, self.white)
        self.gameDisplay.blit(text, (0, 75))


    def wait_for_other_racers(self):
        font = pygame.font.SysFont("Vineta BT", 42)
        text = font.render("Waiting", True, self.white)
        text_mod = text.get_rect(center=(self.gameDisplay.get_width() // 2, 200))
        self.gameDisplay.blit(text, text_mod)

        text = font.render("for", True, self.white)
        text_mod = text.get_rect(center=(self.gameDisplay.get_width() // 2, 240))
        self.gameDisplay.blit(text, text_mod)

        text = font.render("other racers to join....", True, self.white)
        text_mod = text.get_rect(center=(self.gameDisplay.get_width() // 2, 280))
        self.gameDisplay.blit(text, text_mod)

        text = font.render("Good Luck", True, self.white)
        text_mod = text.get_rect(center=(self.gameDisplay.get_width() // 2, 320))
        self.gameDisplay.blit(text, text_mod)

    def display_racer_username(self, username, x, y):
        font = pygame.font.SysFont("arial", 20)
        text = font.render(username, True, (0,0,255))
        username_text_rect = text.get_rect(center=(x + self.car_width // 2, y + self.car_width + 60))
        self.gameDisplay.blit(text, username_text_rect)

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))

    def display_timer(self):
        font = pygame.font.SysFont("arial", 20)
        text_timer = font.render("Time: {:.2f}".format(self.timer) + "sec", True, self.white)  # Display the remaining time
        self.gameDisplay.blit(text_timer, (0, 25))
        self.gameDisplay.blit(text_timer, (0, 25))


if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.Signin_Window()
