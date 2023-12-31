import bisect
from enum import Enum
import sys
import itertools
import heapq

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

    visited = False
    id = itertools.count()
    
    x_pos = 0
    y_pos = 0
    cost = sys.maxsize
    
    def __init__(self, heat, x_pos, y_pos):
        self.heat = heat
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.id = f"({x_pos}, {y_pos})"
    
    def __str__(self):
        return f"({self.x_pos}, {self.y_pos})"
        
    def get_pos(self):
        return (self.x_pos, self.y_pos)
    
    def __hash__(self):
        return self.id.__hash__()
        

class Path:

    def __init__(self, node = None, path = None):
        if not node and not path:
            raise Exception("Must provide either a node or a path")
        
        if not path:
            self.start = node
            self.path = []
            self.current_direction = None
            self.current_direction_length = 0
            self.score = 0
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
        
        self.end = node
        self.score += node.heat
        self.current_direction_length += 1
        self.path.append(node)
        
        if node.cost > self.score:
            node.cost = self.score
            
        return True
    
    def count(self):
        return sum([node.heat for node in self.path])
    
    def __lt__(self, path):
        return self.score < path.score



class Queue:
    _queue = []
    
    def add(self, path: Path):
        heapq.heappush(self._queue, (path.score, path))
    
    def pop(self):
        return heapq.heappop(self._queue)[1]
    
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
            
            if node == end_node:
                if not best_path:
                    best_path = path
                else:
                    best_path = min(best_path, path, key=lambda x: x.score)
                break
            
            path.visited.add(node)
                    
            for dest, dir in [(node.up, Direction.UP), (node.down, Direction.DOWN), (node.left, Direction.LEFT), (node.right, Direction.RIGHT)]:
                if not dest:
                    continue
                if dest in path.visited:
                    continue
                if dest.cost <= path.score:
                    continue
                
                new_path = Path(path = path)
                if new_path.add(dest, dir):
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
    
    # city_map.print_path(shortest)
    print(f"Total heat: {shortest.count()}")