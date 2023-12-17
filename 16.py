from collections import defaultdict
from enum import Enum

class Direction(Enum):
        UP = 'UP'
        DOWN = 'DOWN'
        LEFT = 'LEFT'
        RIGHT = 'RIGHT'
        
class LightContraption:
    
    energized_count = 0
    visited = defaultdict(lambda: [])
    queue = [(0, 0, Direction.RIGHT)]
    
    def __init__(self, input_data):
        self.input_data = input_data
        self.output_data = input_data.copy()
        
    def __str__(self):
        return_str = ''
        for row in self.output_data:
            for tile in row:
                return_str += tile
            return_str += '\n'
                
        return return_str
        
    def count(self):
        self.energized_count = 0
        for row in self.output_data:
            for char in row:
                if char == '#':
                    self.energized_count += 1
        return self.energized_count
    
    def reset(self, x_pos = 0, y_pos = 0, direction = Direction.RIGHT):
        self.visited = defaultdict(lambda: [])
        self.queue = [(x_pos, y_pos, direction)]
        self.output_data = self.input_data.copy()
        self.energized_count = 0

    def set_energized(self, x_pos, y_pos):
        current_row = list(self.output_data[y_pos])
        current_row[x_pos] = '#'
        self.output_data[y_pos] = ''.join(current_row)
        
    def get_new_position(self, x_pos, y_pos, direction):
        
        new_x, new_y = x_pos, y_pos
        
        match direction:
            case Direction.UP:
                new_y = y_pos - 1
                if new_y < 0:
                    return (None, None)
            
            case Direction.DOWN:
                new_y = y_pos + 1
                if new_y >= len(self.input_data):
                    return (None, None)
            
            case Direction.LEFT:
                new_x = x_pos - 1
                if new_x < 0:
                    return (None, None)
            
            case Direction.RIGHT:
                new_x = x_pos + 1
                if new_x >= len(self.input_data[y_pos]):
                    return (None, None)
        
        return (new_x, new_y)

    def explore(self, x_pos = 0, y_pos = 0, direction = Direction.RIGHT, split_beam = False):
        
        new_x, new_y = self.get_new_position(x_pos, y_pos, direction)
        split_beam = None
        
        if direction in self.visited[(x_pos, y_pos)]:
            return
        
        self.visited[(x_pos, y_pos)].append(direction)

        match self.input_data[y_pos][x_pos]:
            case '-':
                if direction == Direction.DOWN or direction == Direction.UP:
                    split_beam = True
                
                    if x_pos > 0:
                        self.queue.append((x_pos - 1, y_pos, Direction.LEFT))
                    
                    if x_pos + 1 < len(self.input_data[y_pos]):
                        self.queue.append((x_pos + 1, y_pos, Direction.RIGHT))
                    
            case '|':
                if direction == Direction.LEFT or direction == Direction.RIGHT:
                    # print(f"split at {(x_pos, y_pos)}")
                    split_beam = True
                    if y_pos > 0:
                        self.queue.append((x_pos, y_pos - 1, Direction.UP))
                    if y_pos + 1 < len(self.input_data):
                        self.queue.append((x_pos, y_pos + 1, Direction.DOWN))
                    
            case '\\':
                if direction == Direction.UP:
                    # print(f"deflected to left at {(x_pos, y_pos)}")
                    direction = Direction.LEFT
                    
                elif direction == Direction.DOWN:
                    # print(f"deflected to right at {(x_pos, y_pos)}")
                    direction = Direction.RIGHT
                    
                elif direction == Direction.RIGHT:
                    # print(f"deflected down at {(x_pos, y_pos)}")
                    direction = direction.DOWN
                    
                elif direction == Direction.LEFT:
                    # print(f"deflected up at {(x_pos, y_pos)}")
                    direction = Direction.UP
                    
                new_x, new_y = self.get_new_position(x_pos, y_pos, direction)
                    
            case '/':
                if direction == Direction.UP:
                    direction = Direction.RIGHT
                    
                elif direction == Direction.DOWN:
                    direction = Direction.LEFT
                    
                elif direction == Direction.RIGHT:
                    direction = direction.UP
                    
                elif direction == Direction.LEFT:
                    direction = Direction.DOWN
                    
                new_x, new_y = self.get_new_position(x_pos, y_pos, direction)
 
        self.set_energized(x_pos, y_pos)
        
        if split_beam or new_x is None or new_y is None:
            return
        
        self.queue.append((new_x, new_y, direction))
        split_beam = False
        
        
    def find_light_path(self):
        while len(self.queue):
            x_pos, y_pos, direction = self.queue.pop()
            self.explore(x_pos, y_pos, direction)
            
    def find_best_entry(self):
        
        highest_col = len(self.input_data) - 1
        last_row = len(self.input_data[0]) - 1
        
        top_row = [(x, 0, direction) 
                   for x in range(1, last_row)
                   for direction in [Direction.DOWN, Direction.LEFT, Direction.RIGHT]]
        
        bottom_row = [(x, -1, direction)
                      for x in range (1, last_row)
                      for direction in [Direction.UP, Direction.LEFT, Direction.RIGHT]]
        
        columns = [(x, y, direction)
                   for x in [0, -1]
                   for y in range(1, highest_col)
                   for direction in [Direction.UP, Direction.DOWN, Direction.RIGHT]]
        
        corners = [(0, 0, Direction.RIGHT), 
                   (0, 0, Direction.DOWN),
                   (last_row, 0, Direction.RIGHT), 
                   (last_row, 0, Direction.UP),
                   (last_row, highest_col, Direction.UP),
                   (last_row, highest_col, Direction.LEFT),
                   (0, highest_col, Direction.UP),
                   (0, highest_col, Direction.RIGHT)]
        
        entries = [*top_row,
                   *bottom_row,
                   *columns,
                   *corners]

        
        best_entry = (0, 0, Direction.RIGHT)
        best_value = 0
        
        counter = 0
        
        for x, y, direction in entries:
            counter += 1
            if counter % 10 == 0:
                print(f"{counter}/{len(entries)} checked", end="\r")
    
            self.reset(x, y, direction)
            self.find_light_path()
            count = self.count()
            if count > best_value:
                best_entry = (x, y, direction)
                best_value = count
        return (best_value, *best_entry)
                        
        

if __name__ == '__main__':
    with open('16_input.txt') as f:
        input_data = f.readlines()
        input_data = [row.strip() for row in input_data]
        light_contraption = LightContraption(input_data)
        
        value, x, y, dir = light_contraption.find_best_entry()
        
        
        print(f"The best solution is at {(x, y)} in {dir}. The number of energized tiles is {value}")
        
        # print(f"{light_contraption}\n\n")
    
        # light_contraption.find_light_path()
        
        # print(f"{light_contraption}\n\n")
        
        # print(f"{light_contraption.count()} tiles was energized")
    
    
