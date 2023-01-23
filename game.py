"""
game.py

Implementation of Pong
"""
import math
PADDLE_WIDTH = 3/8
PADDLE_LENIENCY = 1/8
PADDLE_ANGLE_CHANGE = 0.3 * math.pi
VELOCITY_INCREASE = 0.005
VELOCITY_START = 0.02
COUNTDOWN_LEN = 50


def clamp(val: float) -> float:
    if val < 0:
        return 0.0
    elif val > 1:
        return 1.0
    else:
        return val


class Game:
    def __init__(self, max_score: int) -> None:
        self.max_score = max_score
        self.countdown = COUNTDOWN_LEN
        self.left_win = True
        self.right_win = True
        self.left_lose = False
        self.right_lose = False
        self.left_score = 0
        self.right_score = 0
        self.ball_pos_x = 0.5
        self.ball_pos_y = 0.5
        self.ball_velocity = VELOCITY_START
        self.ball_angle = 0.0
        self.left_paddle = 0.5
        self.right_paddle = 0.5

    def tick(self, left_paddle_offset: float, right_paddle_offset: float):

        # Move paddles
        self.left_paddle = clamp(self.left_paddle + left_paddle_offset)
        self.right_paddle = clamp(self.right_paddle + right_paddle_offset)

        # Handle countdown
        if self.countdown != 0:
            self.countdown -= 1
            if self.countdown == 0:
                self.left_win = False
                self.right_win = False
            return

        # Move ball
        self.ball_pos_x += self.ball_velocity * math.cos(self.ball_angle)
        self.ball_pos_y += self.ball_velocity * math.sin(self.ball_angle)

        # Bounce off top and bottom edges
        if self.ball_pos_y <= 0 or self.ball_pos_y >= 1:
            self.ball_angle *= -1

        # Detect paddle collisions
        # Left
        if (
            self.ball_pos_x < 0.1
            and abs(self.ball_pos_y - self.left_paddle + PADDLE_LENIENCY)
            < PADDLE_WIDTH / 2
        ):
            self.ball_angle = \
                PADDLE_ANGLE_CHANGE * (self.ball_pos_y - self.left_paddle) \
                / PADDLE_WIDTH
            self.ball_pos_x = 0.1
            self.ball_velocity += VELOCITY_INCREASE
        # Right
        if (
            0.9 < self.ball_pos_x
            and abs(self.ball_pos_y - self.right_paddle + PADDLE_LENIENCY)
            < PADDLE_WIDTH / 2
        ):
            self.ball_angle = math.pi\
                - PADDLE_ANGLE_CHANGE * (self.ball_pos_y - self.right_paddle) \
                / PADDLE_WIDTH
            self.ball_pos_x = 0.9
            self.ball_velocity += VELOCITY_INCREASE

        # Detect left and right edge collisions
        # Left
        if self.ball_pos_x < 0:
            self.right_score += 1
            self.ball_velocity = VELOCITY_START
            self.ball_angle = 0
            self.ball_pos_x = 0.5
            self.right_win = True
            self.countdown = COUNTDOWN_LEN
            if self.right_score == self.max_score:
                self.left_lose = True
                self.countdown = -1
        # Right
        elif self.ball_pos_x > 1:
            self.left_score += 1
            self.ball_velocity = VELOCITY_START
            self.ball_angle = math.pi
            self.ball_pos_x = 0.5
            self.left_win = True
            self.countdown = COUNTDOWN_LEN
            if self.left_score == self.max_score:
                self.right_lose = True
                self.countdown = -1
