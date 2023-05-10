import pygame
from components.position import PositionComponent


class RenderSystem:
    @staticmethod
    def render(entity, surface, x, y):
        position_component = entity.get_component(PositionComponent)
        if position_component and hasattr(entity, 'image'):
            surface.blit(entity.image, (x, y))
