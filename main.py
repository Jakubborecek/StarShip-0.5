import pygame
import os
import random

pygame.font.init()
SIRKA, VYSKA = 1000, 1000
PLOCHA = pygame.display.set_mode((SIRKA, VYSKA))
pozadie = pygame.transform.scale(pygame.image.load(os.path.join("pictures", "pozadie.png")), (SIRKA, VYSKA))
zelena_lod = pygame.image.load(os.path.join("pictures", "zelena_lod.png"))
zlta_lod = pygame.image.load(os.path.join("pictures", "zlta_lod.png"))
laser_zlty = pygame.image.load(os.path.join("pictures", "laser_zlty.png"))


class Lod:
    COOLDOWN = 25

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lod_obr = None
        self.laser_obr = None
        self.lasery = []
        self.cool_down_pocitadlo = 0

    def zobrazit(self, okno):
        okno.blit(self.lod_obr, (self.x, self.y))
        for laser in self.lasery:
            laser.zobrazit(okno)

    def pohyb_laserov(self):
        self.cooldown()

    def strielat(self):
        if self.cool_down_pocitadlo == 0:
            laser = Laser(self.x, self.y, self.laser_obr)
            self.lasery.append(laser)
            self.cool_down_pocitadlo = 1

    def cooldown(self):
        if self.cool_down_pocitadlo >= self.COOLDOWN:
            self.cool_down_pocitadlo = 0
        elif self.cool_down_pocitadlo > 0:
            self.cool_down_pocitadlo += 1

    def get_height(self):
        return self.lod_obr.get_height()

    def get_width(self):
        return self.lod_obr.get_width()


class Hrac(Lod):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.lod_obr = zlta_lod
        self.laser_obr = laser_zlty
        self.mask = pygame.mask.from_surface(self.lod_obr)

    def zobrazit(self, okno):
        super().zobrazit(
            okno)

    def pohyb_laserov(self, rychlost, objekty):
        self.cooldown()
        for laser in self.lasery:
            laser.pohyb(rychlost)
            for obj in objekty:
                if laser.kolizia(obj):
                    objekty.remove(obj)


class Nepriatel(Lod):
    ZADELENIE = {
        'zelena': zelena_lod
    }

    def __init__(self, x, y, farba):
        super().__init__(x, y)
        self.lod_obr = self.ZADELENIE[farba]
        self.mask = pygame.mask.from_surface(self.lod_obr)

    def pohyb(self, rychlost):
        self.y += rychlost


class Laser:
    def __init__(self, x, y, obr):
        self.x = x
        self.y = y
        self.obr = obr
        self.mask = pygame.mask.from_surface(self.obr)

    def zobrazit(self, okno):
        okno.blit(self.obr, (self.x, self.y))

    def pohyb(self, rychlost):
        self.y += rychlost

    def kolizia(self, obj):
        return zrazenie(self, obj)


def zrazenie(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def zaklad():
    spustit = True
    FPS = 60
    zivoty = 10
    hlavne_pismo = pygame.font.SysFont('Verdana', 30)
    nepriatelia = []
    pocet_nepriatelov = 10
    rychlost_hraca = 6
    rychlost_laseru = 9
    rychlost_nepriatela = 1
    pocitadlo_znicenia = 0
    hrac = Hrac(450, 850)
    clock = pygame.time.Clock()
    zniceny = False

    def prekresli_okno():
        PLOCHA.blit(pozadie, (0, 0))
        zobraz_zivoty = hlavne_pismo.render(f"Zivoty: {zivoty}", 1, (255, 255, 255))
        PLOCHA.blit(zobraz_zivoty, (10, 10))
        for nepriatel in nepriatelia:
            nepriatel.zobrazit(PLOCHA)
        hrac.zobrazit(PLOCHA)
        pygame.display.update()

    while spustit:
        clock.tick(FPS)
        prekresli_okno()
        if zivoty <= 0:
            zniceny = True
            pocitadlo_znicenia += 1
        if zniceny:
            if pocitadlo_znicenia > 120:
                spustit = False
            else:
                continue

        klavesy = pygame.key.get_pressed()
        if klavesy[pygame.K_a] and hrac.x - rychlost_hraca > 0:
            hrac.x -= rychlost_hraca
        if klavesy[pygame.K_d] and hrac.x + rychlost_hraca > 0:
            hrac.x += rychlost_hraca
        if klavesy[pygame.K_SPACE]:
            hrac.strielat()

        if len(nepriatelia) == 0:
            pocet_nepriatelov += 5
            for i in range(pocet_nepriatelov):
                nepriatel = Nepriatel(random.randrange(50, SIRKA - 100), random.randrange(-1600, -100),
                                      random.choice(['zelena']))
                nepriatelia.append(nepriatel)

        for nepriatel in nepriatelia[:]:
            nepriatel.pohyb(rychlost_nepriatela)
            if nepriatel.y + nepriatel.get_height() > VYSKA:
                zivoty -= 1
                nepriatelia.remove(nepriatel)
        hrac.pohyb_laserov(-rychlost_laseru, nepriatelia)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


def hlavne_menu():
    spustit = True
    while spustit:
        PLOCHA.blit(pozadie, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spustit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                zaklad()
    pygame.quit()


hlavne_menu()