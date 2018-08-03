import pygame
import math

# utility functions

def angle_to_coord(origin, dest):
    delta_x = dest[0] - origin[0]
    delta_y = origin[1] - dest[1]
    theta_radians = math.atan2(delta_y, delta_x)
    theta_degrees = theta_radians * 180 / math.pi
    return theta_degrees

def rotate_center(image, angle):
    """rotate a Surface, maintaining position."""
    loc = image.get_rect().center  #rot_image is not defined
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def point_in_triangle(point, triangle):
    b1 = sign(point, triangle[0], triangle[1]) < 0
    b2 = sign(point, triangle[1], triangle[2]) < 0
    b3 = sign(point, triangle[2], triangle[0]) < 0
    return ((b1 == b2) and (b2 == b3))
