# histogram.py
import re
from collections import Counter


def read_text_file(path: str) -> str:
    """Read an entire text file and return its contents as one string.

    Args:
        path: Full absolute path to the file, including the file name.

    Returns:
        The complete contents of the file as a single string.

    Raises:
        FileNotFoundError: If no file exists at that path.
    """
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def tokenize(text: str) -> list[str]:
    """Split raw text into a list of comparable words."""
    words = ""
    for i in text:
        if not i.isalpha():
            i = " "
        words += i
    read_list = words.split(" ")
    His_list = []
    for i in read_list:
        if i != "":
            His_list.append(i.lower())
    return His_list


def histogram(
    text: str, top_n: int = 20, include_ties: bool = False
) -> list[tuple[str, int]]:
    """Return the most frequent words in text, most frequent first.

    Words are compared case-insensitively. Ties in count are broken
    alphabetically, ascending.

    Args:
        text: The text to analyse.
        top_n: How many words to return. Must be positive.
        include_ties: If False, return exactly top_n rows. If True, also
            return every word tied with the last one, so the result may
            be longer than top_n.

    Returns:
        A list of (word, count) pairs, ordered by descending count and
        then alphabetically.

    Examples:
        >>> histogram("A A A A", 1)
        [('a', 4)]
        >>> histogram("b b a a c", 2)
        [('a', 2), ('b', 2)]
        >>> histogram("b b a a c", 1)
        [('a', 2)]
        >>> histogram("b b a a c", 1, include_ties=True)
        [('a', 2), ('b', 2)]
    """
    if top_n <= 0:
        raise ValueError("top_n must be a positive integer.")

    tokens = tokenize(text)
    if not tokens:
        return []

    counts = Counter(tokens)

    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    if not include_ties or len(sorted_items) <= top_n:
        return sorted_items[:top_n]

    cutoff_count = sorted_items[top_n - 1][1]
    result = sorted_items[:top_n]

    for word, count in sorted_items[top_n:]:
        if count == cutoff_count:
            result.append((word, count))
        else:
            break

    return result


def format_histogram(
    rows: list[tuple[str, int]], total_words: int | None = None
) -> str:

    if not rows:
        return ""

    lines = []
    for i, j in rows:
        if total_words and total_words > 0:
            porcentage = (j / total_words) * 100
            lines.append(f"{i:<15} {j:<5} {porcentage:.2f}%")
        else:
            lines.append(f"{i:<15} {j:<5}")

    return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    path = input("Full path to the text file: ").strip().strip('"')
    try:
        text = read_text_file(path)
        tokens = tokenize(text)
        print(format_histogram(histogram(text, 20), total_words=len(tokens)))
    except FileNotFoundError:
        print("file not found")
        exit()