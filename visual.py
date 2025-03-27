import pygame
from window import Window

if __name__ == "__main__":

    pygame.init()

    WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Z.")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    X = 400
    Y = 400

    circle_center = (WIDTH // 2, HEIGHT // 2)  # Center of screen
    circle_radius = 100
    border = 2
    
    window = Window("aMUSED.py", first_line=50)
    lines = window.get_window_text(line_numbers=True, status_line=True, pre_post_line=False)
    print(lines)
    
    font = pygame.font.Font('freesansbold.ttf', 12)
    text = font.render(lines, True, BLACK, WHITE)
    
    textRect = text.get_rect()
    # set the center of the rectangular object.
    textRect.center = (WIDTH// 2, HEIGHT // 2)

    running = True
    while running:
        screen.fill(WHITE)
        
        screen.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pygame.display.update()

    # Quit Pygame
    pygame.quit()