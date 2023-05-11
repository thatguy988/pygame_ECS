import unittest
import pygame
from components.position import PositionComponent
from systems.movement import MovementSystem
from systems.bullet_system import BulletSystem
from game import Entity, draw_window, WIDTH, HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, WHITE, BLACK, FPS, VEL, main


class MockDisplaySurface:
    def __init__(self, size):
        self.size = size

    def fill(self, color):
        pass

    def blit(self, source, dest):
        pass

    def update(self):
        pass


class GameTestCase(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = MockDisplaySurface((800, 600))
        pygame.display.set_caption("Test Game")

    def tearDown(self):
        pygame.quit()
        if hasattr(self, 'screen') and self.screen:
            self.screen = None

    def test_spaceship_movement(self):
        entity = Entity(PositionComponent(100, 100))
        keys_pressed = [False] * 323
        keys_pressed[pygame.K_w] = True

        movement_system = MovementSystem()
        movement_system.move(entity, keys_pressed, WIDTH, HEIGHT, VEL, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

        position_component = entity.get_component(PositionComponent)
        self.assertEqual(position_component.y, 96)

    def test_bullet_creation(self):
        entity = Entity(PositionComponent(100, 100))

        bullet_system = BulletSystem()
        position_component = entity.get_component(PositionComponent)
        bullet_system.create_bullet(position_component.x, position_component.y, 5)

        self.assertEqual(len(bullet_system.bullets), 1)

        bullet = bullet_system.bullets[0]
        self.assertEqual(bullet.x, position_component.x)
        self.assertEqual(bullet.y, position_component.y)
        self.assertEqual(bullet.velocity, 5)

    def test_game_runs_without_errors(self):
        try:
            draw_window([], BulletSystem(), WIDTH, BLACK, self.screen)  # Pass the mock display Surface
        except Exception as e:
            self.fail(f"The game encountered an error: {str(e)}")


if __name__ == "__main__":
    unittest.main()
