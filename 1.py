lookup_table = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def search_digit(string, i):
    if string[i].isdigit():
        return string[i]
    for digit in lookup_table:
        if string[i:i+len(digit)] == digit:
            return lookup_table[digit]

def get_digits(line: str):
    first, last = None, None
    for i, _ in enumerate(line):
        cur_digit = search_digit(line, i)
        if cur_digit is not None:
            last = cur_digit
            if not first:
                first = cur_digit
    print(f"{line} -> {first}{last}")
    return int(f"{first}{last}")

def get_calibration_codes(file_name: str):
    codes = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            codes.append(get_digits(line))
    return codes    

# If run from main
if __name__ == '__main__':
    input_file = '1_input.txt'
    
    print(f"The sum of the calibration codes is {sum(get_calibration_codes(input_file))}")
