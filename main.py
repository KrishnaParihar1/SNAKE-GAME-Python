from tkinter import *
import random
import ctypes
from ctypes import wintypes

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3  
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.position = (x, y)
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == food.position[0] and y == food.position[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    # Prevent instant 180° turns
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_direction != opposites.get(direction):
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("consolas", 70),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 80,
        font=("consolas", 30),
        text="Press R to Restart",
        fill="white",
        tag="restart",
    )

    window.bind("r", lambda event: restart_game())


def restart_game():
    global snake, food, score, direction
    canvas.delete(ALL)
    score = 0
    direction = "down"
    label.config(text="Score:{}".format(score))
    snake = Snake()
    food = Food()
    next_turn(snake, food)


def center_window(window, width, height):
    """Centers window inside usable work area (ignores taskbar)"""
    SPI_GETWORKAREA = 0x0030
    work_area = wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0
    )

    work_width = work_area.right - work_area.left
    work_height = work_area.bottom - work_area.top

    x = work_area.left + (work_width // 2) - (width // 2)
    y = work_area.top + (work_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def keep_inside_screen(event):
    """Ensures window stays fully visible inside work area after resize/move"""
    SPI_GETWORKAREA = 0x0030
    work_area = wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0
    )

    x = max(work_area.left, window.winfo_x())
    y = max(work_area.top, window.winfo_y())

    if x + window.winfo_width() > work_area.right:
        x = work_area.right - window.winfo_width()
    if y + window.winfo_height() > work_area.bottom:
        y = work_area.bottom - window.winfo_height()

    window.geometry(f"+{x}+{y}")


# ---------------- MAIN GAME ----------------
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center properly on screen (ignoring taskbar)
center_window(window, window.winfo_width(), window.winfo_height())

# Keep window always inside visible screen
window.bind("<Configure>", keep_inside_screen)

snake = Snake()
food = Food()
next_turn(snake, food)

# Key bindings
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

window.bind("d", lambda event: change_direction("right"))
window.bind("a", lambda event: change_direction("left"))
window.bind("w", lambda event: change_direction("up"))
window.bind("s", lambda event: change_direction("down"))

window.mainloop()
