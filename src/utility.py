
"""
This file contains helper function and is not dependent on any other file
"""

import re
import pandas as pd

def count_syllables(word):
    VOWEL_RUNS = re.compile("[aeiouy]+", flags=re.I)
    EXCEPTIONS = re.compile(
        # fixes trailing e issues:
        # smite, scared
        "[^aeiou]e[sd]?$|"
        # fixes adverbs:
        # nicely
        + "[^e]ely$",
        flags=re.I
    )
    ADDITIONAL = re.compile(
        # fixes incorrect subtractions from exceptions:
        # smile, scarred, raises, fated
        "[^aeioulr][lr]e[sd]?$|[csgz]es$|[td]ed$|"
        # fixes miscellaneous issues:
        # flying, piano, video, prism, fire, evaluate
        + ".y[aeiou]|ia(?!n$)|eo|ism$|[^aeiou]ire$|[^gq]ua",
        flags=re.I
    )

    vowel_runs = len(VOWEL_RUNS.findall(word))
    exceptions = len(EXCEPTIONS.findall(word))
    additional = len(ADDITIONAL.findall(word))
    return max(1, vowel_runs - exceptions + additional)

row_list = []


def writer(row_list, filename):
    df = pd.DataFrame(row_list)    
    df.to_excel(filename)  


    