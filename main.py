from transformers import pipeline
from PIL import Image
import requests
import os
import argparse

# main.py
# example of a Zero Shot Image Classification pipeline with categories
# and labels from files

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


def get_labels_from_file(category="default"):
    file_path = os.path.join("labels", f"{category}.txt")
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def print_categories():
    print("\nAvailable categories:")
    for category in CATEGORIES:
        print(f"\t{category}")


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


def get_url_argument(args: argparse.Namespace) -> str:
    url = args.url
    if url is None:
        url = input("Enter the image URL: ")
    return url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-shot image classification")
    parser.add_argument(
        "--category", type=str, help="Category for image classification"
    )
    parser.add_argument("--url", type=str, help="URL of the image to classify")
    args = parser.parse_args()

    model_name = "openai/clip-vit-large-patch14-336"
    classifier = pipeline("zero-shot-image-classification", model=model_name)

    category = get_category_argument(args)
    url = get_url_argument(args)

    image_to_classify = Image.open(requests.get(url, stream=True).raw)

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
