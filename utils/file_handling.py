import os
from PIL import Image
from PIL.ExifTags import TAGS
from config import (
    IMAGE_FOLDER,
    IMAGE_PREFIX,
    IMAGE_TYPE,
    DATA_FOLDER,
    TIME_THRESHOLD_MINUTES,
    IMAGE_EXCLUSION,
)
import utils.geo_utils as geo_utils
from datetime import datetime, timedelta
import json
import shutil


def extract_exif_data(file_name):
    """
    Extract EXIF data from an image file.

    Parameters:
        file_name (str): The path to the image file.

    Returns:
        dict: A dictionary containing extracted EXIF data.
    """
    extracted_exif_data = {}
    try:
        with Image.open(file_name) as image:
            exif_data = image._getexif()
            if exif_data:
                extracted_exif_data = {
                    TAGS.get(tag, tag): value
                    for tag, value in exif_data.items()
                    if TAGS.get(tag, tag)
                    not in ("XPComment", "XPKeywords", "BodySerialNumber", "MakerNote")  # Ignoring unused, long tags
                }
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        print("Error: Unable to open or read the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return extracted_exif_data



def create_folder(reverse_geocode_result):
    """
    Create a new folder with the specified name in the designated directory.

    Parameters:
        reverse_geocode_result (str): The name of the folder to create.

    Returns:
        tuple: A tuple containing the folder path and a message indicating the status.
    """
    try:
        pictures_directory = os.path.expanduser(IMAGE_FOLDER)  # IMAGE_FOLDER defined in the config
        new_folder_path = os.path.join(pictures_directory, reverse_geocode_result)

        os.makedirs(new_folder_path, exist_ok=True)
        return (
            new_folder_path,
            f"Folder '{reverse_geocode_result}' created in '{pictures_directory}'.",
        )
    except FileExistsError:
        return False, "Folder already exists."
    except Exception as e:
        print(e)  
        return False, str(e)  



def fetch_all_files(
    directory=IMAGE_FOLDER, prefix=IMAGE_PREFIX, file_type=IMAGE_TYPE, include_type=True
):
    """
    Fetch a list of image files in the specified directory.

    Parameters:
        directory (str): The directory path to search for image files (default: IMAGE_FOLDER).
        prefix (str): The filename prefix to filter images (default: IMAGE_PREFIX).
        file_type (str): The file extension to filter by (default: IMAGE_TYPE).
        include_type (bool): Whether to include the file type filter (default: True).

    Returns:
        tuple: A tuple containing a boolean indicating success and a list of image filenames.
    """
    if os.path.exists(directory) and os.path.isdir(directory):
        all_files = os.listdir(directory)
        jpg_files = [
            file
            for file in all_files
            if prefix in file
            and (not include_type or file.lower().endswith(file_type))
            and IMAGE_EXCLUSION not in file
        ]

        return True, jpg_files
    else:
        return (
            False,
            f"The directory '{directory}' does not exist or is not a valid directory.",
        )



def store_exif_data(exif_data):
    """
    Store EXIF data in a JSON file and return a status message.

    Parameters:
    exif_data (dict): The EXIF data to be stored in the JSON file.

    Returns:
        str: A message indicating the status of the operation.
    """
    json_file_path = DATA_FOLDER  # DATA_FOLDER defined in the config.
    try:
        with open(json_file_path, "w") as json_file:
            json.dump(exif_data, json_file, indent=4)
            return f"Exif data stored in {json_file_path}"
    except Exception as e:
        print(e)
        return str(e) 




def fetch_image_data():
    """
    Fetch image data, process it, and perform reverse geocoding.

    Returns:
        Tuple[list, dict]: A tuple containing a list of image data and a dictionary
        of reverse geocoding results.

    This function fetches image data, processes it, and performs reverse geocoding on images
    based on a time threshold. It returns a tuple containing image data and geocoding results.
    """
    result, files = fetch_all_files()  # Fetch a list from folder assigned in the config
    image_data_dump = []  # List to store image data
    image_date_times = []  # List to store image date and times
    reverse_geocode_results = {}  # Dictionary to store reverse geocoding results and images associated with a location

    for file in files:
        # Extract EXIF data from the image file
        image_data = extract_exif_data(f"{IMAGE_FOLDER}\\{file}")
        image_data["file_name"] = file

        # Parse the date and time from EXIF data
        image_date_time = datetime.strptime(image_data["DateTime"], "%Y:%m:%d %H:%M:%S")
        image_data["date"] = image_date_time
        image_date_times.append(image_date_time)
        image_data_dump.append(image_data)

        # Check if the time difference exceeds the threshold for geocoding (based on drone flight time)
        if len(image_date_times) == 1 or abs(
            image_date_time - image_date_times[0]
        ) > timedelta(minutes=TIME_THRESHOLD_MINUTES):
            longitude = [image_data["GPSInfo"][2], image_data["GPSInfo"].get(1, None)]
            latitude = [image_data["GPSInfo"][4], image_data["GPSInfo"].get(3, None)]
            geocode_result = geo_utils.reverse_geocode(longitude, latitude)
            location = geocode_result[0]["formatted_address"]
            removal_characters = f"{geocode_result[0]['address_components'][0]['long_name']} "
            if location.replace(removal_characters, "") not in reverse_geocode_results:
                reverse_geocode_results[(location.replace(removal_characters, ""))] = []

        last_location = list(reverse_geocode_results.keys())[-1]
        reverse_geocode_results[last_location].append(file)

    return image_data_dump, reverse_geocode_results



def move_file(destination_folder, file_name):
    """
    Move a file to a specified destination folder.

    Parameters:
        destination_folder (str): The folder where the file will be moved.
        file_name (str): The name of the file to be moved.

    Returns:
        str: A message indicating the status of the operation.
    """
    try:
        pictures_directory = os.path.expanduser(IMAGE_FOLDER)  # IMAGE_FOLDER defined in config.
        current_file_directory = os.path.join(pictures_directory, file_name)
        destination_file_directory = os.path.join(pictures_directory, destination_folder, file_name)
        shutil.move(current_file_directory, destination_file_directory)
        return f"Moved {file_name} to {destination_folder}"
    except Exception as e:
        print(e) 
        return str(e)  

