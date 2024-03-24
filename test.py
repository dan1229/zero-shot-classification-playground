import time
from typing import Optional
from main import METHODS, classify_image


# This is structured as follows:
# {
#     "image-url": {
#         "method": {
#             "score": score,
#             "time": time_elapsed,
#             "category": category
#         }
#
#     }
# }
test_image_method_scores = {}

# test urls
TEST_URLS = [
    "https://www.dartmoorzoo.org.uk/wp-content/uploads/2021/01/Tiger-1.jpg",
    "https://media.newyorker.com/photos/62c4511e47222e61f46c2daa/4:3/w_2663,h_1997,c_limit/shouts-animals-watch-baby-hemingway.jpg",  # noqa
    "https://upload.wikimedia.org/wikipedia/commons/b/b0/Hamburger_%2812164386105%29.jpg",
    "https://www.iaea.org/sites/default/files/styles/original_image_size/public/str7803.jpg?itok=oYsZLbj9",
    "https://food.fnr.sndimg.com/content/dam/images/food/plus/fullset/2020/04/30/0/FNK_The-Best-Cheddar-And-Herb-Chaffle_H_s4x3.jpg.rend.hgtvcom.1280.720.suffix/1588257306685.jpeg",  # noqa
    "https://cdn.britannica.com/77/170477-050-1C747EE3/Laptop-computer.jpg",
    "https://cdn.britannica.com/94/152294-050-92FE0C83/Arabian-dromedary-camel.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Saturn_during_Equinox.jpg/800px-Saturn_during_Equinox.jpg",  # noqa
    "https://www.hertz.com/content/dam/hertz/global/blog-articles/ev/minivan-ev.jpg",
    "https://delivery.contenthub.allstate.com/api/public/content/a49111a4eda64870b2b52e7a28c5c167?v=841a0b55",
]


def _get_higest_scores(scores, num: Optional[int] = 3) -> list:
    highest_scores = []
    for obj in scores:
        highest_scores.append(obj["score"])
    return sorted(highest_scores)[:num]


if __name__ == "__main__":
    start_time = time.time()
    tests_run = 0
    shortest_time = float("inf")
    fastest_method = None

    try:
        # Loop through each test url
        for index, url in enumerate(TEST_URLS):
            print("\n** ===================================================== **")
            print(f"Test {index + 1}")
            print(f"Testing URL: {url}\n")

            # Loop through each method
            for method in METHODS:
                print(f"\n\tMethod: {method}")
                if method == "Specialized Categories":
                    print("\t\tSkipping method SPECIALIZED_CATEGORIES")
                    continue
                # Run classify_image function with the current method
                print(f"\tclassify_image({url}, {method})")
                scores, time_elapsed, category = classify_image(url, method)

                # Track scores and times for each method
                if url not in test_image_method_scores:
                    test_image_method_scores[url] = {}
                test_image_method_scores[url][method] = {
                    "scores": scores,
                    "time": time_elapsed,
                    "category": category,
                }
            tests_run += 1

        # Print overall stats
        print("\n=============================")
        print("\nOverall Stats:")
        for url, method_obj in test_image_method_scores.items():
            print(f"\nURL: {url}")
            for method, obj in method_obj.items():
                print(f"\tMethod: {method}")
                print(f"\t\tScore: {_get_higest_scores(obj['scores'])}")
                print(f"\t\tCategory: {obj['category']}")
                print(f"\t\tElapsed Time: {obj['time']} seconds")
                if obj["time"] < shortest_time:
                    shortest_time = obj["time"]
                    fastest_method = method
    except Exception as e:
        print("Error:", e)
    print("")
    print(f"\nFastest Method: {fastest_method}")
    print(f"\tElapsed Time: {shortest_time} seconds")
    print("Tests run:", tests_run)
    print("")
    print("Testing complete.")
    end_time = time.time()
    print("Total time elapsed:", end_time - start_time, "seconds")
