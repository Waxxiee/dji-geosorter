import json
from utils import file_handling


def main():
    # Fetch image data and reverse geocode results using the fetch_image_data function
    image_data_dump, reverse_geocode_results = file_handling.fetch_image_data()

    # Store the extracted image data in a JSON file using the store_exif_data function
    file_handling.store_exif_data(json.dumps(image_data_dump, default=str))

    new_folders = []  

    # Iterate through reverse geocode results to create new folders for each location
    for geocode_result in reverse_geocode_results:
        new_folders.append(file_handling.create_folder(geocode_result))

    # Iterate through locations and associated files to move files to their respective folders
    for location, files in reverse_geocode_results.items():
        for file in files:
            file_handling.move_file(location, file)



if __name__ == "__main":
    main()
