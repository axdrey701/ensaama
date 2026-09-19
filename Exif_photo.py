from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def convert_gps_to_string(gps_info):
    """Convertit les données GPS en format 'XX.XXXX° N/S, YY.YYYY° E/O'."""
    if not gps_info:
        return None

    def convert_to_degrees(coord):
        d, m, s = coord
        return d + (m / 60.0) + (s / 3600.0)

    lat = gps_info.get('GPSLatitude')
    lat_ref = gps_info.get('GPSLatitudeRef', 'N')
    lon = gps_info.get('GPSLongitude')
    lon_ref = gps_info.get('GPSLongitudeRef', 'E')

    if not lat or not lon:
        return None

    lat_deg = convert_to_degrees(lat)
    lon_deg = convert_to_degrees(lon)

    return f"{lat_deg:.6f}° {lat_ref}, {lon_deg:.6f}° {lon_ref}"

def get_exif_data(image_path):
    # Ouvrir l'image
    image = Image.open(image_path)

    # Extraire les données EXIF brutes
    exif_data = image._getexif()

    # Dictionnaire pour stocker les données EXIF lisibles
    readable_exif = {}

    # Parcourir les balises EXIF et les convertir en format lisible
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        readable_exif[tag] = value

    # Extraire les coordonnées GPS si disponibles (en excluant les balises spécifiques)
    gps_info = {}
    if 'GPSInfo' in readable_exif:
        gps_data = readable_exif['GPSInfo']
        for tag_id, value in gps_data.items():
            gps_tag = GPSTAGS.get(tag_id, tag_id)
            # Exclure les balises non désirées
            if gps_tag not in [
                'GPSAltitude', 'GPSTimeStamp', 'GPSSpeedRef', 'GPSSpeed',
                'GPSImgDirectionRef', 'GPSImgDirection', 'GPSDestBearingRef',
                'GPSDestBearing', 'GPSDateStamp', 'GPSHPositioningError'
            ]:
                gps_info[gps_tag] = value

    # Extraire la date et l'heure
    date_time = readable_exif.get('DateTimeOriginal', None)

    # Retourner les données pertinentes
    return {
        "date_heure": date_time,
        "gps": convert_gps_to_string(gps_info)  # <-- Remplace `gps_info` par cette ligne
    }

# Exemple d'utilisation
image_path = "assets/photo0.jpg"
exif_data = get_exif_data(image_path)
print("Date et heure :", exif_data["date_heure"])
print("Coordonnées GPS :", exif_data["gps"])