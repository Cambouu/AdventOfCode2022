import os

def get_matches():
    matches = []

    with open(os.path.join('.', 'aoc', 'day02.txt'), 'r') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            
            match = tuple(line.split())
            matches.append(match)
    
    return matches

def match_result_part1(opponent, me):
    '''
    Rock:    A, X, +1
    Paper:   B, Y, +2
    Scissor: C, Z, +3
    '''
    selection_score = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    if opponent == 'A':
        if me == 'X': match_score = 3
        elif me == 'Y': match_score = 6
        elif me == 'Z': match_score = 0
    elif opponent == 'B':
        if me == 'X': match_score =  0
        elif me == 'Y': match_score =  3
        elif me == 'Z': match_score =  6
    elif opponent == 'C':
        if me == 'X': match_score =  6
        elif me == 'Y': match_score =  0
        elif me == 'Z': match_score =  3
    else: match_score = None
    
    return match_score + selection_score[me]

def match_result_part2(opponent, result):
    '''
    Rock:    A, +1
    Paper:   B, +2
    Scissor: C, +3
    Lose:    X, +0
    Draw:    Y, +3
    Win:     Z, +6
    '''
    if opponent == 'A' and result == 'X':   return 0 + 3
    elif opponent == 'A' and result == 'Y': return 3 + 1
    elif opponent == 'A' and result == 'Z': return 6 + 2
    elif opponent == 'B' and result == 'X': return 0 + 1
    elif opponent == 'B' and result == 'Y': return 3 + 2
    elif opponent == 'B' and result == 'Z': return 6 + 3
    elif opponent == 'C' and result == 'X': return 0 + 2
    elif opponent == 'C' and result == 'Y': return 3 + 3
    elif opponent == 'C' and result == 'Z': return 6 + 1
    else: return None

def score(matches, part):
    total_score = 0

    for opponent, me in matches:
        if part == 1:
            match_score = match_result_part1(opponent, me)
        elif part == 2:
            match_score = match_result_part2(opponent, me)
        total_score += match_score
    
    return total_score

if __name__ == '__main__':
    matches = get_matches()

    print('Part 1')
    total_score_part1 = score(matches, 1)
    print('Total score: {0}'.format(total_score_part1))

    print('Part 2')
    total_score_part2 = score(matches, 2)
    print('Total score: {0}'.format(total_score_part2))