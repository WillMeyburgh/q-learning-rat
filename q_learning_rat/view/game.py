from typing import List, Optional, Union
import numpy as np
import pygame

from q_learning_rat.agent.abstract_agent import AbstractAgent
from q_learning_rat.input import Input
from q_learning_rat.model.level import Level
from q_learning_rat.model.move import Move
from q_learning_rat.view.abstract_trainer import AbstractTrainer
from q_learning_rat.view.level_renderer import LevelView


class Game:
    __BACKGROUND_COLOR = pygame.colordict.THECOLORS['sandybrown']

    def __init__(self, trainer: AbstractTrainer, dimensions: np.ndarray = np.array([640, 480]), debug: bool = False):
        self.dimensions = dimensions
        self.running = False
        self.input = Input.get()
        self.trainer = trainer
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
        score = self.font.render(f'Score: {self.level.score:.2f}', True, pygame.colordict.THECOLORS['white'])
        if self.last_score is not None:
            last_score = self.font.render(f'Last score: {self.last_score:.2f}', True, pygame.colordict.THECOLORS['white'])
            new_score = pygame.Surface((max(score.get_width(), last_score.get_width()), score.get_height()+last_score.get_height()+10), pygame.SRCALPHA)
            new_score.blit(score, ((new_score.get_width() - score.get_width())/2, 0))
            new_score.blit(last_score, ((new_score.get_width() - last_score.get_width())/2, self.font.get_height()+10))
            score = new_score
        
        return score

    def draw(self, screen: pygame.Surface):
        screen.fill(self.__BACKGROUND_COLOR)
        surface = self.view.render(self.level)
        surface_dimensions = np.array(surface.get_size())
        score = self.score()
        screen.blit(score, ((self.dimensions[0] - score.get_width())/2, 0))
        screen.blit(surface, (self.dimensions - surface_dimensions) / 2)

    def process(self, delta: float):
        score = self.level.score
        self.level = self.trainer.step()
        if self.level.time == 0:
            self.last_score = score

    def run(self):
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode(self.dimensions.tolist())
        clock = pygame.time.Clock()

        self.running = True

        while self.running:
            events = []

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