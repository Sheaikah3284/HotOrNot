import json


def generate_rankings():
    """
    Generates rankings based on the girls' ratings.

    Parameters:
        data (dict): The data dictionary containing girls' information and ratings.

    Returns:
        list: A list of dictionaries containing the ranked girls' information.

    Note:
        The rankings are based on the descending order of ratings. Ties are allowed.
    """
    with open("./girlsRatings.json", "r") as f:
        data = json.load(f)

        girls_list = data["List"]

        # Sort the girls based on ratings in descending order
        sorted_girls = sorted(
            girls_list, key=lambda x: x["ratings"], reverse=True)

        # Generate rankings
        rankings = []
        rank = 1
        for i, girl in enumerate(sorted_girls):
            ranking = {"rank": rank,
                       "name": girl["Name"] + " " + girl["LastName"], "rating": girl["ratings"]}
            rankings.append(ranking)

            # Check for ties in ratings
            if i < len(sorted_girls) - 1 and girl["ratings"] != sorted_girls[i + 1]["ratings"]:
                rank += 1

        return rankings
