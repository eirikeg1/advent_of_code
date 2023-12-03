from collections import defaultdict

def get_max_counts(line):
    max_counts = defaultdict(lambda: 0)
    for color_count in line:
        count, color = color_count.strip().split(" ")
        if int(count) > max_counts[color]:
            max_counts[color] = int(count)
    return max_counts
        

def get_possible_game_ids(file, max_counts):
    ids = []
    powers = []
    for line in file:
        line_content = line.replace(";", ",").strip().split(":")
        game_number = int(line_content[0].split(" ")[1].strip())
        game_results = line_content[1].strip().split(",")
        
        counts = get_max_counts(game_results)
        powers.append(int(counts["red"] * counts["green"] * counts["blue"]))
        if all(counts[color] <= max_counts[color] for color in counts):
            ids.append(game_number)
    return ids, powers
    

if __name__ == '__main__':
    input_file = '2_input.txt'
    max_counts = {"red": 12, "green": 13, "blue": 14}
    with open(input_file, 'r') as file:
        lines = file.readlines()
        game_ids, powers = get_possible_game_ids(lines, max_counts)
        print(f"The sum of all possible game ids is {sum(game_ids)}")
        print(f"The power is {sum(powers)}")