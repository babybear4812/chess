# Handling user input and displaying the board (state of the game, i.e. State class)
import pygame as pg
import engine

WIDTH = HEIGHT = 400
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15  # for animations only
IMAGES = {}


def import_images():
    pieces = ["wR", "wKn", "wB", "wQ", "wK",
              "wP", "bR", "bKn", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
