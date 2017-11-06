# -*- coding: utf-8 -*-
from random import choice
from string import ascii_letters, digits


def random_str(length=8):
    char = ascii_letters + digits
    return "".join(choice(char) for _ in range(length))


def random_num(length=8):
    char = digits
    return "".join(choice(char) for _ in range(length))


def random_alpha(length=6):
    char = ascii_letters
    return "".join(choice(char) for _ in range(length))


if __name__ == "__main__":
    print random_str(67)
