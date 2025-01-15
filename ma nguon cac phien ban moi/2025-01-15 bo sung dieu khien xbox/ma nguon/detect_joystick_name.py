import pygame

pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for device in joysticks:
    device.init()
    print(device.get_name())

pygame.quit()