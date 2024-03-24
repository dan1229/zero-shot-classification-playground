from main import METHODS, classify_image

categories_scores = {}
categories_times = {}

# test urls
TEST_URLS = [
    "https://www.dartmoorzoo.org.uk/wp-content/uploads/2021/01/Tiger-1.jpg",
    "https://media.newyorker.com/photos/62c4511e47222e61f46c2daa/4:3/w_2663,h_1997,c_limit/shouts-animals-watch-baby-hemingway.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/b/b0/Hamburger_%2812164386105%29.jpg",
    "https://www.iaea.org/sites/default/files/styles/original_image_size/public/str7803.jpg?itok=oYsZLbj9",
    "https://food.fnr.sndimg.com/content/dam/images/food/plus/fullset/2020/04/30/0/FNK_The-Best-Cheddar-And-Herb-Chaffle_H_s4x3.jpg.rend.hgtvcom.1280.720.suffix/1588257306685.jpeg",
]


if __name__ == "__main__":

    # Loop through each test url
    for index, url in enumerate(TEST_URLS):
        print("\n=============================")
        print(f"Test {index + 1}")
        print(f"Testing URL: {url}\n")

        # Loop through each method
        for method in METHODS:
            print(f"\tMethod: {method}")
            if method == "Specialized Categories":
                print("\t\tSkipping method SPECIALIZED_CATEGORIES")
                continue
            # Run classify_image function with the current method
            print(f"\t\tpython main.py --method={method} --url={url}")
            (scores, time_elapsed, category) = classify_image(url, method)

            # Track scores and times for each category
            if category:
                if category not in categories_scores:
                    categories_scores[category] = {}
                    categories_times[category] = {}
                categories_scores[category][method] = scores[0]["score"]
                categories_times[category][method] = time_elapsed

        # Find the highest score and elapsed time for each category
        for category, scores in categories_scores.items():
            print(f"\nCategory: {category}")
            max_score = max(scores.values())
            max_score_method = [
                method for method, score in scores.items() if score == max_score
            ]
            print(f"Highest Score: {max_score} (Method: {', '.join(max_score_method)})")
            print(
                f"Elapsed Time: {categories_times[category][max_score_method[0]]} seconds"
            )

    # Print overall stats
    print("\n=============================")
    print("\nOverall Stats:")
    for category, scores in categories_scores.items():
        max_score = max(scores.values())
        max_score_method = [
            method for method, score in scores.items() if score == max_score
        ]
        print(f"\nCategory: {category}")
        print(f"Highest Score: {max_score} (Method: {', '.join(max_score_method)})")
        print(
            f"Elapsed Time: {categories_times[category][max_score_method[0]]} seconds"
        )
