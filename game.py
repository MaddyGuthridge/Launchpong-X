"""
game.py

Implementation of Pong
"""
import math
PADDLE_WIDTH = 3/8
PADDLE_ANGLE_CHANGE = 0.3 * math.pi
VELOCITY_INCREASE = 0.01


def clamp(val: float) -> float:
    if val < 0:
        return 0.0
    elif val > 1:
        return 1.0
    else:
        return val


class Game:
    def __init__(self) -> None:
        self.left_score = 0
        self.right_score = 0
        self.ball_pos_x = 0.5
        self.ball_pos_y = 0.5
        self.ball_velocity = 0.02
        self.ball_angle = 0.0
        self.left_paddle = 0.5
        self.right_paddle = 0.5

    def tick(self, left_paddle_offset: float, right_paddle_offset: float):
        # Move paddles
        self.left_paddle = clamp(self.left_paddle + left_paddle_offset)
        self.right_paddle = clamp(self.right_paddle + right_paddle_offset)

        # Move ball
        self.ball_pos_x += self.ball_velocity * math.cos(self.ball_angle)
        self.ball_pos_y += self.ball_velocity * math.sin(self.ball_angle)

        # Bounce off top and bottom edges
        if self.ball_pos_y == 0 or self.ball_pos_y == 1:
            self.ball_angle *= -1

        # Detect paddle collisions
        # Left
        if (
            0.05 < self.ball_pos_x < 0.1
            and abs(self.ball_pos_y - self.left_paddle) < PADDLE_WIDTH / 2
        ):
            self.ball_angle = \
                PADDLE_ANGLE_CHANGE * (self.ball_pos_y - self.left_paddle) \
                / PADDLE_WIDTH
            self.ball_pos_x = 0.1
        # Right
        if (
            0.9 < self.ball_pos_x < 0.95
            and abs(self.ball_pos_y - self.right_paddle) < PADDLE_WIDTH / 2
        ):
            self.ball_angle = math.pi\
                - PADDLE_ANGLE_CHANGE * (self.ball_pos_y - self.right_paddle) \
                / PADDLE_WIDTH
            self.ball_pos_x = 0.9

        # Detect left and right edge collisions
        # Left
        if self.ball_pos_x < 0:
            if abs(self.ball_pos_y - self.left_paddle) < PADDLE_WIDTH / 2:
                # Paddle
                self.ball_angle = PADDLE_ANGLE_CHANGE \
                    * (self.ball_pos_y - self.left_paddle) \
                    / PADDLE_WIDTH
            else:
                # Win
                self.right_score += 1
                self.ball_velocity = 0.1
                self.ball_angle = 0
            self.ball_pos_x = 0.0
        # Right
        elif self.ball_pos_x > 1:
            if abs(self.ball_pos_y - self.right_paddle) < PADDLE_WIDTH / 2:
                # Paddle
                self.ball_angle = math.pi - PADDLE_ANGLE_CHANGE \
                    * (self.ball_pos_y - self.right_paddle) \
                    / PADDLE_WIDTH
            else:
                self.left_score += 1
                self.ball_velocity = 0.1
                self.ball_angle = math.pi
            self.ball_pos_x = 1.0
