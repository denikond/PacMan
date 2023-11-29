import os

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import scale


class GameObject(Sprite):
    sprite_filename: str | None = None
    sprite_extension: str = "png"
    width: int = 30
    height: int = 30
    color_key: tuple[int, int, int] = (245, 245, 245)
    current_image: str | None = None

    def __init__(self, topleft_x: int, topleft_y: int):
        super().__init__()
        sprite_image_full_path = os.path.join("resources", f"{self.sprite_filename}.{self.sprite_extension}")
        self.image = scale(load(sprite_image_full_path), (self.width, self.height))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_x, topleft_y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_collided_with(self, another_object: "GameObject") -> bool:
        return self.rect.colliderect(another_object.rect)

class WallObject(Sprite):
    sprite_filenames:dict = {'q': "LeftUp", 'w': "RightUp", 'a': "LeftDown", 's':"RightDown", '-': "Horizontal", '|': 'Vertical'}
    sprite_filename: str | None = None
    sprite_extension: str = "png"
    width: int = 30
    height: int = 30
    color_key: tuple[int, int, int] = (245, 245, 245)
    current_image: str | None = None

    def __init__(self, element: str, topleft_x: int, topleft_y: int):
        super().__init__()
        self.sprite_filename = self.sprite_filenames[element]
        sprite_image_full_path = os.path.join("resources", f"{self.sprite_filename}.{self.sprite_extension}")
        self.image = scale(load(sprite_image_full_path), (self.width, self.height))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_x, topleft_y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))


class AnimatedGameObject(GameObject):
    sprite_filenames: list[str] | None = None

    def __init__(self, topleft_x: int, topleft_y: int):
        super(Sprite).__init__()
        self.image = {}
        for sprite_filename in self.sprite_filenames:
            sprite_image_full_path = os.path.join("resources", f"{sprite_filename}.{self.sprite_extension}")
            surface = scale(load(sprite_image_full_path), (self.width, self.height))
            surface.set_colorkey(self.color_key)
            self.image[sprite_filename] = surface
        self.rect = self.image[self.sprite_filenames[0]].get_rect()
        self.rect.topleft = topleft_x, topleft_y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image[self.current_image], (self.rect.x, self.rect.y))

    def is_collided_with(self, another_object: "Group") -> bool:
        for sprite in another_object.spritedict:
            if self.rect.colliderect(sprite.rect):
                another_object.remove(sprite)
                return True

