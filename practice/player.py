from settings import *
from timerthing import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, collision_sprites):
        super().__init__(group)
        # Respawn
        self.spawnpos = pos

        self.image = pygame.Surface((48,56))
        self.image.fill("Green")
        self.rect = self.image.get_frect(topleft = (pos))

        # Physics
        self.direction = vector(0,0)
        self.speed = 300
        self.gravity = 100
        self.jump: bool = False
        self.can_wall_jump: bool = False
        
        # Collisions
        self.collision_sprites = collision_sprites
        self.on_surface = {"floor":False, "left":False, "right":False}
        self.platform = None

        self.old_rect = self.rect.copy()

        # Timers
        self.timers = {"wall_delay":Timer(500),
                       "wall_jump":Timer(250)}
        
        # TEST
        self.display_surf = pygame.display.get_surface()

    def input(self):
        key = pygame.key.get_pressed()

        # Respawn
        if key[pygame.K_r]:
            self.rect.topleft = self.spawnpos

        # Horizontal
        if self.timers["wall_jump"].active == False:
            input_vector = vector()
            if key[pygame.K_RIGHT]:
                input_vector.x += 1
            if key[pygame.K_LEFT]:
                input_vector.x -= 1

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        # Vertical
        if key[pygame.K_SPACE] and any((self.on_surface["floor"], self.on_surface["left"], self.on_surface["right"])):
            self.jump = True
    
    def move(self, dt):
        # Horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collisions("horizontal")

        # Vertical
        if any((self.on_surface["left"], self.on_surface["right"])) and self.timers["wall_delay"].active == False:
            self.direction.y = 120 * dt
            self.rect.y += self.direction.y

        else:
            self.direction.y += self.gravity / 2 * dt 
            self.rect.y += self.direction.y 
            self.direction.y += self.gravity / 2 * dt 

        self.collisions("vertical")

        if self.jump:
            if any((self.on_surface["left"], self.on_surface["right"])) and self.timers["wall_delay"].active == False and self.on_surface["floor"] == False:
                self.timers["wall_jump"].activate()
                
                if self.on_surface["left"]:
                    self.direction.x = 1
                else:
                    self.direction.x = -1
                self.direction.y = -20
            
            else:
                self.timers["wall_delay"].activate()
                self.direction.y = -35
                self.jump = False
                

    def collisions(self, axis):
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.rect):
                    if axis == 'horizontal':
                        if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.rect.right = sprite.rect.left 
                        if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.rect.left = sprite.rect.right
                    else:
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom 
                        self.direction.y = 0
    
    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2))
        
        collidelist = [sprite for sprite in self.collision_sprites]
        
        self.on_surface["floor"] = True if floor_rect.collidelist(collidelist) >= 0 else False
        self.on_surface["left"] = True if left_rect.collidelist(collidelist) >= 0 else False
        self.on_surface["right"] = True if right_rect.collidelist(collidelist) >= 0 else False 

        pygame.draw.rect(self.display_surf, "yellow", floor_rect)
        pygame.draw.rect(self.display_surf, "yellow", left_rect)
        pygame.draw.rect(self.display_surf, "yellow", right_rect)

        self.platform = None
        for sprite in [sprite for sprite in self.collision_sprites.sprites() if hasattr(sprite, "moving")]:
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite

    def platform_movement(self, dt):
        if self.platform:
            self.rect.topleft += self.platform.direction * self.platform.speed * dt

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()    

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_contact()
        self.platform_movement(dt)
        self.update_timers()
        print(self.platform)