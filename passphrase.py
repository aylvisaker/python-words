import os, math, random, string, re

#TODO date of birth
#TODO address

# list of characters for passwords
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
symbols = string.punctuation
characters = lowercase + uppercase + digits + symbols + ' '

# list of words for passphrases
commonwords1000 = open('1000.txt', 'r').readlines()
commonwords5000 = open('5000.txt', 'r').readlines()
adjectives = open("adjectives.txt", 'r').readlines()
nouns = open("nouns.txt", 'r').readlines()
electrum = open('electrum.txt', 'r').readlines()
wwf_additions = open('enable1-wwf-v4.0-wordlist-additions.txt', 'r').readlines()
enable = open('enable.txt', 'r').readlines()
# add enable to dictionaries to use a very large word list
dictionaries = [commonwords1000, commonwords5000, adjectives, nouns, electrum, wwf_additions]
dictionaries = map(lambda x: [y[:-1].lower() for y in x], dictionaries)
words = set()
minlength, maxlength = 3, 10
for word_list in dictionaries:
    words |= set(word_list)
words = list(words)
# TODO: remove words with punctuation
# pattern = re.compile("[\d{}]+$".format(re.escape(string.punctuation)))
# words = [word for word in words if pattern.match(word)]

# list of given names and surnames
male_names = list(open('malenames.txt', 'r').readlines())
female_names = list(open('femalenames.txt', 'r').readlines())
surnames = list(open('surnames.txt', 'r').readlines())
names = [male_names, female_names, surnames]
names = map(lambda x: [y[:-1].title() for y in x], names)


def secure_random_choice(bits, options, b = 0):
    """choose a random element of options. b = len(options)."""
    if not b:
        b = len(options)
    return options[int(os.urandom(bits).encode('hex'), 16) % b]


def password(bits):
    """choose a random password"""
    options = characters
    b = len(options)
    n = int(math.ceil(math.log(2 ** bits, b)))
    return ''.join([secure_random_choice(128, options) for x in range(n)])


def passphrase(bits):
    """choose a random passphrase"""
    options = words
    b = len(options)
    n = int(math.ceil(math.log(2 ** bits, b)))
    return ' '.join([secure_random_choice(128, options) for x in range(n)])


def random_name(g):
    """choose a random name. g = 0 for male, g = 1 for female."""
    return ' '.join([secure_random_choice(128, name) for name in [names[g], names[2]]])


def main():
    t, n = '', ''
    while not t in [1,2,3,4]:
        t = input('What would you like to generate?\n'
                  '1    Passwords\n'
                  '2    Passphrases\n'
                  '3    Random male names\n'
                  '4    Random female names\n')
    while not isinstance(n, int):
        n = input('How many would you like to generate?\n')
    bits = 128
    if t in [1, 2]:
        bits = input('How many bits of entropy?\n')
    algorithms = [password, passphrase, lambda x : random_name(0), lambda x : random_name(1)]
    for i in range(n):
        print(algorithms[t-1](bits))


if __name__ == '__main__':
    main()