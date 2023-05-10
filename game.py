import pygame
import os
from components.position import PositionComponent
from systems.movement import MovementSystem
from systems.render import RenderSystem
from systems.bullet_system import BulletSystem
from components.bullet import Bullet

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FPS = 120
VEL = 4

class Entity:
    def __init__(self, *components):
        self.components = list(components)

    def get_component(self, component_type):
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None


def draw_window(entities, bullet_system, width, color):
    WIN.fill(WHITE)
    for entity in entities:
        position_component = entity.get_component(PositionComponent)
        if position_component:
            x = position_component.x
            y = position_component.y
            RenderSystem.render(entity, WIN, x, y)  # Pass x and y as arguments

    bullet_system.render_bullets(WIN, color)
    pygame.display.update()


def main():
    yellow = Entity(PositionComponent(100, 300))
    yellow.image = pygame.transform.rotate(
        pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'spaceship_yellow.png')),
            (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        ),
        90
    )
    yellow.position = yellow.get_component(PositionComponent)  # Attach position component to the entity

    movement_system = MovementSystem()
    bullet_system_instance = BulletSystem()

    clock = pygame.time.Clock()
    # Track the state of the space bar
    space_pressed = False
    last_bullet_time = 0  # Initialize the last_bullet_time variable

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    last_bullet_time = 0  # Reset the time elapsed

        # Update the game state
        current_time = pygame.time.get_ticks()
        time_since_last_bullet = current_time - last_bullet_time

        if space_pressed and time_since_last_bullet >= 100:  # Delay of 100 milliseconds (0.1 seconds)
            bullet_system_instance.create_bullet(
                yellow.position.x + SPACESHIP_WIDTH, yellow.position.y + SPACESHIP_HEIGHT // 2, 5
            )
            last_bullet_time = current_time

        keys_pressed = pygame.key.get_pressed()
        movement_system.move(
            yellow, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT
        )
        draw_window([yellow], bullet_system_instance, WIDTH, BLACK)
        bullet_system_instance.update(WIDTH, BLACK, WIN)  # Pass the WIDTH and BLACK values

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

