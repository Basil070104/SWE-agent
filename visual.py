import pygame

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Z.")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

circle_center = (WIDTH // 2, HEIGHT // 2)  # Center of screen
circle_radius = 100
border = 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, BLACK, circle_center, circle_radius, border)

    pygame.display.flip()

# Quit Pygame
pygame.quit()