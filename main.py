import random

import pygame
from pygame.sprite import Group, spritecollide

from game_object import GameObject, AnimatedGameObject, WallObject
from text import Text
from field_map import field


class Player(AnimatedGameObject):
    sprite_filenames = ["PacMan_R1", "PacMan_R2", "PacMan_R3", "PacMan_R4", "PacMan_L1", "PacMan_L2", "PacMan_L3",
                        "PacMan_L4", "PacMan_U1", "PacMan_U2", "PacMan_U3", "PacMan_U4", "PacMan_D1", "PacMan_D2",
                        "PacMan_D3", "PacMan_D4"]
    current_image = "PacMan_R1"


class Wall(WallObject):
    pass

class Meal(GameObject):
    sprite_filename = "SmallDot"

class Boost(GameObject):
    sprite_filename = "BigDot"

'''
class Chest(GameObject):
    sprite_filename = "wall"
    current_image = "wall"
'''

def get_next_img_packman(current_image: str, direction: str) -> str:
    old_direct = current_image[7:]
    if old_direct[0:1] == direction[0:1]:
        step = int(old_direct[1:]) + 1
        if step > 4:
            step = 1
        current_image = current_image[0:8] + str(step)
    else:
        current_image = current_image[0:7] + str(direction[0:1]) + "1"
    return current_image


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
    start_field = field

    walls_coordinates, meal_coordinates, boost_coordinates = [], [], []

    for line_counter, line in enumerate(field):
        for element_counter, element in enumerate(line):
            if element == '*':
                meal_coordinates.extend([(element_counter*30,line_counter*30)])
            elif element in ("q", "w", "a", "s", "|", "-"):
                walls_coordinates.extend([(element, element_counter * 30, line_counter * 30)])
            elif element == 'O':
                boost_coordinates.extend([(element_counter * 30, line_counter * 30)])

    return walls_coordinates, meal_coordinates, boost_coordinates
'''
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2


    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (block_num * wall_block_width, 0),
            (block_num * wall_block_width, screen_height - wall_block_height),
        ])
    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, block_num * wall_block_height),
            (screen_width - wall_block_width, block_num * wall_block_height),
        ])
'''



def compose_context(screen):
    #walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    #walls_coordinates, meal_coordinates, boost_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    walls_coordinates, meal_coordinates, boost_coordinates = calculate_walls_coordinates(1024, 768, 30, 30)
    return {
        #"player": Player(screen.get_width() // 2, screen.get_height() // 2),
        "player": Player(27*30//2,30*30//2),
        "walls": Group(*[Wall(el, x, y) for (el, x, y) in walls_coordinates]),
        "meals": Group(*[Meal(x, y) for (x, y) in meal_coordinates]),
        "boost": Group(*[Boost(x, y) for (x, y) in boost_coordinates]),
        "score": 0,
        #"chest": Chest(100, 100),
    }


def draw_whole_screen(screen, context):
    screen.fill("black")
    context["player"].draw(screen)
    context["meals"].draw(screen)
    context["walls"].draw(screen)
    context["boost"].draw(screen)
    Text(str(context["score"]), (10, 930)).draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((840, 960))
    clock = pygame.time.Clock()
    running = True
    player_speed = 5

    context = compose_context(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        old_player_topleft = context["player"].rect.topleft
        if keys[pygame.K_w]:
            context["player"].rect = context["player"].rect.move(0, -1 * player_speed)
            context["player"].current_image = get_next_img_packman(context["player"].current_image, "Up")
        if keys[pygame.K_s]:
            context["player"].rect = context["player"].rect.move(0, player_speed)
            context["player"].current_image = get_next_img_packman(context["player"].current_image, "Down")
        if keys[pygame.K_a]:
            context["player"].rect = context["player"].rect.move(-1 * player_speed, 0)
            context["player"].current_image = get_next_img_packman(context["player"].current_image, "Left")
        if keys[pygame.K_d]:
            context["player"].rect = context["player"].rect.move(player_speed, 0)
            context["player"].current_image = get_next_img_packman(context["player"].current_image, "Right")

        if spritecollide(context["player"], context["walls"], dokill=False):
            context["player"].rect.topleft = old_player_topleft

        if context["player"].is_collided_with(context["meals"]):
            context["score"] += 10

        if context["player"].is_collided_with(context["boost"]):
            context["score"] += 50


        clock.tick(18) / 1000
    pygame.quit()


if __name__ == '__main__':
    main()
