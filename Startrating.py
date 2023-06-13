""""
{
    "Name": "Kenna",
    "LastName": "Finlayson",
    "imgDir": "./photos/unassigned/female/KennaFinlayson.png",
    "rattings": "1400",
    "rank": "1"
}
"""

import os
import json

# create a loop through all images in ./photos/unassigned/female
girls = os.listdir("./photos/unassigned/female")

for photo in girls:
    photo = photo.split(".")[0]
    name = ""
    lastName = ""
    for i in range(len(photo)):
        if photo[i].isupper():
            if not i == 0:

                name = photo[:i]
                lastName = photo[i:]
                break

    # Link Json file
    with open("./girlsRatings.json", "r") as f:
        data = json.load(f)

        if not lastName == "":

            data["List"].append({
                "Name": name,
                "LastName": lastName,
                "imgDir": "photos/unassigned/female/" + photo + ".png",
                "ratings": 1000
            })

    with open("./girlsRatings.json", "w") as f:

        json.dump(data, f, indent=4)
