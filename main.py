from typing import Optional
from transformers import pipeline
from PIL import Image
import requests
import os
import argparse
import time

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
METHOD_USE_CATEGORY_NAMES = "Use Category Names"
METHODS = [
    METHOD_SPECIALIZED_CATEGORIES,
    METHOD_ADD_DIFFERENT_CATEGORIES,
    METHOD_COMBINE_ALL_TEXT_FILES,
    METHOD_USE_CATEGORY_NAMES,
]

# Classifier pipeline
model_name = "openai/clip-vit-large-patch14-336"
classifier = pipeline("zero-shot-image-classification", model=model_name)


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
    if method is not None:
        method_input = method
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
        else:
            method = method_input
    return method


#
# METHODS
#


# Method 1: Specialized Categories
def method_specialized_categories(image_to_classify: str, url: str) -> list:
    category = get_category_argument(args)
    labels_for_classification = get_labels_from_file(category)

    print(f"Evaluating {len(labels_for_classification)} labels.")

    scores = classifier(image_to_classify, candidate_labels=labels_for_classification)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("...")

    print(
        "It is most likely a", scores[0]["label"], "with a score of", scores[0]["score"]
    )

    return scores


# Method 2: Processing Different Categories without User Input
def method_add_different_categories(image_to_classify: str, url: str) -> list:
    print("\nProcessing different categories without user input...")
    total_labels = 0
    # Process each category and choose the ones with the highest scores
    top_scores = []
    for category in CATEGORIES:
        print(f"\tProcessing category: {category}")
        labels_for_classification = get_labels_from_file(category)
        total_labels += len(labels_for_classification)
        scores = classifier(
            image_to_classify, candidate_labels=labels_for_classification
        )
        top_scores.extend(scores[:10])

    print(f"Evaluating {total_labels} labels.")

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    print("Processing without user input...")
    print("Top 10 scores:")
    for obj in top_scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("")

    return top_scores


# Method 3: Combine All Text Files and Use for Labels
def method_combine_all_text_files(image_to_classify: str, url: str) -> list:
    all_labels = []
    for category in CATEGORIES:
        labels_for_category = get_labels_from_file(category)
        all_labels.extend(labels_for_category)

    total_labels = len(all_labels)
    image_to_classify = Image.open(requests.get(url, stream=True).raw)

    scores = classifier(image_to_classify, candidate_labels=all_labels)

    print(f"Evaluating {total_labels} labels.")

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("...")

    print(
        "It is most likely a", scores[0]["label"], "with a score of", scores[0]["score"]
    )
    print("")

    return scores


# Method 4: Use Category Names as Labels and Refine with X Scored Labels
def method_use_category_names(image_to_classify: str, url: str) -> list:
    threshold_score = 0.2  # Example threshold score, adjust as needed

    category_names = [category.lower() for category in CATEGORIES]

    scores = classifier(image_to_classify, candidate_labels=category_names)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    print("Evaluating category names...")
    print("Category names:")
    for obj in scores:
        print(f"\t{obj['label']}: {obj['score']}")
    print("\nRefining labels...")

    refined_labels = []
    for obj in scores:
        if obj["score"] >= threshold_score:
            category = obj["label"]
            labels_for_category = get_labels_from_file(category)
            refined_labels.extend(labels_for_category)

    print(
        f"Evaluating {len(refined_labels)} refined labels with score >= {threshold_score}."
    )

    scores = classifier(image_to_classify, candidate_labels=refined_labels)

    print("\nTop predictions after refinement:")
    for obj in scores[:10]:
        print(f"\t{obj['label']}: {obj['score']}")
    print("...")
    print("")

    return scores


#
# MAIN
#
def classify_image(
    url: str, method: Optional[str] = None, category: Optional[str] = None
) -> tuple[list, float, str]:
    def _handle_return(scores, category):
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("\n=============================")
        print("Classification complete.")
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"URL: {url}")
        print("=============================\n")
        return (scores, elapsed_time, category)

    if method is None:
        method = get_method(None)
    if category is None and method == METHOD_SPECIALIZED_CATEGORIES:
        category = get_category_argument(None)

    start_time = time.time()

    try:
        image_to_classify = Image.open(requests.get(url, stream=True).raw)
    except Exception as e:
        print(f"Error opening image from URL: {url}")
        print(e)
        return _handle_return([], category)

    if method == METHOD_SPECIALIZED_CATEGORIES:
        scores = method_specialized_categories(image_to_classify, url)
    elif method == METHOD_ADD_DIFFERENT_CATEGORIES:
        scores = method_add_different_categories(image_to_classify, url)
    elif method == METHOD_COMBINE_ALL_TEXT_FILES:
        scores = method_combine_all_text_files(image_to_classify, url)
    elif method == METHOD_USE_CATEGORY_NAMES:
        scores = method_use_category_names(image_to_classify, url)
    else:
        print(f"\nInvalid method selected - {method}\n\nPlease choose {METHODS}\n")

    return _handle_return(scores, category)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-shot image classification")
    parser.add_argument(
        "--method", type=str, help=f"Method of processing ({', '.join(METHODS)})"
    )
    parser.add_argument("--url", type=str, help="URL of the image to classify")
    parser.add_argument(
        "--category",
        type=str,
        help=f"Category for specialized categories ({', '.join(CATEGORIES)})",
    )
    args = parser.parse_args()

    classify_image(args.url, args.method, args.category)
