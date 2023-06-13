import os
import shutil
from PIL import Image

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


# Example usage
unassigned_directory = "./photos/unassigned"
process_unassigned_photos(unassigned_directory)
