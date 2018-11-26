def search4vowels(phrase):
    """Return any vowels found in a supplied phrase."""
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))


def search4letters(phrase, letters='aeiou'):
    """Return a set of the 'letters' found in 'phrase'."""
    return set(letters).intersection(set(phrase))
