# Works just like SwinGame input system, but init() needs to be called
# to initialise everything.
#
# Consists of three main functions:
# key_down -> If the key is currently pressed
# key_typed -> If the key was pressed this frame
# key_released -> If the key was released this frame
#
# Mouse positions are fetched with mouse_x() and mouse_y()
#
# process_events() is exactly like SwinGame ProcessEvents() and needs
# to be called each frame.

import pygame
from enum import Enum


class KeyState(Enum):
    Down = 1        # Key is currently pressed
    Typed = 2       # Key was pressed this frame
    Released = 3    # Key was released this frame

# Pygame integer representations of mouse buttons
__LEFT_MOUSE = 1
__RIGHT_MOUSE = 3

# Mouse values. Clicked is registered when the button is released
left_mouse_clicked = False
left_mouse_down = False
right_mouse_clicked = False
right_mouse_down = False

# Key values
tracked_keys = {}


# Initialises variables and specifies which keys will be tracked for input
def init():
    add_key(pygame.K_w)
    add_key(pygame.K_s)
    add_key(pygame.K_a)
    add_key(pygame.K_d)
    add_key(pygame.K_c)
    add_key(pygame.K_r)
    add_key(pygame.K_q)
    add_key(pygame.K_e)
    add_key(pygame.K_g)
    add_key(pygame.K_t)


# Adds a new key to be tracked for input
def add_key(key):
    tracked_keys[key] = {}
    tracked_keys[key][KeyState.Down] = False
    tracked_keys[key][KeyState.Typed] = False
    tracked_keys[key][KeyState.Released] = False


# Specifies if a key is currently pressed
def key_down(key):
    return tracked_keys[key][KeyState.Down]


# Specifies if a key has been pressed this frame
def key_typed(key):
    return tracked_keys[key][KeyState.Typed]


# Specifies if a key has been released this frame
def key_released(key):
    return tracked_keys[key][KeyState.Released]


# Returns the x position of the mouse
def mouse_x():
    return pygame.mouse.get_pos()[0]


# Returns the y position of the mouse
def mouse_y():
    return pygame.mouse.get_pos()[1]


# Updates all key and mouse states
def process_events():
    global left_mouse_clicked
    global left_mouse_down

    global right_mouse_clicked
    global right_mouse_down

    left_mouse_clicked = False
    right_mouse_clicked = False

    # Typed and released states set to false at start of each frame
    for key in tracked_keys:
        tracked_keys[key][KeyState.Typed] = False
        tracked_keys[key][KeyState.Released] = False

    # Process each event and map key / mouse states
    for event in pygame.event.get():
        # Key Down event
        if event.type == pygame.KEYDOWN:
            if event.key in tracked_keys:
                tracked_keys[event.key][KeyState.Down] = True
                tracked_keys[event.key][KeyState.Typed] = True
        # Key Up event
        elif event.type == pygame.KEYUP:
            if event.key in tracked_keys:
                tracked_keys[event.key][KeyState.Down] = False
                tracked_keys[event.key][KeyState.Released] = True
        # Mouse Button Down event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == __LEFT_MOUSE:
                left_mouse_down = True
            elif event.button == __RIGHT_MOUSE:
                right_mouse_down = True
        # Mouse Button Up event
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == __LEFT_MOUSE:
                left_mouse_clicked = True
                left_mouse_down = False
            elif event.button == __RIGHT_MOUSE:
                right_mouse_clicked = True
                right_mouse_down = False
        # Quit event
        elif event.type == pygame.QUIT:
            pygame.quit()