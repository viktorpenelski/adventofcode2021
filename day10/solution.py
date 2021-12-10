expected = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>'
}

score_invalid = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

score_complete = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def solve(line):
    stack = []
    for ch in line:
        if ch in expected:
            stack.append(expected[ch])
        else:
            if len(stack) == 0 or stack.pop() != ch:
                return score_invalid[ch], 0

    fixed_score = 0
    while stack:
        fixed_score *= 5
        fixed_score += score_complete[stack.pop()]

    return 0, fixed_score


with open('in.txt') as f:
    lines = [list(line.strip()) for line in f.readlines()]

print(sum([solve(line)[0] for line in lines]))

completed_scores = [solve(line)[1] for line in lines if solve(line)[0] == 0]
completed_scores.sort()
print(completed_scores[int(len(completed_scores) / 2)])
