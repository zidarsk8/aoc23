import math

with open('input/2.txt') as f:
    text = f.read().strip()



valid_numbers = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


id_sum = 0
for line in text.splitlines():
    game_id = int(line.split(": ", 1)[0].split()[1])
    game = line.split(": ", 1)[1]
    sets = game.split("; ")
    valid = True
    for s in sets:
        counts = s.split(", ")
        for count in counts:
            number, color = count.split()
            if valid_numbers[color] < int(number):
                valid = False

    if valid:
        id_sum+=game_id

print(id_sum)

game_sum = 0
for line in text.splitlines():
    game = line.split(": ", 1)[1]
    sets = game.split("; ")
    cube_counts = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for s in sets:
        counts = s.split(", ")
        for count in counts:
            number, color = count.split()
            cube_counts[color] = max(int(number), cube_counts[color])

    power = math.prod(cube_counts.values())
    game_sum += power

print(game_sum)
