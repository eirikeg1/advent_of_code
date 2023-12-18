import java.util.*;
import java.io.*;

enum Direction {
    UP, DOWN, LEFT, RIGHT;
}

class Node {
    Node up, down, left, right, previousNode;
    int x_pos, y_pos;
    int cost;
    int heat;

    public Node(int heat, int x_pos, int y_pos) {
        this.heat = heat;
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        this.cost = Integer.MAX_VALUE;
    }

    public String toString() {
        return "(" + this.x_pos + ", " + this.y_pos + ")";
    }
}

class Path implements Comparable<Path> {
    List<Node> path;
    Set<Node> visited;
    Node start, end;
    Direction currentDirection;
    int currentDirectionLength, score;

    public Path(Node node) {
        this.start = this.end = node;
        this.path = new ArrayList<>();
        this.visited = new HashSet<>();
        this.visited.add(node);
        this.score = 0;
        this.currentDirectionLength = 0;
    }

    public Path(Path other) {
        this.path = new ArrayList<>(other.path);
        this.visited = new HashSet<>(other.visited);
        this.start = other.start;
        this.end = other.end;
        this.score = other.score;
        this.currentDirection = other.currentDirection;
        this.currentDirectionLength = other.currentDirectionLength;
    }

    public boolean add(Node node, Direction direction) {
        if (direction != this.currentDirection) {
            this.currentDirection = direction;
            this.currentDirectionLength = 1;
        } else {
            this.currentDirectionLength++;
        }

        if (this.currentDirectionLength > 3) {
            return false;
        }

        if (this.visited.contains(node)) {
            return false;
        }

        this.visited.add(node);
        this.end = node;
        this.score += node.heat;
        this.path.add(node);

        if (node.cost > this.score) {
            node.cost = this.score;
        }

        return true;

    }

    public void printPath() {
        for (Node node : this.path) {
            System.out.print(node + " ");
        }
        System.out.println();
    }

    public int count() {
        return this.path.stream().mapToInt(n -> n.heat).sum();
    }

    @Override
    public int compareTo(Path other) {
        return Integer.compare(this.score, other.score);
    }
}

class CityMap {
    List<List<Node>> map;
    PriorityQueue<Path> queue;
    List<String> input_file;

    public void readFile(String fileName) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String line;
            input_file = new ArrayList<>();
            while ((line = br.readLine()) != null) {
                input_file.add(line.trim());
            }
        }

        map = new ArrayList<>();
        for (int y_pos = 0; y_pos < input_file.size(); y_pos++) {
            List<Node> row = new ArrayList<>();
            map.add(row);
            String line = input_file.get(y_pos);
            for (int x_pos = 0; x_pos < line.length(); x_pos++) {
                int heat = Character.getNumericValue(line.charAt(x_pos));
                row.add(new Node(heat, x_pos, y_pos));
            }
        }

        // Set up connections
        for (int y = 0; y < map.size(); y++) {
            for (int x = 0; x < map.get(y).size(); x++) {
                Node node = map.get(y).get(x);
                if (y > 0) node.up = map.get(y - 1).get(x);
                if (y < map.size() - 1) node.down = map.get(y + 1).get(x);
                if (x > 0) node.left = map.get(y).get(x - 1);
                if (x < map.get(y).size() - 1) node.right = map.get(y).get(x + 1);
            }
        }

        System.out.println("Map size: " + map.size() + "x" + map.get(0).size());
    }

    public Path findShortestPath() {
    PriorityQueue<Path> queue = new PriorityQueue<>(Comparator.comparingInt(p -> p.score));
    Map<Node, Path> shortestPaths = new HashMap<>();
    
    Node start = map.get(0).get(0);
    Node target = map.get(map.size() - 1).get(map.get(0).size() - 1);
    
    Path startPath = new Path(start);
    queue.add(startPath);
    shortestPaths.put(start, startPath);

    while (!queue.isEmpty()) {
        Path currentPath = queue.poll();
        Node currentNode = currentPath.end;

        if (shortestPaths.get(currentNode) != currentPath) {
            continue;
        }

        if (currentNode == target) {
            return currentPath;
        }

        for (Direction direction : Direction.values()) {
            Node neighbor = null;
            switch (direction) {
                case UP:
                    neighbor = currentNode.up;
                    break;
                case DOWN:
                    neighbor = currentNode.down;
                    break;
                case LEFT:
                    neighbor = currentNode.left;
                    break;
                case RIGHT:
                    neighbor = currentNode.right;
                    break;
            }

            if (neighbor != null && !currentPath.visited.contains(neighbor)) {
                Path newPath = new Path(currentPath);
                if (newPath.add(neighbor, direction)) {
                    Path oldPath = shortestPaths.get(neighbor);
                    if (oldPath == null || newPath.score < oldPath.score) {
                        shortestPaths.put(neighbor, newPath);
                    }
                    queue.add(newPath);
                }
            }
        }
    }

    return null; // Return null if no path is found
}

    public void printMap() {
        for (List<Node> row : map) {
            for (Node node : row) {
                System.out.print(node.heat);
            }
            System.out.println();
        }
    }

    public void printPath(Path path) {
        for (List<Node> row : map) {
            for (Node node : row) {
                if (path.visited.contains(node)) {
                    System.out.print("■ ");
                } else {
                    System.out.print(node.heat + " ");
                }
            }
            System.out.println();
        }
    }
}


class Java17 {
    public static void main(String[] args) throws IOException {
        CityMap cityMap = new CityMap();
        cityMap.readFile("input_files/" + args[0] + ".txt");


        Path path = cityMap.findShortestPath();

        cityMap.printPath(path);

        System.out.println("Shortest path: " + path.score);
    }
}