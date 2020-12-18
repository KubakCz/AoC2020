from typing import List, Dict


def load_expresions(path: str) -> List[str]:
    f = open(path)
    expr = []
    for line in f.read().splitlines():
        expr.append(line)
    return expr


def eval_operator(a: int, b: int, operator: str) -> int:
    if operator == '+':
        return a + b
    elif operator == '*':
        return a * b
    return 0


def split_expresion(expresion: str) -> List[str]:
    tmp_tokens = expresion.split()
    tokens = []
    right_brackets = 0
    for t in tmp_tokens:
        while t[0] == '(':
            tokens.append('(')
            t = t[1:]
        while t[-1] == ')':
            right_brackets += 1
            t = t[:-1]
        tokens.append(t)
        while right_brackets > 0:
            tokens.append(')')
            right_brackets -= 1
    return tokens


def infix_to_postfix(tokenised_expresion: List[str],
                     operator_priority: Dict[str, int]) \
        -> List[str]:
    operator_stack: List[str] = []
    output_queue = []
    for t in tokenised_expresion:
        if t.isnumeric():
            output_queue.append(t)
        elif t in operator_priority:
            while len(operator_stack) > 0 and \
                    operator_stack[-1] != '(' and \
                    operator_priority[operator_stack[-1]] <= operator_priority[t]:
                output_queue.append(operator_stack.pop())
            operator_stack.append(t)
        elif t == '(':
            operator_stack.append(t)
        elif t == ')':
            while operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
    while len(operator_stack) > 0:
        output_queue.append(operator_stack.pop())
    return output_queue


def eval(tokenised_expresion: List[str],
         operator_priority: Dict[str, int]) \
        -> int:
    postfix = infix_to_postfix(tokenised_expresion, operator_priority)
    value_stack = []
    for t in postfix:
        if t.isnumeric():
            value_stack.append(int(t))
        else:
            val = eval_operator(value_stack.pop(), value_stack.pop(), t)
            value_stack.append(val)
    return value_stack[0]


def solve(file_path: str, name: str):
    print()
    print(name)
    t_expresions = list(map(split_expresion, load_expresions(file_path)))
    results = map(lambda expr: eval(expr, {'+': 1, '*': 1}), t_expresions)
    print('No priority sum:', sum(results))
    results = map(lambda expr: eval(expr, {'+': 1, '*': 2}), t_expresions)
    print('+ priority sum:', sum(results))


def test():
    expr = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
    print('\nTest:', expr)
    tokenized_expr = split_expresion(expr)
    print('No priority:', eval(tokenized_expr, {'+': 1, '*': 1}))
    print('+ priority:', eval(tokenized_expr, {'+': 1, '*': 2}))


if __name__ == '__main__':
    test()
    solve('18/input.txt', 'Task')
