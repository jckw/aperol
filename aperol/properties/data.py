import requests
import urllib.parse


class BingMapsRoutes(object):
    base_url = 'https://dev.virtualearth.net/REST/v1/Routes/'

    def __init__(self, api_key):
        self.api_key = api_key

    def calculate_distance_matrix(self, origins, destinations,
                                  travel_mode='driving',
                                  distance_unit='kilometer'):
        url = urllib.parse.urljoin(self.base_url, 'DistanceMatrix')
        params = {
            "origins": self.strf_latlngs(origins),
            "destinations": self.strf_latlngs(destinations),
            "travelMode": travel_mode,
            "distanceUnit": distance_unit,
            "key": self.api_key
        }

        r = requests.get(url, params=params)

        if not r.ok:
            raise Exception(
                'Failed request: <{} {}> {}'.format(r.status_code, r.reason,
                                                    r.url))

        data = r.json()

        # Not sure when different resourceSets and resources are returned.
        return data["resourceSets"][0]["resources"][0]["results"]

    @staticmethod
    def strf_latlng(latlng):
        return "{},{}".format(*latlng)

    @staticmethod
    def strf_latlngs(latlngs):
        return ';'.join(map(BingMapsRoutes.strf_latlng, latlngs))

    def calculate_distance(self, origin, destination):
        return self.calculate_distance_matrix([origin], [destination])
