import re

import math
from sklearn.metrics.pairwise import cosine_similarity

def replace_whitespace(text):
    return re.sub(r'\s+', '-', text)

def get_cosine_similarity(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]

def vectorize_string(string):
    return [ord(char) for char in string]

def get_cosine_similarity2(vector1, vector2): # use this if the dimensions in numpy are different (NOT EQUAL IN SHAPE)
    return sum(a * b for a, b in zip(vector1, vector2)) / (math.sqrt(sum(a * a for a in vector1)) * math.sqrt(sum(b * b for b in vector2)))

def convert_code_to_string(code):
    return ''.join(chr(i) for i in code)

def capitalize_all_words(string):
    return ' '.join(word.capitalize() for word in string.split(' '))