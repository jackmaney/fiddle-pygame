import pygame

pygame.init()

windowSize = (800, 600)

screen = pygame.display.set_mode(windowSize, pygame.DOUBLEBUF, 32)

font = pygame.font.Font(None, 32)

fadeString = "Fade to black..."
returnString = "Fading back..."

fadeText = font.render(fadeString, True, (255, 255, 255), (0, 0, 0))
returnText = font.render(returnString, True, (255, 255, 255), (0, 0, 0))

fadingOut = True
alpha = 256

clock = pygame.time.Clock()

while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    screen.fill((0, 0, 0))

    text = None

    if fadingOut:
        alpha -= 1
        text = fadeText
    else:
        alpha += 1
        text = returnText

    if alpha < 0:
        fadingOut = False
        alpha = 0
    elif alpha > 255:
        fadingOut = True
        alpha = 255

    text.set_alpha(alpha)

    screen.blit(text, (100, 100))

    pygame.display.update()
