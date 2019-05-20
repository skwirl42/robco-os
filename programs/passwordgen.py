# Format a file of English words so they are valid data
# for "password" options in the RobCo terminal game
import random
import os

with open(os.path.join('programs', 'trimmed-words.txt'), 'r') as file:

    raw_text = file.readlines()
    clean_text = ['secretsecretwords'] # Add one 17 character string to this set :)

    for lines, word in enumerate(raw_text):
        clean_text.append(raw_text[lines].rstrip('\n'))

word_groups = {} # Holds the block of indices and entries that follow
sorted_text = []


def arrange_words_by_length(unsorted_text):

    global sorted_text
    sorted_text = sorted(unsorted_text, key=len)
    last_word_length = 0

    # Keep track of the blocks of words and where they start
    for idx, words in enumerate(sorted_text):

        # Passwords in the terminal game are ALLCAPS
        sorted_text[idx] = words.upper()
        word_length = len(words)

        if word_length > last_word_length:
            word_groups[word_length] = [idx, 0]
            last_word_length = word_length

        # Figure out the number of words in each group
        # This dict is naturally ordered, so this works ok through word length of 16
        group_keys = sorted(word_groups.keys())
        for index, group in enumerate(group_keys):
            if index < len(group_keys) - 1:
                word_groups[group][1] = word_groups[group_keys[index + 1]][0] - word_groups[group][0]
            else:
                word_groups[group][1] = len(sorted_text) - word_groups[group][0]
"""
    for key in word_groups:
        print('Words of length {0}, '
              'have {1} entries at index {2}'.format(str(key),
                                                     str(word_groups[key][1]),
                                                     str(word_groups[key][0])))
"""

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

    arrange_words_by_length(clean_text)
    random_list = []

    if length_of_words in word_groups.keys():

        word_block_index = word_groups[length_of_words][0]
        word_block_size = word_groups[length_of_words][1]

        password_index = random.randrange(word_block_index, word_block_index + word_block_size)
        password = sorted_text[password_index]

        # Prepare a table of
        similarities_table = {}
        for i in range(0, length_of_words):
            similarities_table[i] = []

        for i in range(word_block_index, word_block_index + word_block_size):
            if i == password_index:
                continue
            similarity_count = count_similarities(sorted_text[i], password)
            similarities_table[similarity_count].append(sorted_text[i])

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
