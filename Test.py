import pygame
from Brick import OBlock

if __name__ == '__main__':
    pygame.init()
    
    screen_width = 350
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True

    #block
    block = OBlock(screen_size=(screen_width, screen_height))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            block.handle_event(event)
        
        screen.fill((255, 255, 255))
        block.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()