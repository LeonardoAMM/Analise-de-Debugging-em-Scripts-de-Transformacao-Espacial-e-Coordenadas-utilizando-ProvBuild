from pyproj import Transformer


def convert_coordinates(latitude, longitude):      # Converte sistema de latitude/longitude para sistema de metros/plano cartesiano

    transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:32723",
        always_xy=True
    )

    x, y = transformer.transform(longitude, latitude)

    return x, y