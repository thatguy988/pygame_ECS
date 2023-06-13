
from components.explosion import Explosion

class ExplosionSystem:
    def __init__(self):
        self.explosions = []
        
    def create_explosion(self, x, y):
        explosion = Explosion(x, y)
        self.explosions.append(explosion)
    
    def update_explosions(self):
        for explosion in self.explosions:
            explosion.update()

            if explosion.is_finished():
                self.remove_explosion(explosion)

    def remove_explosion(self, explosion):
        if explosion in self.explosions:
            self.explosions.remove(explosion)
    
    def reset(self):
        self.explosions = []  # Clear the list of active explosions
        
        
        


    

    
