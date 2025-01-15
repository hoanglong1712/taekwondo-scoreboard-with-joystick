import pygame

def get_hat_position(joystick, hat_number):
    """
    Gets the current position of a joystick hat.

    Args:
        joystick (pygame.joystick.Joystick): The joystick object.
        hat_number (int): The index of the hat.

    Returns:
        tuple: A tuple containing the x and y coordinates of the hat position.
               (0, 0): Centered
               (1, 0): Right
               (-1, 0): Left
               (0, 1): Up
               (0, -1): Down
               (1, 1): Up-Right
               (-1, 1): Up-Left
               (1, -1): Down-Right
               (-1, -1): Down-Left
    """
    try:
        hat_position = joystick.get_hat(hat_number)
        return hat_position
    except (pygame.error, IndexError):
        return (0, 0)  # Return (0, 0) if hat is not found or an error occurs

# Example usage:
pygame.init()

joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    hat_number = 0  # Assuming you want to get the position of the first hat
    x, y = get_hat_position(joystick, hat_number)
    print(f"Hat {hat_number} position: ({x}, {y})")
    print(joystick.get_numhats())

pygame.quit()

if (0, -1) == (1, -1):
    print('ok')

    pass