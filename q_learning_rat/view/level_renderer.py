import pygame

from q_learning_rat.model.level import Level
from q_learning_rat.model.position import Position


class LevelView:
    __BACKGROUND_COLOR = pygame.colordict.THECOLORS['saddlebrown']
    __DEBUG_CELL_COLOR = pygame.colordict.THECOLORS['white']
    __TILE_SIZE = 64

    def __init__(self, debug: bool = False):
        self.__debug = debug
        self.__last_render_time = -1
        self.__surface = None
        self.__font = None
        self.__init_sprites()

    @property
    def font(self) -> pygame.font.Font:
        if self.__font is None:
            self.__font = pygame.font.SysFont('Arial', 12)
        return self.__font

    def __init_sprites(self):
        self.__sprites = {}
        self.__sprites['wall'] = pygame.image.load('sprites/wall.png')
        self.__sprites['cheese'] = pygame.image.load('sprites/cheese.png')
        self.__sprites['hole'] = pygame.image.load('sprites/hole.png')
        self.__sprites['trap'] = pygame.image.load('sprites/trap.png')
        self.__sprites['finish'] = pygame.image.load('sprites/finish.png')
        self.__sprites['rat'] = pygame.image.load('sprites/rat.png')

        for name, sprite in self.__sprites.items():
            self.__sprites[name] = self.__scale_sprite(sprite, self.__TILE_SIZE)

    def __scale_sprite(self, sprite: pygame.Surface, size: int) -> pygame.Surface:
        scale = size/max(sprite.get_size())

        return pygame.transform.smoothscale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
    
    def __draw_debug_cell(self, level: Level, surface: pygame.Surface, position: Position):
        text = self.font.render(f'{position.x}, {position.y}: {level.reward(position)}', True, self.__DEBUG_CELL_COLOR)
        surface.blit(text, (
            (position.x + .5) * self.__TILE_SIZE - text.get_width() / 2, 
            (level.height - position.y - 0.5) * self.__TILE_SIZE - text.get_height() / 2
        ))

    def __draw_sprite(self, level: Level, surface: pygame.Surface, position: Position, sprite_name: str):
        location = (
            (position.x + .5) * self.__TILE_SIZE - self.__sprites[sprite_name].get_width() / 2, 
            (level.height - position.y - 0.5) * self.__TILE_SIZE - self.__sprites[sprite_name].get_height() / 2
        )
        surface.blit(self.__sprites[sprite_name], location)

    def render(self, level: Level) -> pygame.Surface:
        if self.__last_render_time != level.time:
            self.__surface = pygame.Surface((level.width * self.__TILE_SIZE, level.height * self.__TILE_SIZE))
            self.__surface.fill(self.__BACKGROUND_COLOR)
                
            self.__draw_sprite(level, self.__surface, level.rat, 'rat')
            self.__draw_sprite(level, self.__surface, level.finish, 'finish')
            for cheese in level.cheeses:
                self.__draw_sprite(level, self.__surface, cheese, 'cheese')
            for hole in level.holes:
                self.__draw_sprite(level, self.__surface, hole, 'hole')
            for trap in level.traps:
                self.__draw_sprite(level, self.__surface, trap, 'trap')
            for wall in level.walls:
                self.__draw_sprite(level, self.__surface, wall, 'wall')

            if self.__debug:
                for x in range(level.width):
                    for y in range(level.height):
                        position = Position(x, y)
                        self.__draw_debug_cell(level, self.__surface, position)

            self.__last_render_time = level.time

        return self.__surface