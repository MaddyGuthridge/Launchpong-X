# name=Launchpong X
"""
# Launchpong X

An FL Studio script that lets you play Pong on your Launchpad X
"""
import device
from game import Game, PADDLE_WIDTH


MSG_HEADER = [
    0xF0,
    0x00,
    0x20,
    0x29,
    0x02,
    0x0C,
]

INIT_MSG = [0x0E, 0x01, 0xF7]

DEINIT_MSG = [0x0E, 0x00, 0xF7]


LEFT_PADDLES = [0x0B, 0x15, 0x1F, 0x29, 0x33, 0x3D, 0x47, 0x51]

RIGHT_PADDLES = [0x12, 0x1C, 0x26, 0x30, 0x3A, 0x44, 0x4E, 0x58]

LEFT_SCORES = [0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x61, 0x62]

RIGHT_SCORES = [0x13, 0x1D, 0x27, 0x31, 0x3B, 0x45, 0x4F, 0x59]

PLAY_FIELD = [
    list(range(0x0C, 0x12)),
    list(range(0x16, 0x1C)),
    list(range(0x20, 0x26)),
    list(range(0x2A, 0x30)),
    list(range(0x34, 0x3A)),
    list(range(0x3E, 0x44)),
    list(range(0x48, 0x4E)),
    list(range(0x52, 0x58)),
]

COLOR_PADDLE = 0x29
COLOR_BALL = 3
COLOR_WIN = 0x15
COLOR_LOSE = 0x48

LEFT_PRESS = None
RIGHT_PRESS = None


game = Game(8)


def OnInit():
    device.midiOutSysex(bytes(MSG_HEADER + INIT_MSG))


def OnDeInit():
    device.midiOutSysex(bytes(MSG_HEADER + DEINIT_MSG))


def OnMidiIn(event):
    # Yes, I know global variables are bad, I'm being lazy ok
    global LEFT_PRESS, RIGHT_PRESS
    if event.status == 0xA0:
        return
    if event.data1 in LEFT_PADDLES:
        if event.data2 == 0:
            LEFT_PRESS = None
        else:
            LEFT_PRESS = LEFT_PADDLES.index(event.data1)
    elif event.data1 in RIGHT_PADDLES:
        if event.data2 == 0:
            RIGHT_PRESS = None
        else:
            RIGHT_PRESS = RIGHT_PADDLES.index(event.data1)
    elif event.data1 == 0x62 and event.data2 != 0:
        # Reset game on pressing Capture MIDI button
        global game
        game = Game(8)


def OnIdle():
    # Draw the paddles
    left_bottom = game.left_paddle - PADDLE_WIDTH / 2
    left_top = left_bottom + PADDLE_WIDTH
    left_middle_index = int(game.left_paddle * len(LEFT_PADDLES))

    right_bottom = game.right_paddle - PADDLE_WIDTH / 2
    right_top = right_bottom + PADDLE_WIDTH
    right_middle_index = int(game.right_paddle * len(RIGHT_PADDLES))

    for i, x in enumerate(LEFT_PADDLES):
        # If paddle is here
        if left_bottom <= i / len(LEFT_PADDLES) <= left_top:
            color = COLOR_PADDLE
        else:
            if game.left_lose:
                color = COLOR_LOSE
            elif game.left_win:
                color = COLOR_WIN
            else:
                color = 0
        device.midiOutMsg(0x90, 0x0, x, color)

    for i, x in enumerate(RIGHT_PADDLES):
        # If paddle is here
        if right_bottom <= i / len(RIGHT_PADDLES) <= right_top:
            color = COLOR_PADDLE
        else:
            if game.right_lose:
                color = COLOR_LOSE
            elif game.right_win:
                color = COLOR_WIN
            else:
                color = 0
        device.midiOutMsg(0x90, 0x0, x, color)

    # Draw the ball
    ball_x = int(game.ball_pos_x * len(PLAY_FIELD[0]))
    ball_y = int(game.ball_pos_y * len(PLAY_FIELD))
    for i, row in enumerate(PLAY_FIELD):
        for j, x in enumerate(row):

            # If ball is here
            if ball_x == j and ball_y == i:
                device.midiOutMsg(0x90, 0x0, x, 0x3)
            else:
                device.midiOutMsg(0x90, 0x0, x, 0x0)

    # Draw scores
    for i, x in enumerate(LEFT_SCORES):
        if i < game.left_score:
            device.midiOutMsg(0x90, 0x0, x, COLOR_WIN)
        else:
            device.midiOutMsg(0x90, 0x0, x, 0)
    for i, x in enumerate(RIGHT_SCORES):
        if i < game.right_score:
            device.midiOutMsg(0x90, 0x0, x, COLOR_WIN)
        else:
            device.midiOutMsg(0x90, 0x0, x, 0)

    # Calculate movement
    left_offset = 0.0
    right_offset = 0.0

    if LEFT_PRESS is not None:
        if LEFT_PRESS <= left_middle_index:
            left_offset = -0.05
        elif LEFT_PRESS > left_middle_index:
            left_offset = 0.05

    if RIGHT_PRESS is not None:
        if RIGHT_PRESS <= right_middle_index:
            right_offset = -0.05
        elif RIGHT_PRESS > right_middle_index:
            right_offset = 0.05

    game.tick(left_offset, right_offset)
