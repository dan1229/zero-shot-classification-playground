from transformers import pipeline
from PIL import Image
import requests


DEFAULT_LABELS_FILE_PATH = "labels.txt"


def get_labels_from_file(file_path=DEFAULT_LABELS_FILE_PATH):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


if __name__ == "__main__":
    model_name = "openai/clip-vit-large-patch14-336"
    classifier = pipeline("zero-shot-image-classification", model=model_name)

    url = "https://unsplash.com/photos/g8oS8-82DxI/download?ixid=MnwxMjA3fDB8MXx0b3BpY3x8SnBnNktpZGwtSGt8fHx8fDJ8fDE2NzgxMDYwODc&force=true&w=640"

    image_to_classify = Image.open(requests.get(url, stream=True).raw)

    labels_for_classification = get_labels_from_file()

    scores = classifier(image_to_classify, candidate_labels=labels_for_classification)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores[:10]:
        print(f"{obj['label']}: {obj['score']}")
    print("...")
    print("")
