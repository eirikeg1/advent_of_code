import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.io.FileReader;

enum Direction {
    RIGHT, LEFT, UP, DOWN
}

class Instruction {
    Direction direction;
    int steps;
    String color;

    public Instruction(Direction direction, int steps, String color) {
        this.direction = direction;
        this.steps = steps;
        this.color = color;
    }
}

class CustomList<T> {
    private int size = 1000000;
    private int[] list = new int[size];

    double growthFactor = 1.2;

    int start = size / 2;
    int end = start + 1;

    public CustomList(int size) {
        this.size = size;
        list = new int[size];
        start = size / 2;
        end = start + 1;
    }

    public CustomList() {
        list = new int[size];
        start = size / 2;
        end = start + 1;
    }

    public void addStart(String element) {
        if (start == 0) {
            int newSize = (int) Math.round(size * growthFactor);
            int[] newList = new int[newSize];
            for (int i = 0; i < size; i++) {
                newList[i + size / 2] = list[i];
            }
            list = newList;
            start = newSize / 2;
            end = start + size;
            size = newSize;
        }

        list[--start] = convert(element);
    }

    public void addEnd(String element) {
        if (end == size) {
            int newSize = (int) Math.round(size * growthFactor);
            int[] newList = new int[newSize];
            for (int i = 0; i < size; i++) {
                newList[i] = list[i];
            }
            list = newList;
            start = newSize / 2;
            end = start + size;
            size = newSize;
        }
        list[end++] = convert(element);
    }

    public int convert(String element) {
        if (element.equals("#")) {
            return 1;
        } else {
            return 0;
        }
    }

    public String convert(int element) {
        if (element == 1) {
            return "#";
        } else {
            return ".";
        }
    }

    public void printRow() {
        for (int i = start; i < end; i++) {
            System.out.print(convert(list[i]));
        }
    }

    public String get(int index) {
        return convert(list[index + start]);
    }

    public void set(int index, String element) {
        list[index + start] = convert(element);
    }

    public int size() {
        return end - start;
    }

}

class Digger {
    ArrayList<CustomList<String>> map;
    ArrayList<Instruction> instructions = new ArrayList<>();

    int xPos, yPos, counter = 0;

    HashMap<String, Direction> directions = new HashMap<>(Map.of(
            // Part 1:
            "R", Direction.RIGHT,
            "L", Direction.LEFT,
            "U", Direction.UP,
            "D", Direction.DOWN,

            // Part 2:
            "0", Direction.RIGHT,
            "1", Direction.DOWN,
            "2", Direction.LEFT,
            "3", Direction.UP));

    public Digger(String filePath) {
        initDigger();
        readInstructions(filePath);
    }

    private void expandMap(Direction direction, int steps) {

        int colSize = map.size();
        int rowSize = map.get(0).size();

        switch (direction) {
            case RIGHT:
                int newCols = Math.max(0, xPos + steps - rowSize);
                for (CustomList<String> row : map) {
                    for (int i = 0; i < newCols; i++) {
                        row.addEnd(".");
                    }
                }
                break;

            case LEFT:
                newCols = Math.max(0, steps - xPos);
                if (newCols > 0) {
                    for (CustomList<String> row : map) {
                        for (int i = 0; i < newCols; i++) {
                            row.addStart(".");
                        }
                    }
                    xPos += newCols;
                }
                break;

            case UP:
                int newRows = Math.max(0, steps - yPos);
                if (newRows > 0) {
                    for (int i = 0; i < newRows; i++) {
                        map.add(0, new CustomList<>(rowSize));
                        if (i % 1000 == 0)
                            System.out.println(" * loop 1: " + i + " / " + newRows + " rows");
                    }
                    yPos += newRows;
                }
                break;

            case DOWN:
                newRows = Math.max(0, yPos + steps - colSize);
                for (int i = 0; i < newRows; i++) {
                    if (i % 1000 == 0)
                        System.out.println(" * loop 1: " + i + " / " + newRows + " rows");
                    map.add(new CustomList<>(rowSize));
                }
                break;
        }
    }

    public void dig() {
        for (Instruction instruction : instructions) {
            digInstruction(instruction);
        }

        fillBorders();
    }

    private void digInstruction(Instruction instruction) {
        digInstruction(instruction.direction, instruction.steps, instruction.color);
    }

