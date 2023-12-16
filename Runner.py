import pygame
import sys
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.is_falling = True
        self.fall_speed = 5  # Adjust the fall speed
        self.image = self.player_jump  # Initially set to jump image
        self.rect = self.image.get_rect(midbottom=(80, -100))  # Start above the screen

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.is_falling = False
            self.jump_sound.play()

    def apply_gravity(self):
        if not self.is_falling:
            self.rect.y += self.gravity
            self.gravity += 1
            if self.rect.bottom >= 300:
                self.is_falling = False
                self.rect.bottom = 300
        else:
            if self.rect.bottom < 300:  # Check if the player is still in the air
                self.rect.y += self.fall_speed
            else:
                self.is_falling = False
                self.rect.bottom = 300


    def animation_state(self):
        if not self.is_falling:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/Fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha() #it will remove the alpha values
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
                self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite():
    global game_active
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()

        player.sprite.is_falling = True
        player.sprite.rect = player.sprite.image.get_rect(midbottom=(80, -100))
        return False
    else:
        return True
    
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(loops = -1)
bg_music.set_volume(0.1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("graphics/sky.png").convert() #pygame will work with the images more easily
sky_x = 0
ground_surface = pygame.image.load("graphics/ground.png").convert()

#Intro screen
game_name = test_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_message = test_font.render("Press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit('Game Closed')

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                sky_x = 0
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        sky_x -= 1
        if sky_x < -800:
            sky_x = 0
        screen.blit(sky_surface, (sky_x,0))
        screen.blit(sky_surface, (sky_x + 800,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #Collisions
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        
        score_message = test_font.render(f"Your score: {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0:    
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60) #Frame rate