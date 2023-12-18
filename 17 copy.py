import bisect
from enum import Enum
import sys
import itertools

class Direction(Enum):
        UP = 'UP'
        DOWN = 'DOWN'
        LEFT = 'LEFT'
        RIGHT = 'RIGHT'

class Node:
    up = None
    down = None
    left = None
    right = None
    
    x_pos = 0
    y_pos = 0
    cost = sys.maxsize
    
    def __init__(self, heat, x_pos, y_pos):
        self.heat = heat
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def __str__(self):
        return f"({self.x_pos}, {self.y_pos})"
        
    def get_pos(self):
        return (self.x_pos, self.y_pos)
    

class Path:

    def __init__(self, node = None, path = None):
        if not node and not path:
            raise Exception("Must provide either a node or a path")
        
        if not path:
            self.start = node
            self.path = []
            self.current_direction = None
            self.current_direction_length = 0
            self.score = node.heat
            self.end = node
            self.visited = {node}
        else:
            self.path = path.path.copy()
            self.visited = path.visited.copy()
            self.start = path.start
            self.score = path.score
            self.current_direction = path.current_direction
            self.current_direction_length = path.current_direction_length
            self.end = path.end
            
        
    def add(self, node, direction):
        if direction != self.current_direction:
            self.current_direction_length = 0
            self.current_direction = direction
        
        if self.current_direction_length >= 3:
            return False
        
        if node in self.visited:
            return False
        
        self.visited.add(node)
        self.score += node.heat
        
        if node.cost <= self.score:
            return False
        
        node.cost = self.score
        self.end = node
        self.current_direction_length += 1
        self.path.append(node)
            
        return True
    
    def count(self):
        return sum([node.heat for node in self.path])
    
    def __lt__(self, path):
        return self.score < path.score



class Queue:
    _queue = []
    
    def add(self, path: Path):
        bisect.insort(self._queue, (path.score, path))
    
    def pop(self):
        return self._queue.pop(0)[1]
    
    def is_empty(self):
        return len(self._queue) == 0
    
    def print_queue(self):
        for path in self._queue:
            print(path[0], end=' ')
        print()
        
    def __len__(self):
        return len(self._queue)

class CityMap:
    map: list[list[Node]] = None
    queue = Queue()
    
    input_file: list[str] = None
    
    def read_file(self, file_name = "input_files/17_small.txt"):
        with open(file_name) as f:
            lines = f.readlines()
            self.input_file = [line.strip() for line in lines]
        
        self.map = []
        
        # create nodes
        for y_pos, line in enumerate(self.input_file):
            row = []
            self.map.append(row)
            for x_pos, heat in enumerate(line):
                row.append(Node(int(heat), int(x_pos), int(y_pos)))
        
        # set up connections
        for row in self.map:
            for node in row:
                x_pos, y_pos = node.get_pos()
                
                above = y_pos - 1
                below = y_pos + 1
                left = x_pos - 1
                right = x_pos + 1
                
                if y_pos > 0:
                    node.up = self.map[above][x_pos]
                
                if below < len(self.map):
                    node.down = self.map[below][x_pos]
                
                if x_pos > 0:
                    node.left = self.map[y_pos][left]
                
                if right < len(self.map[y_pos]):
                    node.right = self.map[y_pos][right]
                
                
        print(f"Map size: {len(self.map)}x{len(self.map[0])}= {len(self.map) * len(self.map[0])}")
            
    def find_shortest_path(self) -> Path:
        start_node = self.map[0][0]
        end_node = self.map[-1][-1]
        
        best_path = None
        start = Path(node = start_node)
        self.queue.add(start)
        
        while not self.queue.is_empty():
            path = self.queue.pop()
            node = path.end
            
            # if len(path.path) > 20000:
            #     continue
            
            
            if node == end_node:
                if not best_path or path.score < best_path.score:
                    best_path = path
            
            # if node in path.visited:
            #     continue
            
            path.visited.add(node)
            
            if node.up and node.up not in path.visited and node.up.cost > path.score:
                new_path = Path(path = path)
                if new_path.add(node.up, Direction.UP):
                    self.queue.add(new_path)
            
            if node.down and node.down not in path.visited and node.down.cost > path.score:
                new_path = Path(path = path)
                if new_path.add(node.down, Direction.DOWN):
                    self.queue.add(new_path)
            
            if node.left and node.left not in path.visited and node.left.cost > path.score:
                new_path = Path(path = path)
                if new_path.add(node.left, Direction.LEFT):
                    self.queue.add(new_path)
            
            if node.right and node.right not in path.visited and node.right.cost > path.score:
                new_path = Path(path = path)
                if new_path.add(node.right, Direction.RIGHT):
                    self.queue.add(new_path)
                    
        return best_path
    
    
    def print_map(self):
        for row in self.map:
            for node in row:
                print(node.heat, end='')
            print()
            
    def print_path(self, path: Path):
        for row in self.map:
            for node in row:
                if node in path.path:
                    print('█', end=' ')
                else:
                    print(node.heat, end=' ')
            print()
        
        
if __name__ == '__main__':
    city_map = CityMap()
    city_map.read_file('input_files/17_small.txt')
    
    shortest = city_map.find_shortest_path()
    
    city_map.print_path(shortest)
    print(f"Total heat: {shortest.count()}")