    private void digInstruction(Direction direction, int steps, String color) {
        int destRow = yPos;
        int destCol = xPos;

        switch (direction) {
            case RIGHT:
                destCol += steps;
                break;

            case LEFT:
                destCol = Math.max(0, destCol - steps);
                break;

            case UP:
                destRow = Math.max(0, destRow - steps);
                break;

            case DOWN:
                destRow += steps;
                break;
        }

        // System.out.println(
        // "Digging " + direction + " " + steps + " steps " + color + " from (" + xPos +
        // ", " + yPos + ") to ("
        // + destRow + ", " + destCol + ")");

        System.out.println(" * expanding");
        expandMap(direction, steps);
        System.out.println(" * expanded");

        // System.out.println("Map size: " + map.size() + "x" + map.get(0).size());

        for (int i = Math.min(yPos, destRow); i <= Math.max(yPos, destRow); i++) {
            for (int j = Math.min(xPos, destCol); j < Math.max(xPos, destCol); j++) {
                // System.out.println("Digging (" + i + ", " + j + ")" + " out of steps: " +
                // steps);
                map.get(i).set(j, "#");
            }
        }

        // Update position
        xPos = destCol;
        yPos = destRow;

    }

    private void recursiveFill(int row, int col) {
        Queue<int[]> queue = new LinkedList<>();
        queue.add(new int[] { row, col });

        while (!queue.isEmpty()) {
            int[] pos = queue.poll();
            row = pos[0];
            col = pos[1];

            if (row < 0 || row >= map.size() || col < 0 || col >= map.get(row).size()
                    || map.get(row).get(col).equals("#")) {
                continue;
            }

            map.get(row).set(col, "#");

            if (row > 0 && map.get(row - 1).get(col).equals(".")) { // up
                queue.add(new int[] { row - 1, col });
            }
            if (row < map.size() - 1 && map.get(row + 1).get(col).equals(".")) { // down
                queue.add(new int[] { row + 1, col });
            }
            if (col > 0 && map.get(row).get(col - 1).equals(".")) { // left
                queue.add(new int[] { row, col - 1 });
            }
            if (col < map.get(row).size() - 1 && map.get(row).get(col + 1).equals(".")) { // right
                queue.add(new int[] { row, col + 1 });
            }
        }
    }

    private int[] findEntry() {
        int row, column = -1;

        for (row = 0; row < map.size(); row++) {
            for (column = 0; column < map.get(row).size(); column++) {
                if (map.get(row).get(column).equals("#")) {

                    // Check left
                    if (column > 0 && map.get(row).get(column - 1).equals("#")) {
                        continue;
                    }

                    // Check right
                    if (column < map.get(row).size() - 1 && map.get(row).get(column + 1).equals("#")) {
                        continue;
                    }

                    return new int[] { row, column + 1 };
                }
            }
        }

        return null;
    }

    private void fillBorders() {

        int[] entry = findEntry();
        int row = entry[0];
        int col = entry[1];

        System.out.println("Entry: (" + row + ", " + col + ")");

        recursiveFill(row, col);

    }

    public void readInstructions(String filePath) {
        // Read instructions from file
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filePath));
            String line;
            while ((line = reader.readLine()) != null) {

                String[] cells = line.split(" ");

                // Part 1 parsing:

                // Direction direction = directions.get(cells[0]);
                // int steps = Integer.parseInt(cells[1]);
                // String color = cells[2];

                // Part 2 parsing:
                String hexadecimal = cells[2];
                String stepsHex = hexadecimal.substring(2, 7);
                String directionHex = hexadecimal.substring(7, 8);

                int steps = Integer.parseInt(stepsHex, 16);
                Direction direction = directions.get(directionHex);

                String color = "";
                // System.out.println("Hex: " + hexadecimal + ", Steps: " + steps + ",
                // Direction: " + direction);

                instructions.add(new Instruction(direction, steps, color));
            }
            reader.close();
        } catch (IOException e) {
            System.out.println("Error reading file: " + e);
        }
    }

    public void initDigger() {
        map = new ArrayList<>();
        CustomList<String> initial = new CustomList<>();
        initial.addStart(".");
        map.add(initial);
    }

    public void printMap() {
        for (CustomList<String> row : this.map) {
            row.printRow();
            System.out.println();
        }
    }

    public int count() {
        counter = 0;
        for (CustomList<String> row : this.map) {
            counter += row.size();
        }
        return counter;
    }
}

class Java18 {
    public static void main(String[] args) throws IOException {
        String file = args[0];
        if (args.length != 1)
            file = "18";

        Digger digger = new Digger("input_files/" + file + ".txt");

        digger.dig();
        digger.printMap();

        System.out.println("Part 1: " + digger.count());

    }
}