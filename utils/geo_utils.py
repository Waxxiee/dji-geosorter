import googlemaps
import config

gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY)


def reverse_geocode(longitude, latitude):
    """
    Perform reverse geocoding to retrieve location information for a given longitude and latitude.

    Parameters:
        longitude (list): A list containing longitude coordinate information.
        latitude (list): A list containing latitude coordinate information.

    Returns:
        dict: Location information obtained through reverse geocoding.
    """
    decimal_latitude = convert_coordinates_to_decimal(*latitude)
    decimal_longitude = convert_coordinates_to_decimal(*longitude)
    #Use GoogleMaps geocoding API to perform reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode(
        (decimal_longitude, decimal_latitude)
    )
    return reverse_geocode_result



def convert_coordinates_to_decimal(coordinate, direction):
    """
    Convert coordinate values in degrees, minutes, and seconds to decimal degrees.

    Parameters:
        coordinate (list): A list containing degrees, minutes, and seconds.
        direction (str): The direction (e.g., 'N', 'S', 'E', 'W') indicating the hemisphere.

    Returns:
        float: The decimal degree representation of the coordinate.
    """
    degrees, minutes, seconds = coordinate
    # Calculate the decimal degrees
    decimal_degrees = degrees + minutes / 60 + seconds / 3600

    # Adjust the sign based on the direction (North, South, East, West)
    if direction in ["S", "W"]:
        decimal_degrees = -decimal_degrees

    return float(decimal_degrees)

