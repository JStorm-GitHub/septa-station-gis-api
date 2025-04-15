import xml.etree.ElementTree as ET
from shapely.geometry import Point, mapping
import geojson
from bs4 import BeautifulSoup

def create_db(kml_path, output_path="shared/storage/stations_parsed.geojson"):
    ns = {
        'kml': 'http://www.opengis.net/kml/2.2',
        'gx': 'http://www.google.com/kml/ext/2.2'
    }

    tree = ET.parse(kml_path)
    root = tree.getroot()
    features = []

    for placemark in root.findall(".//kml:Placemark", ns):
        name_elem = placemark.find("kml:name", ns)
        desc_elem = placemark.find("kml:description", ns)
        coord_elem = placemark.find(".//kml:Point/kml:coordinates", ns)

        name = name_elem.text if name_elem is not None else None
        description = desc_elem.text if desc_elem is not None else None
        coords_text = coord_elem.text.strip() if coord_elem is not None else None

        if coords_text:
            lon, lat, *_ = map(float, coords_text.split(","))
            point = Point(lon, lat)

            props = {"name": name}
            if description:
                soup = BeautifulSoup(description, "html.parser")
                for row in soup.find_all("tr"):
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        key = cells[0].get_text(strip=True)
                        val = cells[1].get_text(strip=True)
                        props[key] = val

            feature = geojson.Feature(
                geometry=mapping(point),
                properties=props
            )
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    with open(output_path, "w") as f:
        geojson.dump(feature_collection, f, indent=2)

    # print(f"Exported {len(features)} features to {output_path}")


# create_db("doc.kml", "stations_parsed.geojson")
