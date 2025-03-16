from flask import json
import pandas as pd
import re
import google.generativeai as genai
import base64
from PIL import Image

# Set your Gemini API Key
genai.configure(api_key="AIzaSyAC-nkgnUKBNtE3qjVNN-3ORC9gpHn6XU4")

def crop_image(image_path):
    """Crop everything below the color boxes (assume they take up ~70 pixels)."""
    image = Image.open(image_path)
    cropped_image = image.crop((0, 70, image.width, image.height))  # Crop from (left, top, right, bottom)
    
    # cropped_path = "C:/Users/lenovo/Desktop/cropped_paint_output.png"
    cropped_path = "static/drawing.png" 
    cropped_image.save(cropped_path)
    return cropped_path

def encode_image(image_path):
    """Convert image to Base64 format."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def extract_text_from_image(image_path):
    """Extract text from an image using Gemini API."""
    cropped_image_path = crop_image(image_path)  # Apply cropping
    image_data = encode_image(cropped_image_path)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        response = model.generate_content(
            [{"mime_type": "image/png", "data": image_data},"Just tell what object is image trying to convey hich can be bought from shopping store,  and main text and any shape or object ,No explanations, just the object name ."], 
            generation_config={"max_output_tokens": 7}
        )
        return response.text.strip() if response.text else ""  # Ensure we return clean text
    except Exception as e:
        print("Error extracting text:", e)
        return ""

def clean_keywords(text):
    """Remove stopwords and extract meaningful words."""
    stopwords = {
        "the", "a", "an", "and", "is", "it", "this", "that", "of", "to", "be", "as",
        "shows", "below", "could", "word", "written", "interpreted", "image", "in",
        "on", "for", "with", "at", "by", "from", "about", "which", "who", "whom",
        "whose", "what", "when", "where", "why", "how", "was", "were", "are", "has",
        "have", "had", "do", "does", "did", "will", "shall", "should", "would",
        "can", "could", "may", "might", "must", "if", "then", "than", "also",
        "yet", "but", "or", "so", "very", "just", "only", "even", "much", "such",
        "some", "any", "all", "many", "most", "more", "less", "other", "another",
        "each", "every", "either", "neither", "own", "same", "different", "new"
    }

    words = re.findall(r'\b\w+\b', text.lower())  # Extract words
    return {word for word in words if word not in stopwords}  # Use a set for fast lookup

def count_keyword_matches(description, keywords):
    """Count how many unique keywords appear in a product description."""
    description_words = set(str(description).lower().split())  # Convert description to a set
    return sum(1 for word in keywords if word in description_words)

# def search_product(keyword, dataset_path="D:/KioskInk/Online Retail.csv"):
#     """Search for products based on extracted keywords."""
#     df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
#     print(keyword)
#     keywords = clean_keywords(keyword)
#     print(keywords)
#     if not keywords:
#         return pd.DataFrame(columns=['StockCode', 'Description', 'Quantity', 'UnitPrice'])  # Empty result

#     # Step 1: Exact Match (Products with all keywords)
#     df["MatchCount"] = df["Description"].apply(lambda x: count_keyword_matches(x, keywords))
#     exact_match = df[df["MatchCount"] == len(keywords)].head(5)

#     if not exact_match.empty:
#         return exact_match[['StockCode', 'Description', 'Quantity', 'UnitPrice']]

#     # Step 2: Get at least 3 products for each keyword separately
#     results = []
#     for word in keywords:
#         word_matches = df[df["Description"].str.contains(word, case=False, na=False)].head(3)  # Force 3 per word
#         results.append(word_matches)

#     partial_matches = pd.concat(results).drop_duplicates().head(5)

#     return partial_matches[['StockCode', 'Description', 'Quantity', 'UnitPrice']]
# def search_product(keyword, dataset_path="D:/KioskInk/my_data.csv"):
#     """Search for products based on extracted keywords."""
#     df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
    
#     keywords = clean_keywords(keyword)
#     if not keywords:
#         output_data = { "products": []}  # Return an empty list instead of an empty DataFrame

#     # Step 1: Exact Match (Products with all keywords)
#     df["MatchCount"] = df["Description"].apply(lambda x: count_keyword_matches(x, keywords))
#     exact_match = df[df["MatchCount"] == len(keywords)].head(5)

#     if not exact_match.empty:
#         xx= exact_match[['StockCode', 'Description', 'Quantity', 'UnitPrice']].to_dict(orient="records")

#     # Step 2: Get at least 3 products for each keyword separately
#     results = []
#     for word in keywords:
#         word_matches = df[df["Description"].str.contains(word, case=False, na=False)].head(3)  
#         results.append(word_matches)

#     partial_matches = pd.concat(results).drop_duplicates().head(5)

#     xx= partial_matches[['StockCode', 'Description', 'Quantity', 'UnitPrice']].to_dict(orient="records")
#     output_data = {"products": xx}
# # Example Usage
# # image_path = "C:/Users/lenovo/Desktop/paint_output.png"
# image_path = "static/drawing.png"    # Make sure this file exists
# extracted_text = extract_text_from_image(image_path)

# with open("output.json", "w") as f:
#     json.dump(output_data, f, indent=4)
# if extracted_text:
#     top_products = search_product(extracted_text)
#     print(top_products)
# else:
#     print("No text found in the image.")
def search_product(keyword, dataset_path="D:/KioskInk/my_data.csv"):
    """Search for products based on extracted keywords."""
    df = pd.read_csv(dataset_path, encoding="ISO-8859-1")
    
    keywords = clean_keywords(keyword)
    output_data = {"products": []}  # Ensure it's always initialized

    if not keywords:
        return output_data  # Return empty JSON if no keywords found

    # Step 1: Exact Match (Products with all keywords)
    df["MatchCount"] = df["Description"].apply(lambda x: count_keyword_matches(x, keywords))
    exact_match = df[df["MatchCount"] == len(keywords)].head(5)

    if not exact_match.empty:
        xx = exact_match[['StockCode', 'Description', 'Quantity', 'UnitPrice']].to_dict(orient="records")
        output_data = {"products": xx}
        return output_data  # Return early if exact match found

    # Step 2: Get at least 3 products for each keyword separately
    results = []
    for word in keywords:
        word_matches = df[df["Description"].str.contains(word, case=False, na=False)].head(10)  
        results.append(word_matches)

    if results:  # Ensure we don't concat empty results
        partial_matches = pd.concat(results).drop_duplicates().head(10)
        xx = partial_matches[['StockCode', 'Description', 'Quantity', 'UnitPrice']].to_dict(orient="records")
        output_data = {"products": xx}

    return output_data  # Always return valid JSON

# Example Usage
image_path = "static/drawing.png"  # Ensure this file exists
extracted_text = extract_text_from_image(image_path)

if extracted_text:
    top_products = search_product(extracted_text)

    # Save results to output.json
    with open("output.json", "w") as f:
        json.dump(top_products, f, indent=4)

    print(top_products)  # Print for debugging
else:
    print("No text found in the image.")