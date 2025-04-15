import google.generativeai as genai
from PIL import Image
import os
import sys  # To access command-line arguments


def analyze_image_transactions(image_path):
    """
    Analyzes an image of handwritten transactions using Gemini API and
    returns a structured table of transaction details with added information.
    """

    genai.configure(api_key="AIzaSyD5GC5HIz3NgDW-8FVpdx7uZ71JqWC8hi4")
    model = genai.GenerativeModel('gemini-2.0-flash')

    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        return "Error: Image file not found at specified path."
    except Exception as e:
        return f"Error: Could not open or process image: {e}"

    prompt = f"""
    You are an expert financial assistant tasked with analyzing images of handwritten
    transaction lists.  Your goal is to extract all transaction details and present
    them in a structured, organized table format. ONLY RETURN THE TABLE. Analyze the image I provide and:

    1.  **Extract Transaction Details:** Identify and extract the following information
        for each transaction:
        *   Date (if present)
        *   Description (what was purchased or the reason for the transaction)
        *   Amount (the monetary value of the transaction)
        *   Category (e.g., Groceries, Utilities, Entertainment, Income, etc.  Infer
            this based on the description if not explicitly stated.)

    2.  **Create a Table:** Organize the extracted information into a table with the
        following columns:
        *   Date
        *   Description
        *   Amount
        *   Category
        *   Notes (if there is any description which is not related to the purchase reason)
    3.  **Enhance Data (Optional but highly encouraged):**
        *   If possible, infer additional information such as payment method or specific
            store.  Add this as a 'Notes' column in the table.
        *   If the image contains a running balance, include that information as well
            (e.g., "Starting Balance: [amount]", "Ending Balance: [amount]")

    4.  **Format and Structure:**
        *   Use clear and concise language.
        *   Make sure the table is well-formatted for readability.  Use markdown table format.
        *   Provide a short summary of the table.

    5. If you detect there are multiple currencies mentioned in the image create multiple tables based on the type of currencies mentioned. Add a title to the table for each currency.
    Be precise with the currencies and consider all possible currency types.

    Example table format:

    | Date       | Description       | Amount | Category    | Notes         |
    |------------|-------------------|--------|-------------|---------------|
    | 2024-10-26 | Coffee at Cafe X | $3.50  | Food & Drink | Paid with card |

    Now, analyze the image I provide.  Do your best to provide a complete and accurate
    analysis. Do not say any info or any other text. return only and only the table
    """

    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Error during Gemini API call: {e}"


def save_to_file(text, image_path):
    """Saves the analysis text to a file."""
    absolute_image_path = os.path.abspath(image_path)
    path_without_ext, _ = os.path.splitext(absolute_image_path)
    filename = path_without_ext + ".txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
        return f"Analysis saved to {filename}"
    except Exception as e:
        return f"Error saving to file: {e}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: DigiNote.py <image_filename>")
        sys.exit(1)

    image_path = sys.argv[1]
  

    analysis_result = analyze_image_transactions(image_path)
    # print(analysis_result)
    save_message = save_to_file(analysis_result, image_path)
    print(save_message)
    print("Process completed")