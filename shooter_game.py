#Створи власний Шутер!
from pygame import *
from random import randint
mixer.init()
font.init()
mixer.music.load("space.ogg")
#mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
img_back = "galaxy.jpg"
img_hero = "rocket.png"

lost = 0
count = 0

class  GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,  self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_wideth - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            self.fire()
    def fire(self):
        b = Bullet("bullet.png", self.rect.centerx, self.rect.y, 15, 20, 15)
        bullets.add(b)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_wideth - 80)
            self.rect.y = 0
            lost = lost + 1    

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
win_wideth = 700
win_height = 500
display.set_caption("Shooter")
icon_image = image.load("asteroid.png")
display.set_icon(icon_image)



window = display.set_mode((win_wideth, win_height))
background = transform.scale(image.load(img_back), (win_wideth, win_height))
ship = Player(img_hero, 300, win_height - 150, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    rand_v = randint(3, 8)
    rand_y = randint(-300, -50)
    rand_x = randint(0, win_height - 100)
    nlo = Enemy("ufo.png", rand_x, - 100, 80, 50,  rand_v)
    monsters.add(nlo)

finish = False

game = True

font1 = font.SysFont("Impact", 70)
score = 0
score_text = font1.render("Рахунок: 0", True, (255,0,0))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        bullets.update()
        monsters.update()
        
        if sprite.spritecollide(ship, monsters, False):
            finish = True
            lose = font1.render("YOU LOSER!", True, (255,0,0))
            window.blit(lose, (win_wideth/2 - 100, win_height/2 - 50))

        collides = sprite.groupcollide(bullets, monsters, True, True)

        for c in collides:
            score+=1
            score_text = font1.render("Рахунок: 0" + str(score), True, (255,0,0))

        if score >= 5:
            finish = True
            lose = font1.render("YOU WIN!", True, (255,0,0))
            window.blit(lose, (win_wideth/2 - 100, win_height/2 - 50))

        window.blit(score_text,(20, 20))

        monsters.draw(window)
        bullets.draw(window)
        ship.reset()
        display.update()
    time.delay(50)