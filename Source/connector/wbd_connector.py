import wbgapi as wb
import copy
import pandas


class Connector:
    def __init__(self):
        self.db = wb
        self.indicators = None
        self.countries = None
        self.regions = None

    def load_data(self):
        self.load_countries()
        self.load_regions()
        self.load_indicators()

    def load_indicators(self):
        self.indicators = list(wb.series.list())

    def find_indicator(self, indicator_description):
        matching_indicators = []
        for indicator in self.indicators:
            id = indicator['id']
            value = indicator['value']
            if indicator_description in value:
                matching_indicators.append({id, value})

        return matching_indicators

    def load_countries(self):
        economy_info = list(wb.economy.list())
        countries = {}
        for economy in economy_info:
            if not economy['aggregate']:
                country = economy['value']
                country_id = economy['id']
                country_region = economy['region']
                countries[country] = {'id': country_id,
                                      'region': country_region
                                      }
        self.countries = countries

    def load_regions(self):
        economy_info = list(wb.economy.list())
        regions = {}
        for economy in economy_info:
            if economy['aggregate']:
                region = economy['value']
                region_id = economy['id']
                regions[region] = {'id': region_id
                                   }
        self.regions = regions

    def get_regions(self):
        regions = copy.deepcopy(self.regions)
        return regions

    def get_countries(self):
        countries = copy.deepcopy(self.countries)
        return countries

    def get_countries_names(self):
        return [country for country in self.countries.keys()]

    def get_indicators(self):
        return self.indicators

    def get_country_id(self, country):
        if country in self.countries.keys():
            return self.countries[country]['id']
        return None

    def query_for_one_indicator(self, indicator, country):
        country_id = self.get_country_id(country)
        if country_id is not None:
            return self.db.data.DataFrame(indicator, country_id).loc[country_id]

    def query_for_two_indicators(self, indicator_a, indicator_b, country):
        country_id = self.get_country_id(country)
        if country_id is not None:
            dataframe = self.db.data.DataFrame([indicator_a, indicator_b], country_id)
            return dataframe.loc[indicator_a], dataframe.loc[indicator_b]







