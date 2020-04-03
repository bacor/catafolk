from geopy.geocoders import Nominatim
import pandas as pd
import time
import os
import logging

CUR_DIR = os.path.dirname(__file__)
CACHE = os.path.join(CUR_DIR, 'location-cache.csv')
CORRECTIONS = os.path.join(CUR_DIR, 'location-corrections.csv')

class Locator(object):
    def __init__(self, sleep=1, cache=CACHE, corrections=CORRECTIONS):
        self.geolocator = Nominatim(user_agent="catafolk")
        self.cache = {}
        self.sleep = sleep
        self.cache_path = cache
        self.corrections_path = corrections
        self.load_cache()
    
    def coordinates(self, location, refresh=False):
        if refresh or location not in self.cache:
            result = self.lookup(location)
            if result == False:
                return (None, None)
        loc = self.cache[location]
        return loc['longitude'], loc['latitude']
        return (latitude, longitude)

    def lookup(self, location):
        # Temporarily disable
        return False

        loc = self.geolocator.geocode(location, exactly_one=True)
        self.cache[location] = {
            'location': location,
            'latitude': loc.latitude if loc is not None else None,
            'longitude': loc.longitude if loc is not None else None,
            'altitude': loc.altitude if loc is not None else None,
            # 'address': loc.address if loc is not None else None,
            # 'bbox': loc.raw.boundingbox if loc is not None else None
        }
        logging.info(f'Looked up {location}')
        time.sleep(self.sleep)
        return True
        
    def load_cache(self):
        cache = {}
        if os.path.exists(self.cache_path):
            cache_df = pd.read_csv(self.cache_path)
            cache_df.index = cache_df['location']
            cache = cache_df.T.to_dict()

        # Load corrections that override the cache
        if os.path.exists(self.corrections_path):
            corrections_df = pd.read_csv(self.corrections_path).set_index('location')
            for loc, (lat, long, alt) in corrections_df.iterrows():
                if loc not in cache:
                    cache[loc] = {}
                    cache[loc]['location'] = loc
                if not pd.isnull(lat):
                    cache[loc]['latitude'] = lat
                if not pd.isnull(long):
                    cache[loc]['longitude'] = long
                if not pd.isnull('altitude'):
                    cache[loc]['altitude'] = alt

        self.cache = cache    
    
    def save_cache(self):
        if len(self.cache) == 0:
            with open(self.cache_path, 'w') as handle:
                handle.write('location,latitude,longitude,altitude')
        else:
            df = pd.DataFrame(self.cache).T.set_index('location')
            df.sort_index(inplace=True)
            df.to_csv(self.cache_path)

    def clear_cache(self):
        self.cache = {}
        self.save_cache()

# if __name__ == '__main__':
#     L = Locator()
#     locations = ["175 5th Avenue NYC", "Amsterdam", "Amsterdam", "Paris", "Amsterdam"]
#     L.load_cache()
    
#     for loc in locations:
#         print(L.coordinates(loc))
#     L.clear_cache()
#     L.save_cache()

    
    # get_coordinates(locations)
    # print(location.address)
    # print(location)