import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

logo = pygame.image.load("logo.jpg")
logo = pygame.transform.scale(logo, (800, 400))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(logo, (3, 0))

    pygame.display.flip()

pygame.quit()