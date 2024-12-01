# Разработай свою игру в этом файле!


from pygame import *




#Класс для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))


        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
   
    #метод для отрисовки героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
       GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
 
       self.x_speed = player_x_speed
       self.y_speed = player_y_speed




    def update(self):
       #по горизонтали
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed <0:
            self.rect.x += self.x_speed
        plaforms_touched = sprite.spritecollide(self, barriers, False)


        if self.x_speed > 0: #идём направо
            for p in plaforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)


        elif self.x_speed < 0: #идём налево
            for p in plaforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)


        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.y_speed < 0:
            self.rect.y += self.y_speed
        plaforms_touched = sprite.spritecollide(self, barriers, False)


        if self.y_speed > 0: #идём вниз
            for p in plaforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)


        elif self.y_speed < 0: #идём вверх
            for p in plaforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)


    def fire(self):
        bullet = Bullet('weapon.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
   
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()


class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
   
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -=self.speed
        else:
            self.rect.x += self.speed




win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Игра Лабиринт')
back = (119, 210, 223)


barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()


wall_1 = GameSprite('platform_h.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
wall_2 = GameSprite('platform_v.png', 370, 100, 50, 400)


barriers.add(wall_1)
barriers.add(wall_2)


packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
kiborg = Enemy('enemy.png', win_width - 80, 180, 80, 80, 5)
kiborg2 = Enemy('enemy.png', win_width - 80, 250, 80, 80, 5)
final_sprite = GameSprite('finalSprite.png', win_width - 85, win_height - 100, 80, 80)


monsters.add(kiborg)
monsters.add(kiborg2)
#переменная-флаг прохождения
finish = False
#переменная-флаг игры
run = True
while run:
    time.delay(50)


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()






        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        window.fill(back)


        packman.update()
        bullets.update()
        barriers.draw(window)
        bullets.draw(window)
        final_sprite.reset()
        packman.reset()


        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)


    #проверка столкновения героя с врагом или финальным спрайтом
    if sprite.spritecollide(packman, monsters, False):
        finish = True


        img = image.load('game-over_1.png')
        d = img.get_width() // img.get_height()
        window.fill((128,128,128))
        window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


    if sprite.collide_rect(packman, final_sprite):
        finish = True
        img = image.load('thumb.jpg')
        window.fill((128,128,128))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))


    display.update()
