import math

def is_collide_with(entity1, entity2):
    if entity1.entity_shape == "circle" and entity2.entity_shape == "circle":
        diff_x = entity1.x - entity2.x
        diff_y = entity1.y - entity2.y
        distance = math.sqrt(diff_x * diff_x + diff_y * diff_y)
        if distance <= entity1.radius + entity2.radius:
            return True
        else:
            return False
    elif entity1.entity_shape == "circle" and entity2.entity_shape == "rect":
        if entity1.y <= entity2.y:
            diff_y = entity2.y - entity1.y
            if entity1.x <= entity2.x:
                diff_x = entity2.x - entity1.x
                distance = math.sqrt(diff_x * diff_x + diff_y * diff_y)
                if distance <= entity1.radius:
                    return True
                else:
                    return False
            elif entity2.x < entity1.x < entity2.x + entity2.width:
                distance = diff_y
                if distance <= entity1.radius:
                    return True
                else:
                    return False
            elif entity2.x + entity2.width <= entity1.x:
                diff_x = entity1.x - entity2.x + entity2.width
                distance = math.sqrt(diff_x * diff_x + diff_y * diff_y)
                if distance <= entity1.radius:
                    return True
                else:
                    return False
        elif entity2.y < entity1.y < entity2.y + entity2.height:
            if entity1.x <= entity2.x:
                diff_x = entity2.x - entity1.x
                distance = diff_x
                if distance <= entity1.radius:
                    return True
                else:
                    return False
            elif entity2.x < entity1.x < entity2.x + entity2.width:
                return True
            elif entity2.x + entity2.width <= entity1.x:
                diff_x = entity1.x - (entity2.x + entity2.width)
                distance = diff_x
                if distance <= entity1.radius:
                    return True
                else:
                    return False
        elif entity2.y + entity2.height <= entity1.y:
            diff_y = entity1.y - (entity2.y + entity2.height)
            if entity1.x <= entity2.x:
                diff_x = entity2.x - entity1.x
                distance = math.sqrt(diff_x * diff_x + diff_y * diff_y)
                if distance <= entity1.radius:
                    return True
                else:
                    return False
            elif entity2.x < entity1.x < entity2.x + entity2.width:
                distance = diff_y
                if distance <= entity1.radius:
                    return True
                else:
                    return False
            elif entity2.x + entity2.width <= entity1.x:
                diff_x = entity1.x - (entity2.x + entity2.width)
                distance = math.sqrt(diff_x * diff_x + diff_y * diff_y)
                if distance <= entity1.radius:
                    return True
                else:
                    return False
    elif entity1.entity_shape == "rect" and entity2.entity_shape == "rect":
        x1 = entity1.x
        y1 = entity1.y
        w1 = entity1.width
        h1 = entity1.height
        x2 = entity2.x
        y2 = entity2.y
        w2 = entity2.width
        h2 = entity2.height
        diff_x = abs(x2 + h2 - x1)
        if abs(x1 + w1 - x2) >= abs(x2 + w2 - x1):
            diff_x = abs(x1 + w1 - x2)
        else:
            diff_x = abs(x2 + w2 - x1)
        if abs(y1 + h1 - y2) >= abs(y2 + h2 - y1):
            diff_y = abs(y1 + h1 - y2)
        else:
            diff_y = abs(y2 + h2 - y1)
        if diff_x <= w1 + w2 and diff_y <= h1 + h2:
            return True
        else:
            return False