import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jump_sfx = pygame.mixer.Sound("src/Audio/jumpsfx.ogg")
        self.screen = screen
        self.image = pygame.image.load("src/Images/p1_walk04.png").convert_alpha()
        self.left = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midbottom=(150, 300))
        self.gravity = 0
        self.direction = "right"

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom >= 635:
            self.jump_sfx.play()
            self.gravity = -18
        if keys[pygame.K_d]:
            self.rect.x += 5
            self.direction = "right"
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.direction = "left"

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 640: self.rect.bottom = 640
        if self.rect.x >= 730: self.rect.x = 730
        if self.rect.x <= 0: self.rect.x = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        if self.direction == "left":
            self.image = self.left
        else:
            self.image = pygame.transform.flip(self.left, True, False)
        self.screen.blit(self.image, self.rect)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'croc_fly':
            self.croc_fly_surf = pygame.image.load("src/Images/croc-1.png").convert_alpha()
            self.croc_fly_surf = pygame.transform.scale(self.croc_fly_surf, (100, 50))
            self.image = self.croc_fly_surf
            self.rect = self.image.get_rect(bottomright=(randint(900, 1100), 525))
        else:
            self.croc_surf = pygame.image.load("src/Images/croc.png").convert_alpha()
            self.croc_surf = pygame.transform.scale(self.croc_surf, (100, 50))
            self.image = self.croc_surf
            self.rect = self.image.get_rect(bottomright=(randint(900, 1100), 635))

    def update(self):
        self.rect.x -= 15
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 85))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
pygame.display.set_caption("Crocodile Crawler")
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
running = True
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
test_font = pygame.font.Font(r'C:\Users\Isaac\PycharmProjects\Crocodile-Crawler\src\font\Pixeltype.ttf', 50)
game_active = True
start_time = 0
player.add(Player())

game_name = test_font.render('Crocodile Crawler', False, (111,196,196))
game_rect = game_name.get_rect(center=(400, 250))

game_message = test_font.render('Press R to run', False, (111,196,196))
game_message_rect = game_message.get_rect(center=(400, 450))

background_surface = pygame.image.load(r'C:\Users\Isaac\PycharmProjects\Crocodile-Crawler\src\Images\sky.png').convert()
background_surface = pygame.transform.scale(background_surface, (800, 800))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

bg_audio = pygame.mixer.Sound(r"C:\Users\Isaac\PycharmProjects\Crocodile-Crawler\src\Audio\bg_audio.mp3")
bg_audio.play(loops=-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['croc_fly', 'croc', 'croc', 'croc'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        screen.blit(background_surface, (0, 0))
        score = display_score()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
        player.update()
        player.draw(screen)
    else:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_rect)
        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 196))
        score_message_rect = score_message.get_rect(center=(400, 350))
        screen.blit(score_message, score_message_rect)
        screen.blit(game_message, game_message_rect)

    pygame.display.update()
    clock.tick(60)