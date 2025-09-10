import random
import argparse

# English letter frequencies (source: Wikipedia, general English text)
# We use these as a base to invert from.
letter_frequencies = {
    'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 12.7, 'f': 2.2, 'g': 2.0,
    'h': 6.1, 'i': 7.0, 'j': 0.15, 'k': 0.77, 'l': 4.0, 'm': 2.4, 'n': 6.7,
    'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6.0, 's': 6.3, 't': 9.1, 'u': 2.8,
    'v': 0.98, 'w': 2.4, 'x': 0.15, 'y': 2.0, 'z': 0.074
}

# Assigning some estimated frequencies for numbers.
number_frequencies = {
    '1': 1.0, '2': 0.8, '3': 0.7, '4': 0.6, '5': 0.5,
    '6': 0.4, '7': 0.3, '8': 0.2, '9': 0.15, '0': 0.1
}

# Pessimistic guess for symbols. We want these to be highly represented.
symbol_base_weight = 3.0
symbols = "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?~`"
symbol_frequencies = {char: symbol_base_weight for char in symbols}


def get_inverted_weights():
    """
    Inverts the frequencies to create weights.
    Rare characters will get a higher weight, making them more likely to be chosen.
    """
    all_base_frequencies = {
        **letter_frequencies,
        **number_frequencies,
        **symbol_frequencies
    }

    # The core of the logic: invert the frequency to get the weight.
    inverted_weights = {char: 1.0 / (freq + 1e-9)
                        for char, freq in all_base_frequencies.items()}

    # Add capital letters, weighting them to be more common.
    capital_weights = {
        char.upper(): weight * 2.0
        for char, weight in inverted_weights.items()
        if char.isalpha()
    }

    final_weights = {**inverted_weights, **capital_weights}
    return final_weights


def generate_text(char_weights, length):
    """
    Generates a text of a given length, formatted into 8-character chunks
    separated by spaces to simulate words.
    """
    # Separate characters and their corresponding weights for random.choices
    characters = list(char_weights.keys())
    weights = list(char_weights.values())

    # Calculate how many 8-character "words" we need to generate.
    # Each word + space is 9 characters.
    num_words = (length // 9) + 2

    word_list = []
    for _ in range(num_words):
        # Generate one 8-character chunk
        chunk = "".join(random.choices(characters, weights=weights, k=8))
        word_list.append(chunk)

    # Join the words with spaces
    final_text = " ".join(word_list)

    # Trim the final text to the exact length requested
    return final_text[:length]


def main():
    """
    Main function to parse arguments and run the text generation.
    """
    parser = argparse.ArgumentParser(
        description="Generate a text file with a character distribution that oversamples underrepresented keys, formatted into 8-character chunks.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "filename",
        type=str,
        help="The name of the output file (e.g., 'training_data.txt')."
    )
    parser.add_argument(
        "length",
        type=int,
        help="The total number of characters to generate for the file."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducibility."
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print("Calculating character weights...")
    char_weights = get_inverted_weights()

    print(f"Generating {args.length} characters for '{args.filename}'...")
    text_content = generate_text(char_weights, args.length)

    try:
        with open(args.filename, "w", encoding="utf-8") as f:
            f.write(text_content)
        print(
            f"Successfully created '{args.filename}' with {len(text_content)} characters.")
    except IOError as e:
        print(f"Error: Could not write to file '{args.filename}'. Reason: {e}")


if __name__ == "__main__":
    main()
