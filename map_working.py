import requests
import sys

geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


class MapParams:
    def __init__(self):
        self.lat = 55.702999
        self.lon = 37.530883
        self.cur_lat = 55.702999
        self.cur_lon = 37.530883
        self.zoom = 16
        self.type = "map"
        self.step = 0.002

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    def ll_cur(self):
        return str(self.cur_lon) + "," + str(self.cur_lat)


def load_map(mp):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.zoom}&l={mp.type}&pt={mp.ll_cur()},{'pmgnm'}"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def geocode(address):
    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"
    }

    response = requests.get(geocoder_request, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {response.url}
            Http статус: {response.status_code} ({response.reason})
            """
        )

    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_coordinates(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coordinates.split()
    return float(toponym_longitude), float(toponym_latitude)


# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((600, 450))
#     mp = MapParams()
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             elif event.type == pygame.KEYDOWN:
#                 mp.update(event)
#         map_file = load_map(mp)
#         screen.blit(pygame.image.load(map_file), (0, 0))
#         pygame.display.flip()
#     pygame.quit()
#
#
# if __name__ == "__main__":
#     main()
