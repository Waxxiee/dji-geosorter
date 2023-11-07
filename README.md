# dji-geosorter
GeoSorter: Organize your photos effortlessly! GeoSorter is a Python project that automates the sorting of your pictures into folders based on the location data found in their EXIF metadata.

# Configuration File
This section explains the key configuration variables used in your project. These variables are typically stored in a separate file, such as config.py, to keep sensitive information and settings separate from your code.
```
import os
from os import getenv

GOOGLE_MAPS_API_KEY = getenv("MAPS_API_KEY")
IMAGE_PREFIX = "dji"
IMAGE_EXCLUSION = "optimized"
IMAGE_FOLDER = os.path.expanduser("~\\Pictures")
IMAGE_TYPE = '.jpg'
DATA_FOLDER = os.path.join("data", "output.json")
TIME_THRESHOLD_MINUTES = 30
```
Variable Descriptions:

    GOOGLE_MAPS_API_KEY: Your Google Maps API key, fetched from the environment variable "MAPS_API_KEY." This key is used to access location data for geocoding.

    IMAGE_PREFIX: The prefix used to filter image files. Images with filenames starting with this prefix will be processed.

    IMAGE_EXCLUSION: A string used to exclude files from processing. Images with this string in their filenames will be excluded.

    IMAGE_FOLDER: The directory where your image files are located. By default, it points to the "Pictures" folder.

    IMAGE_TYPE: The file type for the images you want to process. This variable specifies the file extension (e.g., '.jpg').

    DATA_FOLDER: The path to the output JSON file where the extracted data will be stored.

    TIME_THRESHOLD_MINUTES: The time threshold in minutes. Images taken within this time frame will be grouped together based on location data.

Please make sure to set these variables in your config.py file, or customize them according to your specific project requirements. Keep your configuration file secure and do not share sensitive information like API keys in your public repository.
