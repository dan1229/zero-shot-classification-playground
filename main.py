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


def get_category_argument(args: argparse.Namespace) -> str:
    category = args.category
    if category is None:
        print("Please choose a category for image classification:")
        print(CATEGORIES)
        category = input("Enter the category: ")
    while category not in CATEGORIES:
        print("Invalid category. Please choose from the following categories:")
        print(CATEGORIES)
        category = input("Enter the category: ")
    return category


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zero-shot image classification")
    parser.add_argument(
        "--category", type=str, help="Category for image classification"
    )
    args = parser.parse_args()

    model_name = "openai/clip-vit-large-patch14-336"
    classifier = pipeline("zero-shot-image-classification", model=model_name)

    url = "https://unsplash.com/photos/g8oS8-82DxI/download?ixid=MnwxMjA3fDB8MXx0b3BpY3x8SnBnNktpZGwtSGt8fHx8fDJ8fDE2NzgxMDYwODc&force=true&w=640"

    image_to_classify = Image.open(requests.get(url, stream=True).raw)

    category = get_category_argument(args)

    labels_for_classification = get_labels_from_file(category)

    scores = classifier(image_to_classify, candidate_labels=labels_for_classification)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("...")
    print("")
