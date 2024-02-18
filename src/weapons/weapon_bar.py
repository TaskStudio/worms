import pygame


class WeaponBar:
    def __init__(self, position, weapon_image_paths, weapon_identifiers):
        self.position = position
        self.weapon_images = [pygame.image.load(path).convert_alpha() for path in weapon_image_paths]
        self.weapon_identifiers = weapon_identifiers
        self.selected_weapon_index = 0

    def draw(self, screen):
        total_width = sum(image.get_width() + 20 for image in self.weapon_images)  # Assuming 20 pixels padding
        start_x = self.position[0] - total_width // 2

        for index, image in enumerate(self.weapon_images):
            image_pos_x = start_x + (20 if index > 0 else 0)  # Adjust for padding
            screen.blit(image, (image_pos_x, self.position[1]))

            # Draw index under the image
            font = pygame.font.Font(None, 24)
            # Highlight the index if it is the selected weapon
            if index == self.selected_weapon_index:
                index_color = (255, 0, 0)  # Highlight color, e.g., yellow
            else:
                index_color = (0, 0, 0)  # Normal color, e.g., white
            index_surface = font.render(str(index + 1), True, index_color)
            index_pos_x = image_pos_x + (image.get_width() / 2) - (index_surface.get_width() / 2)
            index_pos_y = self.position[1] + image.get_height() + 5  # 5 pixels gap
            screen.blit(index_surface, (index_pos_x, index_pos_y))

            start_x += image.get_width() + 20  # Move to the right for the next image

    def get_selected_weapon(self):
        return self.weapon_identifiers[self.selected_weapon_index]
