import pyxel as px
import numpy as np

# Direction
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

# True to remove the wall
RUN_THROUGH = False

# Axis
X_AXIS = 0
Y_AXIS = 1

# Color setting
COL_BG = 0
COL_SNAKE = 3
COL_TEXT = 1
COL_CANDY = 8


class App:
    def __init__(self):
        px.init(70, 50, caption="Snake senzia!")
        self.declare()
        px.run(self.update, self.draw)

    def declare(self):
        self.dead = True
        self.start = False
        self.direction = RIGHT
        self.candy = np.arange(2).reshape(1, 2)
        self.snake = np.array([
            [0, 0],
            [1, 0],
            [2, 0],
            [3, 0]
        ])
        self.generate_candy()

    def generate_candy(self):
        while(True):
            x = np.random.randint(px.width)
            y = np.random.randint(px.height)
            self.candy = np.array([x, y])
            if self.candy not in self.snake:
                break

    def check_dead(self):
        if len(np.unique(self.snake, axis=0)) < len(self.snake):
            self.dead = True
        if not RUN_THROUGH:
            head = (np.array(self.snake[-1]) + self.direction).reshape(1, 2)
            if head[0][0] < 0 or head[0][1] < 0 or head[0][0] > px.width or head[0][1] > px.height:
                self.dead = True

    def change_screen(self):
        if px.btn(px.KEY_R) and self.start:
            self.declare()
            self.start = False
        if not self.start and px.btn(px.KEY_SPACE):
            self.dead = False
            self.start = True

    def update_direction(self):
        if (px.btn(px.KEY_RIGHT) or px.btn(px.KEY_D)) and self.direction != LEFT:
            self.direction = RIGHT
        elif (px.btn(px.KEY_LEFT) or px.btn(px.KEY_A)) and self.direction != RIGHT:
            self.direction = LEFT
        elif (px.btn(px.KEY_UP) or px.btn(px.KEY_W)) and self.direction != DOWN:
            self.direction = UP
        elif (px.btn(px.KEY_DOWN) or px.btn(px.KEY_S)) and self.direction != UP:
            self.direction = DOWN

    def update_candy(self):
        head = self.snake[-1]
        tail = self.snake[0].reshape(1, 2)
        tail_sub = self.snake[1]
        if (head == self.candy).all():
            tail_direction = tail - tail_sub
            tail = np.append(tail + tail_direction, tail, axis=X_AXIS)
            self.snake = np.append(tail, self.snake[1:], axis=X_AXIS)
            self.generate_candy()

    def update_snake(self):
        head = (np.array(self.snake[-1]) + self.direction).reshape(1, 2)
        if RUN_THROUGH:
            head[0][0] %= px.width
            head[0][1] %= px.height
        if not self.dead:
            self.snake = np.append(
                self.snake[1:len(self.snake)], head, axis=X_AXIS)

    def update(self):
        if not self.dead:
            self.update_candy()
            self.update_direction()
            self.update_snake()
            self.check_dead()
        else:
            self.change_screen()

    def draw_snake(self):
        for each in self.snake:
            px.pset(each[0], each[1], COL_SNAKE)

    def draw_candy(self):
        px.pset(self.candy[0], self.candy[1], COL_CANDY)

    def draw_text(self):
        if self.dead and self.start:
            px.text(1, px.height * 1 / 5,
                    f"{(len(self.snake)-4)*100} points", COL_TEXT)
            px.text(1, px.height * 3 / 5, "Press R to restart", COL_TEXT)
        elif self.dead and not self.start:
            px.text(1, px.height * 1 / 2, "Press Space to start", COL_TEXT)

    def draw(self):
        px.cls(COL_BG)
        self.draw_snake()
        self.draw_candy()
        self.draw_text()


App()
