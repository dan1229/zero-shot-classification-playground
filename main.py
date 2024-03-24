from transformers import pipeline
from PIL import Image
import requests
import os
import argparse

# Constants for categories
CATEGORY_DEFAULT = "default"
CATEGORY_ANIMALS = "animals"
CATEGORY_ART = "art"
CATEGORY_NATURE = "nature"
CATEGORY_PEOPLE = "people"
CATEGORY_TECH = "tech"
CATEGORY_TRANSPORT = "transport"
CATEGORY_FOOD = "food"
CATEGORY_OBJECTS = "objects"
CATEGORIES = [
    CATEGORY_DEFAULT,
    CATEGORY_ANIMALS,
    CATEGORY_ART,
    CATEGORY_NATURE,
    CATEGORY_PEOPLE,
    CATEGORY_TECH,
    CATEGORY_TRANSPORT,
    CATEGORY_FOOD,
    CATEGORY_OBJECTS,
]

# Constants for method
METHOD_SPECIALIZED_CATEGORIES = "Specialized Categories"
METHOD_ADD_DIFFERENT_CATEGORIES = "Add Different Categories"
METHOD_COMBINE_ALL_TEXT_FILES = "Combine All Text Files"
METHODS = [
    METHOD_SPECIALIZED_CATEGORIES,
    METHOD_ADD_DIFFERENT_CATEGORIES,
    METHOD_COMBINE_ALL_TEXT_FILES,
]


# Function to get labels from file based on category
def get_labels_from_file(category="default"):
    file_path = os.path.join("labels", f"{category}.txt")
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


#
# GET ARGUMENTS
#


# Function to print available categories
def print_categories():
    print("\nAvailable categories:")
    for category in CATEGORIES:
        print(f"\t{category}")


# Function to get category argument
def get_category_argument(args: argparse.Namespace) -> str:
    def _ask_for_category():
        print("\nPlease choose a category for image classification:")
        print_categories()
        return input("\nEnter the category: ")

    category = args.category
    if category is None:
        category = _ask_for_category()
    while category not in CATEGORIES:
        print("\nInvalid category. Please choose from the following categories:")
        category = _ask_for_category()
    return category


# Function to get URL argument
def get_url_argument(args: argparse.Namespace) -> str:
    url = args.url
    if url is None:
        url = input("Enter the image URL: ")
    return url


# Function to get method argument
def get_method(args: argparse.Namespace) -> str:
    method = args.method
    if method is None:
        print("\nAvailable methods:")
        for i, method_name in enumerate(METHODS, start=1):
            print(f"{i}. {method_name}")
        method_input = input("\nEnter the method name or number: ")
        try:
            method_index = int(method_input) - 1
            if method_index >= 0 and method_index < len(METHODS):
                method = METHODS[method_index]
            else:
                raise ValueError
        except ValueError:
            if method_input not in METHODS:
                print("\nInvalid method. Please choose from the available methods.")
                method = get_method(args)
    return method


#
# METHODS
#


# Method 1: Specialized Categories
def method_specialized_categories(image_to_classify: str, url: str):
    category = get_category_argument(args)

    labels_for_classification = get_labels_from_file(category)

    scores = classifier(image_to_classify, candidate_labels=labels_for_classification)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("...")
    print("")

    print(
        "It is most likely a", scores[0]["label"], "with a score of", scores[0]["score"]
    )


# Method 2: Processing Different Categories without User Input
def method_add_different_categories(image_to_classify: str, url: str):
    # Process each category and choose the one with the highest scores
    highest_score = -1
    highest_category = None
    for category in CATEGORIES:
        labels_for_classification = get_labels_from_file(category)
        scores = classifier(
            image_to_classify, candidate_labels=labels_for_classification
        )
        max_score_for_category = max(score["score"] for score in scores)
        if max_score_for_category > highest_score:
            highest_score = max_score_for_category
            highest_category = category

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    print("Processing without user input...")
    print("Most likely category:", highest_category, "with a score of", highest_score)
    print("")


# Method 3: Combine All Text Files and Use for Labels
def method_combine_all_text_files(image_to_classify: str, url: str):
    all_labels = []
    for category in CATEGORIES:
        labels_for_category = get_labels_from_file(category)
        all_labels.extend(labels_for_category)

    url = get_url_argument(args)
    image_to_classify = Image.open(requests.get(url, stream=True).raw)

    scores = classifier(image_to_classify, candidate_labels=all_labels)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("...")
    print("")
    print(
        "It is most likely a", scores[0]["label"], "with a score of", scores[0]["score"]
    )
    print("")


#
# MAIN
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-shot image classification")
    parser.add_argument("--method", type=int, help=f"Method of processing ({METHODS})")
    parser.add_argument("--url", type=str, help="URL of the image to classify")
    parser.add_argument(
        "--category",
        type=str,
        help=f"Category for specialized categories ({CATEGORIES})",
    )
    args = parser.parse_args()

    model_name = "openai/clip-vit-large-patch14-336"
    classifier = pipeline("zero-shot-image-classification", model=model_name)

    method = get_method(args)
    url = get_url_argument(args)
    image_to_classify = Image.open(requests.get(url, stream=True).raw)

    if method == METHOD_SPECIALIZED_CATEGORIES:
        method_specialized_categories(image_to_classify, url)
    elif method == METHOD_ADD_DIFFERENT_CATEGORIES:
        method_add_different_categories(image_to_classify, url)
    elif method == METHOD_COMBINE_ALL_TEXT_FILES:
        method_combine_all_text_files(image_to_classify, url)
    else:
        print(f"Invalid method selected. Please choose {METHODS}")
