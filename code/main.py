import os
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import randint, choice

class Game:
    def __init__(self):
        # setup
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('CarnaRun')
        self.clock = pygame.time.Clock()
        self.running = True

        # base path
        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        # audio
        music_path = os.path.join(self.base_path, '..', 'audio', 'music.wav')
        self.music = pygame.mixer.Sound(music_path)
        self.music.set_volume(0.5)
        # self.music.play(loops = -1)

        # setup
        self.setup()

    def setup(self):
        map_path = os.path.join(self.base_path, '..', 'data', 'maps', 'world.tmx')
        map = load_pygame(map_path)

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites), obj.name if hasattr(obj, "name") else "default")
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites, obj.name if hasattr(obj, "name") else "default")

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                # self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            self.all_sprites.update(dt)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()