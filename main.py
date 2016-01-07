from kivgame.pygame import pygame as pg
from kivgame.locals import *
pygame = pg.init()

class Paddle(object):
    def __init__(self, image, screen, pos):
        self.screen = screen
        self.image = image
        self.score = 0
        self.x = pos[0]
        self.y = pos[1]
        self.width = image.get_width()
        self.height = image.get_height()
        self.center_y = self.y + self.height / 2.0

    def bounce_ball(self, ball):
        ball_center = ball.get_center()
        if self.collide(ball_center):
            vx, vy = ball.velocity_x, ball.velocity_y
            offset = (ball_center[1] - self.center_y) / (self.height / 2)
            vel = [-1 * vx * 1.25, vy * 1.1]
            ball.velocity_x, ball.velocity_y = vel[0], vel[1] - offset

    def collide(self, obj):
        if (self.x < obj[0] < self.x + self.width and
            self.y < obj[1] < self.y + self.height):
            return True
        else:
            return False

    def render(self):
        self.screen.blit(self.image, (self.x, self.y))

class PongBall(object):
    def __init__(self, image, screen):
        self.image = image
        self.screen = screen
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity = [self.velocity_x, self.velocity_y]
        self.set_center()

    def set_center(self):
        self.x, self.y = self.pos = [self.screen.get_width() / 2.0 - self.image.get_width() / 2.0,
                                     self.screen.get_height() / 2.0 - self.image.get_height() / 2.0]

    def get_center(self):
        return self.x + self.image.get_width() / 2.0, self.y + self.image.get_height() / 2.0

    def top(self):
        return self.y + self.image.get_height()

    def move(self):
        self.x, self.y = self.pos = self.x + self.velocity_x, self.y + self.velocity_y

    def render(self):
        self.screen.blit(self.image, self.pos)

class PongGame(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 480))
        pygame.display.set_caption('Pong', 'img/icon.png')
        self.mouse = (0, self.screen.get_height() / 2.0)
        self.load_images()
        self.player_1 = Paddle(self.img_paddle, self.screen, (100, 190))
        self.player_2 = Paddle(self.img_paddle, self.screen, (675, 190))
        self.ball = PongBall(self.img_ball, self.screen)
        self.serve_ball()

    def set_mouse(self, spos=(0.5, 0.5)):
        self.mouse = spos[0] * self.screen.get_width(), spos[1] * self.screen.get_height()

    def load_images(self):
        self.img_ball = pygame.image.load("img/ball.png")
        self.img_paddle = pygame.image.load("img/paddle.png")
        self.img_foreground = pygame.image.load("img/foreground.png")
        self.img_background = pygame.image.load("img/background.png")

    def render(self):
        self.screen.clear() #equals:> self.screen.fill((0, 0, 0))
        self.screen.blit(self.img_background, (0, 0))
        self.screen.blit(self.img_foreground, (0, 0))
        self.player_1.render()
        self.player_2.render()
        self.ball.render()

    def serve_ball(self, vel=(6, 8)):
        self.ball.set_center()
        self.ball.velocity_x, self.ball.velocity_y = vel

    def touch_event(self, event):
        try:
            game.set_mouse(event.spos)
            if self.mouse[0] < self.screen.get_width() / 3.0:
                self.player_1.y = self.mouse[1] - self.player_1.image.get_height() / 2.0

            if self.mouse[0] > self.screen.get_width() - self.screen.get_width() / 3.0:
                self.player_2.y = self.mouse[1] - self.player_2.image.get_height() / 2.0
        except:
            pass

    def update(self):
        self.ball.move()

        #bounce of paddles
        self.player_1.bounce_ball(self.ball)
        self.player_2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < 0) or (self.ball.top() > self.screen.get_height()):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < -self.ball.image.get_width():
            self.player_2.score += 1
            self.serve_ball(vel=(4, 6))
        if self.ball.x > self.screen.get_width():
            self.player_1.score += 1
            self.serve_ball(vel=(-4, 6))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            elif event.type == MOUSEBUTTONDOWN:
                self.touch_event(event)

            elif event.type == MOUSEMOTION:
                self.touch_event(event)


game = PongGame()

def loop():
    game.render()
    game.update()

def main():
    pygame.set_loop(loop)
    pygame.run()

if __name__ == "__main__":
    main()