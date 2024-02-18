import pygame


# Button class
class Button:
    def __init__(self, position_x, position_y, button_image, image_scale):
        image_width = button_image.get_width()
        image_height = button_image.get_height()
        self.scaled_image = pygame.transform.scale(button_image,
                                                   (int(image_width * image_scale), int(image_height * image_scale)))
        self.button_rect = self.scaled_image.get_rect()
        self.button_rect.topleft = (position_x, position_y)
        self.is_clicked = False

    def draw(self, target_surface):
        is_action_triggered = False
        # Get mouse position
        mouse_position = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.button_rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.is_clicked:
                self.is_clicked = True
                is_action_triggered = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.is_clicked = False

        # Draw button on screen
        target_surface.blit(self.scaled_image, (self.button_rect.x, self.button_rect.y))

        return is_action_triggered
