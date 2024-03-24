import subprocess

from main import METHOD_SPECIALIZED_CATEGORIES, METHODS

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


# Function to parse the output and extract the score and elapsed time
def parse_output(output):
    lines = output.split("\n")
    score_line = [line for line in lines if "It is most likely a" in line]
    time_line = [line for line in lines if "Elapsed time:" in line]
    score = float(score_line[0].split(" ")[-1]) if score_line else None
    time_elapsed = float(time_line[0].split(" ")[-2]) if time_line else None
    return score, time_elapsed


if __name__ == "__main__":

    # Loop through each test url
    for url in TEST_URLS:
        print(f"\nTesting URL: {url}")

        # Loop through each method
        for method in METHODS:
            print(f"\tMethod: {method}")
            if method == METHOD_SPECIALIZED_CATEGORIES:
                print("\t\tSkipping method SPECIALIZED_CATEGORIES")
                continue
            # Run main.py with the current method
            print(f"\t\tpython main.py --method={method} --url={url}")
            process = subprocess.Popen(
                ["python", "main.py", f"--method={method}", f"--url={url}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            output, _ = process.communicate()

            # Parse the output to extract score and elapsed time
            score, time_elapsed = parse_output(output)

            # Extract category
            category_line = [line for line in output.split("\n") if "Category" in line]
            category = (
                category_line[0].split(":")[-1].strip() if category_line else None
            )

            # Track scores and times for each category
            if category:
                if category not in categories_scores:
                    categories_scores[category] = {}
                    categories_times[category] = {}
                categories_scores[category][method] = score
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
