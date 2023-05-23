import pygame
from network import Network

width = 794
height = 535
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
background_img = pygame.image.load("track.jpg")
background_img = pygame.transform.scale(background_img, (width, height))

clientNumber = 0


class Player():
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 3

    def draw(self, win):
        win.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect.topleft = (self.x, self.y)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win, player, player2):
    win.blit(background_img, (0, 0))  # Draw the background image at position (0, 0)
    # win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    # p = Player(startPos[0], startPos[1], 50, 100, 'car.png')
    # p2 = Player(0, 0, 50, 100, 'enemy_car_1.png')
    if clientNumber == 0:
        p = Player(startPos[0], startPos[1], 50, 100, 'car.png')
        p2 = Player(0, 0, 50, 100, 'enemy_car_1.png')
    else:
        p = Player(0, 0, 50, 100, 'enemy_car_1.png')
        p2 = Player(startPos[0], startPos[1], 50, 100, 'car.png')

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)


main()
