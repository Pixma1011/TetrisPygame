import pygame

"""
This inherits the Sprite class from pygame which is useful for game objects.
In definition, a brick would be a single square that will build the standard bricks of tetris
"""
class Brick(pygame.sprite.Sprite):
    #constants
    LIGHT_GRAY = (192, 192, 192)

    def __init__(self, color = LIGHT_GRAY, position = (0,0), size = 50, screen_size = (50 * 7, 50 * 18)):
        super().__init__()
        self.__color = color
        self.__position = position
        self.__size = size
        self.__screen_size = screen_size
        self.__image = pygame.Surface([self.size, self.size])        

        self.update(self.color, self.position)

        self.__rect = self.__image.get_rect()

    #for updating the color
    def update(self, color, position):
        self.__image.fill(color)
        pygame.draw.rect(self.__image, color, (position[0], position[1], self.size, self.size), 1)

    #getters and setters
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):
        self.__color = color
        self.update(self.__color, self.position)

    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, position):
        if position[0] >= 0 or position[0] < self.screen_size[0] or position[1] >= 0 or position[1] < self.screen_size[1]:
            self.__position = position
            self.update(self.color, self.__position)
    
    @property
    def size(self):
        return self.__size
    
    #DON'T USE THIS METHOD UNLESS NECESSARY!
    @size.setter
    def size(self, size):
        self.__size = size

    @property
    def screen_size(self):
        return self.__screen_size

    @property
    def image(self):
        return self.__image
    
    @property
    def rect(self):
        return self.__rect


"""
An O block will be used as the base class of all other blocks
"""
class OBlock():
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    PURPLE = (128, 0, 128)
    RED = (255, 0, 0)

    def __init__(self, color = YELLOW, position = (0,0), brick_size = 50, screen_size = (50 * 7, 50 * 18)):
        self.__color = color
        self.__position = position
        self.__brick_size = brick_size     
        self.__screen_size = screen_size

        self.block = self.shape()
        
    #creates the shape of the block
    #must be overriden in other clases
    def shape(self):
        #create bricks that will build the OBlock
        bricks = []
        for index in range(4):
            brick = Brick(self.color, self.position, self.brick_size, self.screen_size)
            bricks.append(brick)
        
        bricks[0].position = self.position
        bricks[1].position = (self.position[0] + self.brick_size, self.position[1])
        bricks[2].position = (self.position[0], self.position[1] + self.brick_size)
        bricks[3].position = (self.position[0] + self.brick_size, self.position[1] + self.brick_size)

        return bricks
    
    def move_shape(self, movement = (0,0)):
        for block in self.block:
            x = block.position[0] + movement[0]
            y = block.position[1] + movement[1]
            
            #exits if size is out of screen
            if x < 0 or x >= self.screen_size[0] or y < 0 or y >= self.screen_size[1]:
                return
            
        for block in self.block:
            x = block.position[0] + movement[0]
            y = block.position[1] + movement[1]    
            
            block.position = (x, y)

    #draws the shape to the screen
    def draw(self, screen):
        for brick in self.block:
            screen.blit(brick.image, brick.position)
    
    #getter and setter
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def position(self):
        return self.__position
    
    #prolly useless
    @position.setter
    def position(self, position):
        self.__position = position

        self.block[0].position = self.position
        self.block[1].position = (self.position[0] + self.brick_size, self.position[1])
        self.block[2].position = (self.position[0], self.position[1] + self.brick_size)
        self.block[3].position = (self.position[0] + self.brick_size, self.position[1] + self.brick_size)

    @property
    def brick_size(self):
        return self.__brick_size
    
    @brick_size.setter
    def brick_size(self, size):
        self.__brick_size = size

    @property
    def screen_size(self):
        return self.__screen_size
   
    

    #movements
    def move_left(self):
        # self.position = (self.position[0] - self.brick_size, self.position[1])
        self.move_shape((-self.brick_size, 0))

    def move_right(self):
        # self.position = (self.position[0] + self.brick_size, self.position[1])
        self.move_shape((self.brick_size, 0))

    def move_down(self):
        # self.position = (self.position[0], self.position[1] - self.brick_size)
        self.move_shape((0, self.brick_size))
            
    #must be overridden by subclasses
    def rotate(self):
        pass


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left arrow key pressed")
                self.move_left()
            elif event.key == pygame.K_RIGHT:
                print("Right arrow key pressed")
                self.move_right()
            elif event.key == pygame.K_UP:
                print("Up arrow key pressed")
                self.rotate()
            elif event.key == pygame.K_DOWN:
                print("Down arrow key pressed")
                self.move_down()
            