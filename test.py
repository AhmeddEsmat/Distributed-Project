import random
from time import sleep
import pygame
import math

class Test:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.initialize()

    def initialize(self):
        self.crashed = False

        self.carImg = pygame.image.load('car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

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
        self.count = 0
        self.distance_covered = 0

        self.car_speed = 1
        self.car_speed_increment = 2

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Racing Game')
        self.run_car()

    def run_car(self):
        self.clock.tick()  # Start the clock
        self.timer = 60  # Set the timer to 1 minute (60 seconds)
        speed_increment_count = 0
        enemy_car_speed_increment = 0.5  # Increase in enemy car speed when player speed increases

        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_coordinate -= 70  # Move one lane to the left
                        print("CAR X COORDINATE:", self.car_x_coordinate)
                    elif event.key == pygame.K_RIGHT:
                        self.car_x_coordinate += 70  # Move one lane to the right
                        print("CAR X COORDINATE:", self.car_x_coordinate)
                    elif event.key == pygame.K_UP:
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
                        print("CAR SPEED:", self.car_speed)

            # Ensure the car speed does not go below zero
            self.car_speed = max(0, self.car_speed)
            self.enemy_car_speed = max(0, self.enemy_car_speed)

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.highscore(self.count, self.car_speed, self.distance_covered)
            self.count += 1
            self.distance_covered += self.car_speed * 0.1  # Update distance covered based on speed

            self.timer -= self.clock.tick(60) / 1000  # Update the timer based on the elapsed time

            if self.timer <= 0:
                self.crashed = True
                self.display_message("Time's up!")

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)

            # Increase enemy car frequency and background speed every 10 increments in speed
            if self.car_speed % 10 == 0 and speed_increment_count < self.car_speed // 10:
                speed_increment_count += 1
                self.enemy_car_speed += enemy_car_speed_increment
                self.bg_speed += 1
                self.bg_speed = min(self.bg_speed, self.max_bg_speed)  # Limit background speed
                enemy_car_speed_increment += 1  # Increase the increment for enemy car speed

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        self.initialize()
        self.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count, car_speed, distance_covered):
        font = pygame.font.SysFont("arial", 20)
        text_score = font.render("Score: " + str(count), True, self.white)
        text_speed = font.render("Speed: " + str(car_speed), True, self.white)
        text_distance = font.render("Distance: " + str(int(distance_covered)), True, self.white)
        text_timer = font.render("Time: {:.2f}".format(self.timer), True, self.white)  # Display the remaining time
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
    car_racing.racing_window()
