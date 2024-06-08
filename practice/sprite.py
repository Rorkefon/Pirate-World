from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), group = None):
        super().__init__(group)
        self.image = surf
        self.image.fill("White")
        self.rect = self.image.get_frect(topleft = (pos))
        self.old_rect = self.rect.copy()

class MovingSprite(Sprite):
    def __init__(self, start_pos, end_pos, move_dir, speed, group):
        surf = pygame.Surface((200, 50))
        super().__init__(start_pos, surf, group)
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        self.direction = vector(1,0) if move_dir == 'x' else vector(0,1)
        self.speed = speed
        self.move_dir = move_dir
        self.moving = True
    
    def move(self, dt):
        self.rect.topleft += self.direction * self.speed * dt 
        if self.move_dir == 'x':
            if self.rect.x >= self.end_pos[0]:
                self.direction.x = -1
                self.rect.x = self.end_pos[0]
            if self.rect.x <= self.start_pos[0]:
                self.direction.x = 1
                self.rect.x = self.start_pos[0]
        else:
            if self.rect.y >= self.end_pos[1]:
                self.direction.y = -1 
                self.rect.y = self.end_pos[1]
            if self.rect.y <= self.start_pos[1]:
                self.direction.y = 1
                self.rect.y = self.start_pos[1]
    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)