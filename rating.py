
import json
import random
from PIL import Image
import base64


def select_girls_to_compare(data):
    """
    Selects two girls to compare based on their ratings.

    Parameters:
        data (dict): The data dictionary containing girls' information and ratings.

    Returns:
        tuple: A tuple containing the indices of the two selected girls.

    Raises:
        IndexError: If the data list is empty or contains only one girl.

    Note:
        The selection is based on finding two girls with similar ratings within a range of 200.
    """

    girls_list = data["List"]

    if len(girls_list) < 2:
        raise IndexError("Insufficient number of girls for comparison.")

    girl1_index = random.randint(0, len(girls_list) - 1)
    girl1_rating = girls_list[girl1_index]["ratings"]

    # Find another girl with a rating within the range of 200
    remaining_indices = [i for i in range(len(girls_list)) if i != girl1_index]
    valid_indices = []

    for index in remaining_indices:
        rating_diff = abs(girls_list[index]["ratings"] - girl1_rating)
        if rating_diff <= 200:
            valid_indices.append(index)

    if len(valid_indices) == 0:
        raise IndexError("No girl found within the desired rating range.")

    girl2_index = random.choice(valid_indices)

    return girl1_index, girl2_index


def startRating():
    """
    Generates initial data for the rating comparison.

    Returns:
        dict: A dictionary containing information about two girls and their images in base64 format.

    Example:
        rating_data = startRating()
        girl1_name = rating_data["girl1Name"]
        girl1_image = rating_data["girl1Img"]
        girl2_name = rating_data["girl2Name"]
        girl2_image = rating_data["girl2Img"]
    """

    with open("./girlsRatings.json", "r") as f:
        data = json.load(f)

        # Select two girls to compare
        girl1_index, girl2_index = select_girls_to_compare(data)

        girl1 = data["List"][girl1_index]
        girl2 = data["List"][girl2_index]
        girl1Name = girl1["Name"] + " " + girl1["LastName"]
        girl2Name = girl2["Name"] + " " + girl2["LastName"]

        # Convert girl1's image to base64
        with open(girl1["imgDir"], 'rb') as img_file:
            img1_base64 = base64.b64encode(img_file.read()).decode("utf-8")
            img1_base64 = "data:image/png;base64," + img1_base64

        # Convert girl2's image to base64
        with open(girl2["imgDir"], 'rb') as img_file:
            img2_base64 = base64.b64encode(img_file.read()).decode("utf-8")
            img2_base64 = "data:image/png;base64," + img2_base64

        return {
            "girl1Name": girl1Name,
            "girl2Name": girl2Name,
            "girl1Img": img1_base64,
            "girl2Img": img2_base64,
            "girl1ID": girl1_index,
            "girl2ID": girl2_index
        }


def get_expected_probability(rating1, rating2):
    """
    Calculate the expected probability of winning for two players based on their ratings.

    Parameters:
        rating1 (float): Rating of player 1.
        rating2 (float): Rating of player 2.

    Returns:
        float: The expected probability of winning for player 1.
    """
    return 1 / (1 + 10 ** ((rating2 - rating1) / 400))


def rate(winner, loser):
    """
    Updates the ratings of two girls based on the outcome of a comparison.

    Parameters:
        winner (int): The index of the girl who won the comparison.
        loser (int): The index of the girl who lost the comparison.

    Raises:
        IndexError: If the indices are out of range.

    Note:
        The function updates the "ratings" attribute of the girls in the data list.

    Example:
        rate(0, 1)  # Updates the ratings of the girl at index 0 and the girl at index 1, with girl at index 0 being the winner.
    """

    with open("./girlsRatings.json", "r") as f:
        data = json.load(f)

        # Check if the indices are within the valid range
        if winner < 0 or winner >= len(data["List"]) or loser < 0 or loser >= len(data["List"]):
            raise IndexError("Invalid indices.")

        winner_girl = data["List"][winner]
        loser_girl = data["List"][loser]

        # Initial ratings
        winner_rating = winner_girl["ratings"]
        loser_rating = loser_girl["ratings"]

        k_factor = 32  # The K-factor determines how much ratings are adjusted after each comparison

        winner_expected = get_expected_probability(loser_rating, winner_rating)
        loser_expected = 1 - winner_expected

        # print who is expected to win

        # Update ratings using the Elo rating formula
        winner_rating = winner_rating + k_factor * (1 - winner_expected)
        loser_rating = loser_rating + k_factor * (0 - loser_expected)

        data["List"][winner]["ratings"] = winner_rating
        data["List"][loser]["ratings"] = loser_rating

        # Update the JSON file
        with open("./girlsRatings.json", "w") as f:
            json.dump(data, f, indent=4)

        return winner_rating, loser_rating
