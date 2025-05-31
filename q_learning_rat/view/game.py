from typing import List, Optional, Union
import numpy as np
import pygame

from q_learning_rat.agent.abstract_agent import AbstractAgent
from q_learning_rat.input import Input
from q_learning_rat.model.level import Level
from q_learning_rat.model.move import Move
from q_learning_rat.view.basic_trainer import BasicTrainer
from q_learning_rat.view.level_renderer import LevelView


class Game:
    __BACKGROUND_COLOR = pygame.colordict.THECOLORS['sandybrown']

    def __init__(self, trainer: BasicTrainer, debug: bool = False):
        self.dimensions = None
        self.running = False
        self.input = Input.get()
        self.trainer = trainer
        self.previous_level = None
        self.level = self.trainer.level
        self.debug = debug
        self.view = LevelView(self.debug)
        self.__font = None
        self.last_score = None

    @property
    def font(self) -> pygame.font.Font:
        if self.__font is None:
            self.__font = pygame.font.SysFont('Arial', 24)
        return self.__font

    def score(self) -> pygame.Surface:
        score_surface = self.font.render(f'Score: {self.level.score:.2f}', True, pygame.colordict.THECOLORS['white'])
        agent_name_surface = self.font.render(f'Agent: {self.trainer.agent.name()}', True, pygame.colordict.THECOLORS['white'])

        surfaces = [score_surface]
        if self.last_score is not None:
            last_score_surface = self.font.render(f'Last score: {self.last_score:.2f}', True, pygame.colordict.THECOLORS['white'])
            surfaces.append(last_score_surface)
        surfaces.append(agent_name_surface)

        max_width = max(s.get_width() for s in surfaces)
        total_height = sum(s.get_height() for s in surfaces) + (len(surfaces) - 1) * 10 # 10 is padding between lines

        new_score_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        
        y_offset = 0
        for s in surfaces:
            new_score_surface.blit(s, ((new_score_surface.get_width() - s.get_width())/2, y_offset))
            y_offset += s.get_height() + 10
        
        return new_score_surface

    def draw(self, screen: pygame.Surface):
        screen.fill(self.__BACKGROUND_COLOR)
        surface = self.view.render(self.level)
        surface_dimensions = np.array(surface.get_size())
        score = self.score()
        screen.blit(score, ((self.dimensions[0] - score.get_width())/2, 0))
        surface_position = (self.dimensions - surface_dimensions) / 2
        surface_position[1] = max(surface_position[1], score.get_height()+10)
        screen.blit(surface, surface_position)

    def process(self, delta: float):
        score = self.level.score
        self.level = self.trainer.step()
        if self.level.time == 0:
            self.last_score = score

    def run(self):
        pygame.init()
        pygame.font.init()

        clock = pygame.time.Clock()

        self.running = True

        screen = pygame.display.set_mode((600, 400))

        while self.running:
            events = []

            if self.previous_level is None or self.level.id != self.previous_level.id:
                cell_size = 64
                w_padding = 100
                h_padding = 150
                width = self.level.width * cell_size + w_padding
                height = self.level.height * cell_size + h_padding
                self.dimensions = np.array([width, height])
                screen = pygame.display.set_mode(self.dimensions.tolist())
                self.previous_level = self.level

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    events.append(event)

            self.draw(screen)
            pygame.display.flip()

            self.input.process(events)

            delta = clock.tick(60)/1000
            self.process(delta)

        pygame.quit()
