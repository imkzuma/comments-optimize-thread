import json

TEST_CASE: dict = {
    "id": 1,
    "score": 10,
    "children": [
        {"id": 2, "score": 5, "children": [
            {"id": 4, "score": -2, "children": []},
            {"id": 5, "score": 8, "children": []}
        ]},
        {"id": 3, "score": -3, "children": [
            {"id": 6, "score": 7, "children": []}
        ]}
    ]
}

EXPECTED_OUTPUT: list = [
    [1, 2, 5, 3, 6],
    [1, 2, 5],
    [1, 2, 4, 5],
    [1, 3, 6]
]

DATASET = "comments.json"  # Path to the dataset, replace with actual path
DEPTH_LIMIT = 2  # Maximum depth limit for comments, adjust as needed


def select_optimal_comments(thread: dict[str, any], depth_limit: int) -> list[int]:
    """
    Each comment in a thread has a unique `id`, a `score` (representing user engagement, e.g., likes minus dislikes), 
    and a list of `children` comments (nested comments). Your goal is to write a function that selects the optimal subset 
    of comments to display, maximizing the sum of their scores, while respecting the maximum allowed comment depth.

    1.  **Depth Limit (D):** The *selection process* must ensure that no comment at a depth exceeding `D` is included in the output.
    2.  **Parent-Child Dependency:** If a child comment is included in the displayed subset, its parent comment must also be included.
    3.  **Order Preservation:** The displayed comments must maintain their original order within the thread.

    params:
        thread: dict for representation thread for comments with tree
        depth_limit: depth limit 

    return:
        list of optimized id's
    """
    # create memoization for cache
    memo = {}

    def depth_search(comment: dict[str, any], depth: int) -> tuple[float, float, list[int], list[int]]:
        """
        calculating max score for every subtree in comments
        this function will calculate optimal score for every comments score

        params:
            comment: current comments object
            depth: current depth in thread

        returns:
            tuple:
            - incl_score 
            - excl_score
            - incl_ids 
            - excl_ids
        """
        # checking id in memoization
        cache_key = (comment["id"], depth)

        if cache_key in memo:
            return memo[cache_key]

        # if depth > dept_limit return []
        if depth > depth_limit:
            return float('-inf'), 0, [], []

        # initialization id and score
        incl_score = comment.get("score", 0)
        incl_ids = [comment["id"]]
        excl_score = 0
        excl_ids = []

        # processing comment children
        for child in comment.get("children", []):
            # recursive function to get score
            child_incl_score, child_excl_score, child_incl_ids, child_excl_ids = depth_search(
                child, depth + 1)

            # checking for every score and comments
            if child_incl_score > child_excl_score:
                incl_score += child_incl_score
                incl_ids.extend(child_incl_ids)

            else:
                incl_score += child_excl_score
                incl_ids.extend(child_excl_ids)

            excl_score += child_excl_score
            excl_ids.extend(child_excl_ids)

        # memoization for the result
        memo[cache_key] = (incl_score, excl_score, incl_ids, excl_ids)

        return incl_score, excl_score, incl_ids, excl_ids

    # calculating optimal solution with dept_search function
    incl_score, excl_score, incl_ids, excl_ids = depth_search(thread, 0)

    # Selecting id with current option
    # select id if incl_score >= excl_score
    # otherwise excl_ids
    selected_ids = incl_ids if incl_score >= excl_score else excl_ids

    # saving order id with pre-order traversal
    ordered_ids = []

    def collect_ordered_ids(comment: dict[str, any]) -> None:
        """
        Collect selected id from pre-order

        params:
            comment: current comments object
        """

        if comment["id"] in selected_ids:
            ordered_ids.append(comment["id"])

        for child in comment.get("children", []):
            collect_ordered_ids(child)

    collect_ordered_ids(thread)

    return ordered_ids


def using_test_case():
    '''
      Running the function using the test case given in the test
      **Expected Output:**
      [1, 2, 5, 3, 6] or 
      [1,2,5] or 
      [1,2,4,5] or 
      [1,3,6]
    '''
    result = select_optimal_comments(thread=TEST_CASE, depth_limit=2)

    for expected in EXPECTED_OUTPUT:
        if result == expected:
            print("Test Passed")
            print(result)
            break
    else:
        print("Test Failed")


def using_dataset():
    '''
      Load dataset 
    '''
    with open(DATASET, 'r') as file:
        comments_data = json.load(file)

    optimal_comments: list = select_optimal_comments(
        thread=comments_data, depth_limit=DEPTH_LIMIT)
    total_optimized_comments: int = len(optimal_comments)

    print(optimal_comments)
    print("Total comments selected:", total_optimized_comments)


if __name__ == "__main__":
    using_test_case()
    using_dataset()
