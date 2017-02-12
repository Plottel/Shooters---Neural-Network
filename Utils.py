from pygame.rect import Rect
import math
from Renderer import Renderer


def lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    a_dx = x2 - x1
    a_dy = y2 - y1
    b_dx = x4 - x3
    b_dy = y4 - y3

    try:
        s = (-a_dy * (x1 - x3) + a_dx * (y1 - y3)) / (-b_dx * a_dy + a_dx * b_dy)
        t = (+b_dx * (y1 - y3) - b_dy * (x1 - x3)) / (-b_dx * a_dy + a_dx * b_dy)
        return s >= 0 and s <= 1 and t >= 0 and t <= 1
    except ZeroDivisionError:
        return False


def normalized_vector_from_to(pt_from, pt_to):
    x_offset = pt_to[0] - pt_from[0]
    y_offset = pt_to[1] - pt_from[1]

    direct_distance = math.sqrt((x_offset * x_offset) + (y_offset * y_offset))

    try:
        return x_offset / direct_distance, y_offset / direct_distance
    except ZeroDivisionError:
        return 0, 0


def get_tri_center_point(tri):
    far_side_mid_x = tri[1][0] + ((tri[2][0] - tri[1][0]) / 2)
    far_side_mid_y = tri[1][1] + ((tri[2][1] - tri[1][1]) / 2)

    center_point_x = tri[0][0] + ((far_side_mid_x - tri[0][0]) / 2)
    center_point_y = tri[0][1] + ((far_side_mid_y - tri[0][1]) / 2)

    return math.floor(center_point_x), math.floor(center_point_y)


# Specifies if a rectangle intersects with a triangle.
# Triangle is given as 3 points
# Rectangle given as a pygame rect.
# Tests each corner of the rectangle by extending a line from the corner to and through the triangle.
# If the line intersects with exactly one triangle line, they are intersecting.
def rect_tri_intersect(rect, tri):
    # Find the center point of the triangle
    tri_center = get_tri_center_point(tri)

    # Only check center
    points_to_check = [rect.center]

    # For each corner in the Rect
    for rect_pt in points_to_check:
        num_intersections = 0

        # Join the line between Rect pt -> Triangle Center
        vector_to_tri_center = normalized_vector_from_to(rect_pt, tri_center)

        # Extend the line in the direction it was going WAYY past triangle
        ext_line = rect_pt[0] + (vector_to_tri_center[0] * 100000), rect_pt[1] + (vector_to_tri_center[1] * 100000)

        # Test the line for an intersection against each line in the triangle
        num_intersections += int(lines_intersect(tri[0][0], tri[0][1], tri[1][0], tri[1][1], rect_pt[0], rect_pt[1], ext_line[0], ext_line[1]))
        num_intersections += int(lines_intersect(tri[1][0], tri[1][1], tri[2][0], tri[2][1], rect_pt[0], rect_pt[1], ext_line[0], ext_line[1]))
        num_intersections += int(lines_intersect(tri[2][0], tri[2][1], tri[0][0], tri[0][1], rect_pt[0], rect_pt[1], ext_line[0], ext_line[1]))

        # If it collides with exactly 1 line, we have a Triangle -> Rect intersection
        if num_intersections == 1:
            return True

    # If we go through each corner without having exactly 1 intersection, there is no collision.
    return False

