import os
import shutil
import pytesseract
from PIL import Image

# Function to split sprite map and save images in the 'unassigned' folder


def split_sprite_map(sprite_map_path, output_directory):
    # Create the 'unassigned' directory
    unassigned_directory = os.path.join(output_directory, "unassigned")
    os.makedirs(unassigned_directory, exist_ok=True)

    # Load the sprite map image
    sprite_map = Image.open(sprite_map_path)

    # Calculate width and height of each sprite
    sprite_width = sprite_map.width // 8
    sprite_height = sprite_map.height // 7

    # Split the sprite map and save images in the 'unassigned' folder
    # Split the sprite map and save images in the 'unassigned' folder
    for row in range(7):
        for col in range(8):
            # Calculate the coordinates of the current sprite
            left = col * sprite_width
            upper = row * sprite_height
            right = left + sprite_width
            lower = upper + sprite_height

            # Crop the sprite from the sprite map
            RGB_sprite = sprite_map.crop((left, upper, right, lower))
            sprite = sprite_map.convert("L").crop((left, upper, right, lower))

            # Perform OCR to extract text from the sprite image
            extracted_text = pytesseract.image_to_string(sprite)
            # Remove the space and new line characters from the extracted text
            extracted_text = extracted_text.replace(" ", "").replace("\n", "")
            # Remove all non-alphanumeric characters from the extracted text
            extracted_text = "".join(
                char for char in extracted_text if char.isalnum())

            if extracted_text == "":
                # Display Image and get user input for name
                sprite.show()
                extracted_text = input("Enter the name: ")

            # check if first letter is uppercase
            if not extracted_text[0].isupper():
                # ask user to confirm if name is correct
                sprite.show()
                extracted_text = input(f"Is {extracted_text} correct? (y/n): ")
                if extracted_text.lower() == "n":
                    extracted_text = input("Enter the name: ")
                else:
                    extracted_text = extracted_text[0].capitalize()

            # Convert image back to RGB
            sprite = sprite.convert("RGB")

            # Save the sprite image in the 'unassigned' folder with the extracted text as the name
            output_path = os.path.join(
                unassigned_directory, f"{extracted_text}.png")
            RGB_sprite.save(output_path, "PNG")
            print(f"Saved {output_path}")

    print("Sprite map split and images saved successfully!")


# Function to display an image and get user input for gender assignment
def assign_gender(image_path):
    print(f"Image: {image_path}")
    image = Image.open(image_path)
    image.show()

    print("Please assign a gender:")
    print("1. Male")
    print("2. Female")

    while True:
        user_input = input(
            "Enter the gender number (1 for Male, 2 for Female): ")
        if user_input == "1":
            gender = "male"
            break
        elif user_input == "2":
            gender = "female"
            break
        else:
            print("Invalid input. Please enter 1 for Male or 2 for Female.")

    # Close the image after user input
    image.close()

    return gender


# Function to process unassigned photos and move them to the corresponding gender folder
def process_unassigned_photos(unassigned_directory):
    # Create the 'male' and 'female' directories
    male_directory = os.path.join(unassigned_directory, "male")
    female_directory = os.path.join(unassigned_directory, "female")
    os.makedirs(male_directory, exist_ok=True)
    os.makedirs(female_directory, exist_ok=True)

    # Get the list of unassigned photos
    unassigned_photos = os.listdir(unassigned_directory)

    # Process each unassigned photo
    for photo in unassigned_photos:
        photo_path = os.path.join(unassigned_directory, photo)

        # Skip directories
        if os.path.isdir(photo_path):
            continue

        # Display the photo and get user input for gender assignment
        gender = assign_gender(photo_path)

        # Move the photo to the corresponding gender folder
        output_directory = male_directory if gender == "male" else female_directory
        output_path = os.path.join(output_directory, photo)
        shutil.move(photo_path, output_path)
        print(f"Moved {photo} to {output_directory}")

        # Check if the file exists before deleting it
        if os.path.exists(photo_path):
            os.remove(photo_path)
            print(f"Deleted {photo}")
        else:
            print(f"Could not delete {photo}: File not found")

    print("All unassigned photos processed successfully!")


sprite_map_path_1 = "./IMG_1066.jpg"
sprite_map_path_2 = "./IMG_1067.jpg"
output_directory = "./photos"
21
maps = [
    "IMG_2644.png",
    "IMG_2645.png"
]

for map in maps:
    split_sprite_map(map, output_directory)
    unassigned_directory = os.path.join(output_directory, "unassigned")
    process_unassigned_photos(unassigned_directory)
