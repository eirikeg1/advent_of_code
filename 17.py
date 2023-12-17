
class Node:
    
    up = None
    down = None
    left = None
    right = None
    
    x_pos = 0
    y_pos = 0
    
    def __init__(self, heat, x_pos, y_pos):
        self.heat = heat
        self.x_pos = x_pos
        self.y_pos = y_pos
        

        

    




if __name__ == '__main__':
    with open('17_input_small.txt') as f:
        lines = f.readlines()