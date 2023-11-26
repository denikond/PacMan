import os

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import scale


class GameObject(Sprite):
    sprite_filenames: str | list[str] | None = None
    sprite_extension: str = "png"
    width: int = 40
    height: int = 40
    color_key: tuple[int, int, int] = (245, 245, 245)
    current_image: str | None = None

    def __init__(self, topleft_x: int, topleft_y: int):
        super().__init__()
        print(self.sprite_filenames)
        self.image = {}
        for sprite_filename in self.sprite_filenames:
            sprite_image_full_path = os.path.join("resources", f"{sprite_filename}.{self.sprite_extension}")
            surface = scale(load(sprite_image_full_path), (self.width, self.height))
            surface.set_colorkey(self.color_key)
            self.image[sprite_filename] = surface
        self.rect = self.image[self.sprite_filenames[0]].get_rect()
        self.rect.topleft = topleft_x, topleft_y


    def draw(self, surface: Surface) -> None:
        if self.current_image is None:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image[self.current_image], (self.rect.x, self.rect.y))

    def is_collided_with(self, another_object: "GameObject") -> bool:
        return self.rect.colliderect(another_object.rect)
