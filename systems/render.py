


class RenderSystem:
    @staticmethod
    def render(entity, surface):
        if hasattr(entity, 'image'):
            surface.blit(entity.image, (entity.position.x, entity.position.y))
   