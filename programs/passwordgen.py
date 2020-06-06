# Format a file of English words so they are valid data
# for "password" options in the RobCo terminal game
import random
import os

def read_words_of_length(filepath, length):
    words = []
    with open(filepath, 'r') as file:
        for word in file:
            word = word.rstrip('\n')
            if len(word) == length:
                words.append(word.upper())
    return words

def count_similarities(word_a, word_b):
    count = 0
    for n in range(0, len(word_a)):
        if word_a[n] == word_b[n]:
            count += 1
    return count

def get_single_word_similarity(available_similarities, difficulty):
    # TODO: Implement some sort of probabilistic method of picking similarities
    # based on the difficulty level
    return random.choice(available_similarities)

def get_available_similarities(similarities_table):
    key_list = list(similarities_table.keys())[0:-1]
    return list(filter(lambda x: len(similarities_table[x]) > 0, key_list))

def get_list_of_words(num_words, length_of_words, difficulty=1):
    # For the game it's best that words have a length between 4 and 12,
    # but I'm leaving the option for any choice.
    # Words of length 15 or more are impractical though

    words = read_words_of_length(os.path.join('programs', 'trimmed-words.txt'), length_of_words)
    password = random.choice(words)

    # Prepare a table of
    similarities_table = {}
    for i in range(0, length_of_words):
        similarities_table[i] = []

    for word in words:
        if word == password:
            continue
        similarity_count = count_similarities(word, password)
        similarities_table[similarity_count].append(word)

    random_list = []
    random_list.append(password)

    # We're going to take a random sampling of words from a random sampling
    # of similarities, rather than a random word from a contiguous block of words
    for i in range(1, num_words):
        available_similarities = get_available_similarities(similarities_table)
        similarity_desired = get_single_word_similarity(available_similarities, difficulty)
        word = random.choice(similarities_table[similarity_desired])
        random_list.append(word)
        similarities_table[similarity_desired].remove(word)

    return password, random_list


if __name__ == '__main__':

    random_passwords = get_list_of_words(4, 8)
    print(random_passwords)
