"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

import pygame, sys

class Base(object): 
    def __init__(self, screenSize=[512, 512], fullScreen=False):
        """Initializes all pygame and openGL stuff."""
        
        # Initialize all pygame modules
        pygame.init()
        
        # Indicate rendering details
        displayFlags = pygame.DOUBLEBUF | pygame.OPENGL        
        
        if fullScreen:
            screenSize = [pygame.display.Info().current_w,
                          pygame.display.Info().current_h]
            displayFlags = displayFlags | pygame.FULLSCREEN
            
        self.aspectRatio = screenSize[0] / screenSize[1]
        
        # Initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(
            pygame.GL_MULTISAMPLEBUFFERS,
            1)
        pygame.display.gl_set_attribute(
            pygame.GL_MULTISAMPLESAMPLES,
            4)
        
        # Use a core OpenGL profile for cross-platform compatibility 
        pygame.display.gl_set_attribute(
           pygame.GL_CONTEXT_PROFILE_MASK,
           pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 16)
        
        # Create and display the window
        self.screen = pygame.display.set_mode(screenSize,
                                              displayFlags)
        
        # Set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")
        
        # Determine if main loop is active
        self.RUNNING = True
        
        # Manage time-related data and operations
        self.clock = pygame.time.Clock()        
        self.time = 0
        self.deltaTime = 0
        
    def initialize(self):
        """For inheriting classes to initialize their OpenGL scene."""
        pass
    
    def update(self):
        """For inherting classes to update their OpenGL scene."""
        pass
    
    def run(self):
        """The main running loop of the program."""
        
        self.initialize()
        while self.RUNNING:
            self.RUNNING = not self.handleInput()
            
            # Seconds since iteration of run loop, increase
            # total time of program.
            self.deltaTime = self.clock.get_time() / 1000            
            self.time += self.deltaTime
            
            self.update()
            
            # Display image on screen
            pygame.display.flip()
            
            # Pause if necessary to achieve 60 FPS
            self.clock.tick(60)
            
        ## shutdown ##
        pygame.quit()
        sys.exit()
    
    
    def handleExitInput(self, event):
        """For exiting the program."""
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return False

    def handleOtherInput(self, event):
        """For handling other inputs, override for new behaviors"""
        pass

    def handleInput(self):
        """Checks the event queue."""
        for event in pygame.event.get():
            exitRender = self.handleExitInput(event)
            if exitRender:
                return True

            self.handleOtherInput(event)
        
        return False
