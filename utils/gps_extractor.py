import exifread
from PIL import Image
from PIL.ExifTags import TAGS
import io
from datetime import datetime

def extract_gps_from_image(image_path_or_bytes, return_dms=False):
    """
    Extract GPS coordinates from image EXIF data
    
    Args:
        image_path_or_bytes: Path to image file or bytes
        return_dms: If True, return coordinates in degrees/minutes/seconds format
    
    Returns:
        dict: GPS info or None if not found
    """
    try:
        # Handle both file path and bytes
        if isinstance(image_path_or_bytes, str):
            # File path
            with open(image_path_or_bytes, 'rb') as f:
                tags = exifread.process_file(f, stop_tag='EXIF DateTimeDigitized')
        else:
            # Bytes
            image = Image.open(io.BytesIO(image_path_or_bytes))
            exif_data = image._getexif()
            if not exif_data:
                return None
            
            # Convert PIL exif to exifread format
            tags = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                tags[tag] = value
        
        # Check for GPS info
        gps_info = {}
        
        # Latitude
        if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags:
            lat = _convert_to_degrees(tags['GPS GPSLatitude'], tags['GPS GPSLatitudeRef'])
            gps_info['lat'] = lat
        
        # Longitude  
        if 'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
            lon = _convert_to_degrees(tags['GPS GPSLongitude'], tags['GPS GPSLongitudeRef'])
            gps_info['lon'] = lon
        
        # Altitude
        if 'GPS GPSAltitude' in tags:
            alt = float(tags['GPS GPSAltitude'].values[0])
            if 'GPS GPSAltitudeRef' in tags and int(tags['GPS GPSAltitudeRef'].values[0]) == 1:
                alt = -alt  # Below sea level
            gps_info['alt'] = alt
        
        # Timestamp
        if 'EXIF DateTimeDigitized' in tags:
            timestamp_str = str(tags['EXIF DateTimeDigitized'])
            try:
                gps_info['timestamp'] = datetime.strptime(timestamp_str, '%Y:%m:%d %H:%M:%S').isoformat()
            except ValueError:
                pass
        
        # Direction
        if 'GPS GPSImgDirection' in tags:
            gps_info['direction'] = float(tags['GPS GPSImgDirection'].values[0])
        
        if gps_info:
            gps_info['valid'] = True
            if return_dms:
                gps_info['lat_dms'] = _degrees_to_dms(gps_info['lat'])
                gps_info['lon_dms'] = _degrees_to_dms(gps_info['lon'])
            return gps_info
        
        return None
        
    except Exception as e:
        print(f"Error extracting GPS: {e}")
        return None

def _convert_to_degrees(value, ref):
    """Convert GPS coordinates from EXIF format to degrees"""
    try:
        # EXIF GPS values are in format: degrees, minutes, seconds
        d, m, s = value.values
        
        # Convert to decimal degrees
        degrees = float(d.num) / float(d.den)
        minutes = float(m.num) / float(m.den) / 60.0
        seconds = float(s.num) / float(s.den) / 3600.0
        
        decimal_degrees = degrees + minutes + seconds
        
        # Apply reference direction
        if ref in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        
        return round(decimal_degrees, 6)
        
    except (AttributeError, ValueError, ZeroDivisionError):
        return None

def _degrees_to_dms(degrees):
    """Convert decimal degrees to degrees/minutes/seconds string"""
    is_negative = degrees < 0
    degrees = abs(degrees)
    
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = (degrees - d - m/60) * 3600
    
    direction = 'N' if not is_negative else 'S'
    if isinstance(degrees, (int, float)) and degrees > 90:  # Longitude check
        direction = 'E' if not is_negative else 'W'
    
    return f"{d:02d}° {m:02d}' {s:02.0f}\" {direction}"

def validate_coordinates(lat, lon):
    """Validate if coordinates are reasonable"""
    try:
        lat = float(lat)
        lon = float(lon)
        
        if not (-90 <= lat <= 90):
            return False, "Latitude must be between -90 and 90"
        if not (-180 <= lon <= 180):
            return False, "Longitude must be between -180 and 180"
        
        # Check if coordinates are in ocean (very basic check)
        # Most land coordinates have both lat and lon as integers or have specific patterns
        if abs(lat - round(lat)) < 0.001 and abs(lon - round(lon)) < 0.001:
            # Integer coordinates are suspicious for ocean sampling
            return False, "Coordinates appear to be on land (integer values)"
        
        return True, "Valid coordinates"
        
    except (ValueError, TypeError):
        return False, "Invalid coordinate format"

def estimate_location_description(lat, lon):
    """
    Generate a human-readable location description from coordinates
    (This is a simplified version - in production, use a geocoding API)
    """
    try:
        lat = float(lat)
        lon = float(lon)
        
        # Simple region classification
        if -60 <= lat <= -30:
            hemisphere = "Southern Hemisphere"
            ocean = "Southern Ocean"
        elif 30 <= lat <= 60:
            hemisphere = "Northern Hemisphere"
            ocean = "Northern Atlantic/Pacific"
        else:
            hemisphere = "Equatorial"
            ocean = "Tropical Waters"
        
        # Rough longitude-based description
        if -180 <= lon < -60:
            region = "Eastern Pacific"
        elif -60 <= lon < 0:
            region = "Western Atlantic"
        elif 0 <= lon < 60:
            region = "Eastern Atlantic/Mediterranean"
        elif 60 <= lon < 180:
            region = "Indian Ocean/Western Pacific"
        else:
            region = "Eastern Pacific"
        
        return f"{ocean}, {region}, {hemisphere} - Approx. {lat:.1f}°N, {lon:.1f}°E"
        
    except (ValueError, TypeError):
        return "Unknown location"

# Example usage and testing
if __name__ == "__main__":
    # Test with sample coordinates
    test_coords = [
        (40.7128, -74.0060),  # New York (land - should flag)
        (-33.8688, 151.2093), # Sydney (coastal)
        (21.3069, -157.8583), # Hawaii (ocean)
        (0.0000, 0.0000)      # Equator (ocean)
    ]
    
    print("Testing coordinate validation:")
    for lat, lon in test_coords:
        valid, message = validate_coordinates(lat, lon)
        status = "✅" if valid else "❌"
        print(f"{status} {lat}, {lon}: {message}")
        if valid:
            desc = estimate_location_description(lat, lon)
            print(f"   Description: {desc}")
    
    print("\nTesting GPS extraction (would need actual image file)...")