import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

CURRENT_SCREEN = "menu"
ON_SOUND = True
HERO_SPEED = 5

HERO_FRAMES = ["hero1", "hero2", "hero3"]
HERO_STOPPED_FRAMES = ["hero1", "hero4"]
ENEMY_FRAMES_COLLISION = ["enemy3", "enemy4"]

INDEX_HERO = 0
COUNTER_ANIMATION = 0
FRAME_STOPPED_INDEX = 0
COLLIDED = False  


HERO = Actor("hero1", (WIDTH // 2, HEIGHT - 100))


ENEMIES = [Actor("enemy1", (random.randint(50, WIDTH - 50), random.randint(-500, -50))) for _ in range(5)]

MENU_BUTTONS = [
    {"rect": Rect((300, 200), (200, 60)), "cor": "green", "texto": "Iniciar Jogo"},
    {"rect": Rect((300, 300), (200, 60)), "cor": "blue", "texto": "Desligar Som"},
    {"rect": Rect((300, 400), (200, 60)), "cor": "red", "texto": "Sair do Jogo"},
]

BACK_BUTTON = {"rect": Rect((20, 20), (150, 50)), "cor": "orange", "texto": "Voltar ao Menu"}


if ON_SOUND:
    music.play("background")
    music.set_volume(0.5)

def reset_game():
    global HERO, ENEMIES, COLLIDED
    HERO.pos = (WIDTH // 2, HEIGHT - 100)
    ENEMIES = [Actor("enemy1", (random.randint(50, WIDTH - 50), random.randint(-500, -50))) for _ in range(5)]
    COLLIDED = False

def play_click_sound():
    if ON_SOUND:
        sounds.click.play()

def draw():
    screen.clear()
    
    if CURRENT_SCREEN == "menu":
        screen.draw.text("Tela Inicial", center=(WIDTH // 2, 100), fontsize=50, color="white")
        for button in MENU_BUTTONS:
            screen.draw.filled_rect(button["rect"], button["cor"])
            screen.draw.text(button["texto"], center=button["rect"].center, fontsize=30, color="white")

    elif CURRENT_SCREEN == "jogo":
        screen.fill("black")
        HERO.draw()
        for enemy in ENEMIES:
            enemy.draw()
        screen.draw.filled_rect(BACK_BUTTON["rect"], BACK_BUTTON["cor"])
        screen.draw.text(BACK_BUTTON["texto"], center=BACK_BUTTON["rect"].center, fontsize=24, color="white")

    elif CURRENT_SCREEN == "gameover":
        screen.fill("darkred")
        screen.draw.text("Game Over", center=(WIDTH // 2, 200), fontsize=60, color="white")
        screen.draw.filled_rect(BACK_BUTTON["rect"], "gray")
        screen.draw.text("Voltar ao Menu", center=BACK_BUTTON["rect"].center, fontsize=30, color="white")

def on_mouse_down(pos):
    global CURRENT_SCREEN, ON_SOUND

    if CURRENT_SCREEN == "menu":
        for button in MENU_BUTTONS:
            if button["rect"].collidepoint(pos):
                play_click_sound()
                if button["texto"] == "Iniciar Jogo":
                    reset_game()
                    CURRENT_SCREEN = "jogo"
                elif button["texto"] == "Desligar Som":
                    ON_SOUND = not ON_SOUND
                    if ON_SOUND:
                        music.play("background")
                    else:
                        music.stop()
                elif button["texto"] == "Sair do Jogo":
                    exit()

    elif CURRENT_SCREEN in ("jogo", "gameover"):
        if BACK_BUTTON["rect"].collidepoint(pos):
            play_click_sound()
            CURRENT_SCREEN = "menu"

def update():
    global INDEX_HERO, COUNTER_ANIMATION, FRAME_STOPPED_INDEX, COLLIDED, CURRENT_SCREEN

    if CURRENT_SCREEN == "jogo":
        moving = False

        if keyboard.left and HERO.x > 0:
            HERO.x -= HERO_SPEED
            moving = True
        if keyboard.right and HERO.x < WIDTH:
            HERO.x += HERO_SPEED
            moving = True
        if keyboard.up and HERO.y > 0:
            HERO.y -= HERO_SPEED
            moving = True
        if keyboard.down and HERO.y < HEIGHT:
            HERO.y += HERO_SPEED
            moving = True

        
        for enemy in ENEMIES:
            enemy.y += 2
            if enemy.y > HEIGHT:
                enemy.x = random.randint(50, WIDTH - 50)
                enemy.y = random.randint(-300, -50)

      
        for enemy in ENEMIES:
            if HERO.colliderect(enemy):
                COLLIDED = True
                CURRENT_SCREEN = "gameover"

       
        COUNTER_ANIMATION += 1
        if COUNTER_ANIMATION % 9 == 0:
        
            if moving:
                INDEX_HERO = (INDEX_HERO + 1) % len(HERO_FRAMES)
                HERO.image = HERO_FRAMES[INDEX_HERO]
            else:
                FRAME_STOPPED_INDEX = (FRAME_STOPPED_INDEX + 1) % len(HERO_STOPPED_FRAMES)
                HERO.image = HERO_STOPPED_FRAMES[FRAME_STOPPED_INDEX]

       
            if COLLIDED:
                for i, enemy in enumerate(ENEMIES):
                    enemy.image = ENEMY_FRAMES_COLLISION[i % len(ENEMY_FRAMES_COLLISION)]

pgzrun.go()
