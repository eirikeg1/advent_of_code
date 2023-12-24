import numpy as np
from sympy import Point, Line

start_bounds = 200000000000000
end_bounds = 400000000000000

class Wind:
    def __init__(self, x, y, x_vel, y_vel):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.line = Line(Point(x, y), Point(x + x_vel, y + y_vel))
        
    def is_heading_towards(self, x, y):
        return (self.x_vel > 0 and self.x < x) or (self.x_vel < 0 and self.x > x) or (self.x_vel == 0 and self.x == x)
        
    def __repr__(self):
        return f"Wind({self.x}, {self.y}, {self.x_vel}, {self.y_vel})"
          

def check_collisions(winds):
    counter = 0
    
    collisions = set()
    total = len(winds)
    
    print(f"checking collisions...")
    for i, wind1 in enumerate(winds):
        print(f"{i}/{total} checked", end="\r")
        for j, wind2 in enumerate(winds):
            if i == j or f'{i},{j}' in collisions or f'{j},{i}' in collisions:
                continue
            intersection = wind1.line.intersection(wind2.line)
            if intersection:
                x = intersection[0].x
                y = intersection[0].y
    
                if (x >= start_bounds and
                    x <= end_bounds and
                    y >= start_bounds and
                    y <= end_bounds):
                    # print(f"Found intersection for ({i}, {j}): ({int(x)}, {int(y)}): intersection: {intersection}, wind1: ({wind1.x}, {wind1.y}), wind2: ({wind2.x}, {wind2.y})")
                    if wind1.is_heading_towards(x, y) and wind2.is_heading_towards(x, y):
                        collisions.add(f'{i},{j}')
                        counter += 1
                
    return counter
        

if __name__ == '__main__':
    with open('input_files/24.txt') as f:
        print(f"reading file...")
        input_data = f.readlines()
        input_data = [row.strip() for row in input_data]
        
        winds = []
        
        print(f"parsing data...")
        for row in input_data:
            start_pos, direction = row.split(" @ ")
            x_pos, y_pos, z_pos = start_pos.split(", ")
            x_vel, y_vel, z_vel = direction.split(", ")
            # print(f"coords: {x_pos}, {y_pos}, {z_pos}, vel: {x_vel}, {y_vel}, {z_vel}")
            winds.append(Wind(int(x_pos), int(y_pos), int(x_vel), int(y_vel)))

        collisions = check_collisions(winds)
        
        print(f"found {collisions} collisions in bounds")