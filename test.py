import random
from time import sleep
import pygame
import math
import tkinter as tk
from PIL import Image, ImageTk

class Test:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.username = ""
        self.previous_score = 0  # New score variable
        self.previous_distance = 0  # New score variable
        self.previous_time = 0  # New score variable
        self.timer = 60  # Set the timer to 1 minute (60 seconds)
        self.login_window()
        self.initialize()

    def login_window(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Load and resize the background image
        background_image = Image.open("LoginBg.jpg")
        background_image = background_image.resize((800, 600), Image.LANCZOS)  # Use LANCZOS resampling
        bg_image = ImageTk.PhotoImage(background_image)

        # Create a label to hold the background image
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self.root, text="Enter your username:", font=("Arial", 16), bg="white")
        label.place(relx=0.5, rely=0.4, anchor="center")  # Center the label

        entry = tk.Entry(self.root, font=("Arial", 14))
        entry.place(relx=0.5, rely=0.5, anchor="center")  # Center the entry field

        button = tk.Button(self.root, text="Start Game", font=("Arial", 14),
                           command=lambda: self.start_game(entry.get()))
        button.place(relx=0.5, rely=0.6, anchor="center")  # Center the button

        self.error_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red", bg="white")
        self.error_label.place(relx=0.5, rely=0.7, anchor="center")  # Center the error label

        # Set the background image as an attribute to prevent it from being garbage collected
        self.root.bg_image = bg_image

        self.root.mainloop()

    def start_game(self, username):
        username = username.strip()
        if not username:
            self.show_error_message("Please enter a username!")
        else:
            self.username = username
            self.root.destroy()  # Close the login window
            self.initialize()
            self.racing_window()

    def show_error_message(self, message):
        self.error_label.config(text=message)

    def initialize(self):
        # pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.crashed = False
        self.font = pygame.font.SysFont("Arial", 24)


        self.carImg = pygame.image.load('car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49
        self.count = self.previous_score  # Set the count to the previous score
        self.distance_covered = self.previous_distance  # Set the distance covered to the previous distance
        self.time = self.previous_time  # Set the time to the previous time

        # enemy_car
        self.enemy_car = pygame.image.load('enemy_car_1.png')
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load("back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.max_bg_speed = 30  # Maximum background speed
        
        self.car_speed = 4  # Set starting speed to 0
        self.car_speed_increment = 2

        self.max_car_speed = 30 # Set maximum speed to 120

    def car(self, car_x_coordinate, car_y_coordinate, font):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))
        username_text = font.render(self.username, True, (0, 0, 255))  # Blue color (RGB: 0, 0, 255)
        username_text_rect = username_text.get_rect(center=(car_x_coordinate + self.car_width // 2, car_y_coordinate + self.car_width + 60))
        self.gameDisplay.blit(username_text, username_text_rect)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Racing Game')
        self.run_car()

    def run_car(self):
        self.clock.tick()  # Start the clock
        speed_increment_count = 0
        enemy_car_speed_increment = 0.5  # Increase in enemy car speed when player speed increases
        self.move_left = False
        self.move_right = False
        

        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.move_right = True
                    elif event.key == pygame.K_UP:
                         if self.car_speed < 30:
                            self.car_speed += self.car_speed_increment
                            self.enemy_car_speed += self.car_speed_increment  # Increase enemy car speed
                            self.bg_speed += 2  # Increase background speed
                            self.bg_speed = min(self.bg_speed, self.max_bg_speed)  # Limit background speed
                            print("CAR SPEED:", self.car_speed)
                    elif event.key == pygame.K_DOWN:
                        self.car_speed -= self.car_speed_increment
                        self.enemy_car_speed -= self.car_speed_increment  # Decrease enemy car speed
                        self.bg_speed -= 2  # Decrease background speed
                        self.bg_speed = max(self.bg_speed, 0)  # Ensure minimum background speed
                        if(self.car_speed < 2):
                            self.enemy_car_speed = 2
                        print("CAR SPEED:", self.car_speed)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.move_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.move_right = False

            if self.move_left:
                    self.car_x_coordinate -= 5  # Move one lane to the left
                    print("CAR X COORDINATE:", self.car_x_coordinate)
            elif self.move_right:
                    self.car_x_coordinate += 5  # Move one lane to the right
                    print("CAR X COORDINATE:", self.car_x_coordinate)

            # Ensure the car speed does not go below zero
            self.car_speed = max(0, self.car_speed)
            self.enemy_car_speed = max(0, self.enemy_car_speed)

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            #if self.car_x_coordinate <= 310 or self.car_x_coordinate >= 450:
               # self.display_message("Off Road!")

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate, self.font)
            self.highscore(self.count, self.car_speed, self.distance_covered, self.timer)
            self.count += self.bg_speed
            self.distance_covered += self.car_speed * 0.1  # Update distance covered based on speed

            self.timer -= self.clock.tick(60) / 1000  # Update the timer based on the elapsed time

            if self.timer <= 0:
                self.crashed = True
                self.display_message("Time's up!")

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")
                      
            if self.car_x_coordinate <= 270 or self.car_x_coordinate >= 480:
                self.crashed = True
                self.display_message("Off Road!")

            pygame.display.update()
            self.clock.tick(60)

            # Increase enemy car frequency and background speed every 10 increments in speed
            if self.car_speed % 10 == 0 and speed_increment_count < self.car_speed // 10:
                speed_increment_count += 1
                self.enemy_car_speed += enemy_car_speed_increment
                self.bg_speed += 1
                self.bg_speed = min(self.bg_speed, self.max_bg_speed)  # Limit background speed
                enemy_car_speed_increment += 1  # Increase the increment for enemy car speed
            print("score is",self.count)
            self.highscore(self.count, self.car_speed, self.distance_covered, self.timer)
        

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        self.previous_score = self.count
        self.previous_distance = self.distance_covered
        self.previous_time = self.timer
        print(self.previous_score,"prev score")
        print(self.count)
        self.initialize()
        self.racing_window()
        self.count=self.previous_score
        self.distance_covered=self.previous_distance
        self.timer=self.previous_time
        print(self.count)
        print(self.previous_score,"after score")

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = self.bg_y2 - self.bgImg.get_height()

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = self.bg_y1 - self.bgImg.get_height()

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count, car_speed, distance_covered, timer):
        font = pygame.font.SysFont("arial", 20)
        text_score = font.render("Score: " + str(self.count), True, self.white)
        text_speed = font.render("Speed: " + str(car_speed) + " km/h", True, self.white)
        text_distance = font.render("Distance: " + str(int(distance_covered)) + " m", True, self.white)
        text_timer = font.render("Time: {:.2f}".format(timer), True, self.white)  # Display the remaining time
        self.gameDisplay.blit(text_score, (0, 0))
        self.gameDisplay.blit(text_speed, (0, 25))
        self.gameDisplay.blit(text_distance, (0, 50))
        self.gameDisplay.blit(text_timer, (0, 75))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))

if __name__ == '__main__':
    car_racing = Test()

