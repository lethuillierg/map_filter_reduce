"""
Input: Iliad from Homer
Output: one text consisting of iliadic sentences containing a reference to the Olympus
"""

import requests
import re
import string

# not mandatory: just helps with type hinting (`typing.List[str]`)
import typing

# Note: while _map_ and _filter_ do not need to be imported,
#       _reduce_ has to be imported from _functools_
from functools import reduce

# Download The Iliad from Homer (from gutenberg.org)
url = 'https://www.gutenberg.org/cache/epub/16452/pg16452.txt'
iliad = requests.get(url).text

# Note: type hinting is being used here when implementing the function
# Example: `def get_sentences(iliad: str) -> typing.List[str]:`
#               type of the argument _^      ^_ type of the returned object


def get_sentences(iliad: str) -> typing.List[str]:
    """
    Preprocessing:
    - clean the text
    - return a list of strings (corresponding to sentences)
    """

    # 1. using a regex, replace the newlines with a space
    iliad = re.sub('\r\n', ' ', iliad)
    # 2. using a regex, remove `[<number>]` (e.g., `abc[12]` -> `abc`)
    iliad = re.sub('\\[\d+\\]', '', iliad)
    # 3. remove all digits using the maketrans+translate idiom
    iliad = iliad.translate(str.maketrans('', '', string.digits))
    # 4. split on `.` to create a list of sentences
    return iliad.split('.')


def get_olympian_sentences(sentences: typing.List[str]) -> typing.List[str]:
    """
    ------
    FILTER
    ------
    First, split the whole text into sentences based on the punctuation `.`
    then, filter to only keep the sentences containing the prefix `olymp` to
          match `Olympus`, `Olympian`, etc.
    Note: each sentence is lowered in order to make the match case insensitive
           but because this is just a filter, it does not transform the sentences
           into lower case. In other words, `t.lower()` does only occur in the
           lambda and has no effect on the filtered sentences.
    """
    return list(filter(lambda s: 'olymp' in s.lower(), sentences))


def modernize_sentences(sentences: typing.List[str]) -> typing.List[str]:
    """
    ---
    MAP
    ---
    Replace `’d` with `ed` and strip (that is: remove empty space
    at the beginning and end of the sentence)
    """
    return list(map(lambda s: s.replace('’d', 'ed').strip(), sentences))


def merge_sentences(sentences: typing.List[str]) -> str:
    """
    ------
    REDUCE
    ------
    Transform the list of strings into one string
    Note:
    - the lambda takes two arguments: `a` (sentence N) and `b` (sentence N+1)
    - the last character of sentence N (`a[-1]`) is checked:
        ° if it is `.`, the two sentences are directly concatenated (`a + b`)
        ° if it is not `.`, a `.` is inserted between the sentences (`a + '. ' + b`)
    - a ternary operator is used for the condition: `<output A> if <condition> else <output B>`
    """
    return reduce(lambda a, b: a + b if a[-1] == '.' else a + '. ' + b, sentences)


# For debugging purposes, I suggest you to print the intermediary variables
sentences = get_sentences(iliad)
olympian_sentences = get_olympian_sentences(sentences)

# print(olympian_sentences)

modernized_sentences = modernize_sentences(olympian_sentences)

# print(modernized_sentences)

olympian_iliad = merge_sentences(modernized_sentences)

print(olympian_iliad)
