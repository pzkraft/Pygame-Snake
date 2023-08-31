import pygame
import random
import time
import sys
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('monaco', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20


class SnakeGame:

    def __init__(self, width=640, height=480):
        self.screen_width = width
        self.screen_height = height
        # init display
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.screen_width / 2, self.screen_height / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.screen_width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.screen_height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        if self._is_collision():
            self._game_over()
            return self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.screen_width - BLOCK_SIZE or self.head.x < 0 \
                or self.head.y > self.screen_height - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _game_over(self):
        # finish the game
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, RED)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (320, 15)
        self.display.blit(go_surf, go_rect)
        self._show_score()
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def _show_score(self):
        # show the result
        s_font = pygame.font.SysFont('monaco', 35)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, RED)
        s_rect = s_surf.get_rect()
        s_rect.midtop = (320, 120)
        # рисуем прямоугольник поверх surface
        self.display.blit(s_surf, s_rect)
        print('Final Score', score)

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        score = game.play_step()
