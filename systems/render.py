


class RenderSystem:
    @staticmethod
    def render(entity, surface):
        if entity.alive:
            if hasattr(entity, 'image'):
                surface.blit(entity.image, (entity.position.x, entity.position.y))
   