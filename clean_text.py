import re
import argparse


def clean_text(input_file_path, output_file_path):
    """
    Cleans a text file from Project Gutenberg by standardizing quotes,
    normalizing whitespace, and removing the header/footer.

    Args:
        input_file_path (str): The path to the source text file.
        output_file_path (str): The path where the cleaned file will be saved.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # --- 1. Remove Project Gutenberg Header and Footer ---
    # Find the start of the actual content
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    start_index = full_text.find(start_marker)
    if start_index != -1:
        # Move past the marker line itself
        start_index = full_text.find('\n', start_index) + 1
        full_text = full_text[start_index:]

    # Find the end of the actual content
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    end_index = full_text.find(end_marker)
    if end_index != -1:
        full_text = full_text[:end_index]

    # --- 2. Standardize Quotation Marks and Other Characters ---
    # Dictionary of replacements
    replacements = {
        '“': '"', '”': '"',  # Smart double quotes to standard double quote
        '‘': "'", '’': "'",  # Smart single quotes to standard single quote
        '«': '"', '»': '"',  # Guillemets to standard double quote
        '—': '--',         # Em dash to double hyphen (common in plain text)
        '…': '...',        # Ellipsis character to three periods
    }

    for old, new in replacements.items():
        full_text = full_text.replace(old, new)

    # --- 3. Normalize Whitespace ---
    # Replace multiple newlines with a single newline
    # This helps preserve paragraph breaks while removing excessive spacing.
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', full_text)

    # Optional: Remove extra spaces within lines
    cleaned_text = re.sub(r' +', ' ', cleaned_text)

    # Trim leading/trailing whitespace from the whole text
    cleaned_text = cleaned_text.strip()

    # --- 4. Write the Cleaned Text to the Output File ---
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        print(
            f"✅ Successfully cleaned '{input_file_path}' and saved it to '{output_file_path}'")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")


if __name__ == "__main__":
    # --- Set up command-line argument parsing ---
    parser = argparse.ArgumentParser(
        description="Clean a Project Gutenberg text file for training.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="The path to the input text file.")
    parser.add_argument(
        "output_file", help="The path to save the cleaned output file.")

    args = parser.parse_args()

    # --- Run the cleaning function ---
    clean_text(args.input_file, args.output_file)
