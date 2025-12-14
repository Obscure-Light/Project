import itertools
import string

def generate_combinations(min_length: int, max_length: int, character_set: str) -> list:
    """
    Genera tutte le possibili combinazioni di caratteri basate su lunghezze
    minime e massime fornite e su un set di caratteri.

    Args:
        min_length (int): Lunghezza minima della combinazione.
        max_length (int): Lunghezza massima della combinazione.
        character_set (str): Il set di caratteri da utilizzare.

    Returns:
        list: Una lista contenente tutte le combinazioni generate.
    """
    combinations = []
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(character_set, repeat=length):
            combinations.append(''.join(combo))
    return combinations
