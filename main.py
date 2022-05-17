from random import randint


def key_gen(n):
    s = [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
        [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
        [str(i) for i in range(10)]

    key = []
    for i in range(n):
        key.append(s[randint(1, len(s) - 1)])

    return "".join(key)





