from lxml import etree
_path_to_config = "config/startup_config.xml"


class ConfigReader:
    def __init__(self):
        with open(_path_to_config) as config:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(config, parser)
            root = tree.getroot()
            countries = [country.text for country in root.find("countries")]
            indicators = [{"id": indicator.findtext('id'),
                           "value": indicator.findtext('value')
                           } for indicator in root.find("indicators")]
            methods = [method.text for method in root.find("methods")]

        self.root = root
        self.countries = countries
        self.indicators = indicators
        self.methods = methods

    def add_countries(self, countries):
        for country in countries:
            self.add_country(country)

    def add_country(self, country_name):
        country_element = etree.Element("country")
        country_element.text = country_name

        countries_tag = self.root.find("countries")
        countries_tag.append(country_element)

    def add_indicators(self, indicators):
        for indicator in indicators:
            self.add_indicator(indicator)

    def add_indicator(self, indicator):
        indicator_element = etree.Element("indicator")

        indicator_id = etree.Element("id")
        indicator_name = etree.Element("value")

        indicator_id.text = indicator['id']
        indicator_name.text = indicator['value']

        indicator_element.append(indicator_id)
        indicator_element.append(indicator_name)

        indicator_tag = self.root.find("indicators")
        indicator_tag.append(indicator_element)

    def get_countries_from_config(self):
        return self.countries

    def get_indicators_from_config(self):
        return self.indicators

    def get_methods_from_config(self):
        return self.methods

    def save_config(self):
        et = etree.ElementTree(self.root)
        et.write(_path_to_config, pretty_print=True, xml_declaration=True, encoding="utf-8")