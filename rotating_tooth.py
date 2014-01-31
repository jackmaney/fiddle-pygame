import pygame
import sys



class SlantedRect(pygame.sprite.Sprite):
    def __init__(self, angle=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"Mo'Larr.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = [100, 200]
        self.angle = angle
        self.num_rotations = 0
        self.pauseTime = 50
        self.timer = 0
        self.original = self.image.copy()

        self.rotation_center = [500, 600]

    def update(self, time):

        #self.rect.center = pygame.mouse.get_pos()
        delta = time - self.timer

        if delta > self.pauseTime:
            # rot_image = pygame.transform.rotate(self.image, self.angle).copy()
            # rot_rect = rot_image.get_rect().copy()
            #
            # rot_rect.center = self.rect.center
            # self.rect = rot_rect.copy()
            # self.image = rot_image.copy()

            self.num_rotations += 1
            center = self.rect.center

            self.image = pygame.transform.rotate(self.original, self.angle * self.num_rotations)
            self.rect = self.image.get_rect(center=center)
            self.timer = time

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


def main():

    pygame.init()

    pygame.mouse.set_visible(False)

    windowSize = (1024, 768)

    screen = pygame.display.set_mode(windowSize)

    clock = pygame.time.Clock()

    rect = SlantedRect()

    group = pygame.sprite.Group(rect)

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        screen.fill((0, 0, 0))

        group.clear(screen, background)
        group.update(pygame.time.get_ticks())
        group.draw(screen)

        #print rect.rect.size
        print clock.get_fps()

        pygame.display.update()

if __name__ == '__main__':
    main()