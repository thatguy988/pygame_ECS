class RenderSystem:
    @staticmethod
    def render(entity, win, x, y):
        win.blit(entity.image, (x, y))
