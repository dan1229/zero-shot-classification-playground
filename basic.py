from transformers import pipeline
from PIL import Image
import requests

# basic.py
# Just an example for a basic Zero Shot Image Classification pipeline

if __name__ == "__main__":
    model_name = "openai/clip-vit-large-patch14-336"
    classifier = pipeline("zero-shot-image-classification", model=model_name)

    url = "https://unsplash.com/photos/g8oS8-82DxI/download?ixid=MnwxMjA3fDB8MXx0b3BpY3x8SnBnNktpZGwtSGt8fHx8fDJ8fDE2NzgxMDYwODc&force=true&w=640"

    image_to_classify = Image.open(requests.get(url, stream=True).raw)

    labels_for_classification = ["owl", "bird", "cat", "dog", "car"]

    scores = classifier(image_to_classify, candidate_labels=labels_for_classification)

    print("\n=============================")
    print(f"Image URL:\n{url}\n")
    for obj in scores:
        print(f"{obj['label']}: {obj['score']}")
    print("")
