__author__ = 'grainier'
from pyquery import PyQuery as pq


class ApplicationScraper(object):
    __user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'

    def __init__(self):
        pass

    def scrape(self, application_id, application_url):
        app_id = application_id
        app_url = application_url

        body_content = pq(
            app_url,
            headers={'User-Agent': self.__user_agent}
        )('#body-content')

        app_title = self.__get_app_title(body_content)                      # application title
        app_icon = self.__get_app_icon(body_content)                        # application thumbnail
        app_price = self.__get_app_price(body_content)                      # application price
        app_badges_count = self.__get_number_of_badges(body_content)        # number of badges like Top Developer
        app_description = self.__get_app_description(body_content)          # application description
        app_thumbnails = self.__get_app_thumbnails(body_content)            # application screen shots
        application_meta = self.__get_additional_information(body_content)  # application's additional information
        app_updated = application_meta['datePublished']
        app_installs = application_meta['numDownloads']
        app_size = application_meta['fileSize']
        app_version = application_meta['softwareVersion']
        app_os = application_meta['operatingSystems']
        app_content_rating = application_meta['contentRating']

        ## application rating value && count
        rating_data = self.__get_rating_information(body_content)
        app_rating_value = rating_data['ratingValue']
        app_rating_count = rating_data['ratingCount']

        ## make a application object
        application = {
            'id': app_id,
            'url': app_url,
            'title': app_title,
            'icon': app_icon,
            'badges': app_badges_count,
            'rating': app_rating_value,
            'rating_count': app_rating_count,
            'updated': app_updated,
            'installs': app_installs,
            'description': app_description,
            'price': app_price,
            'thumbnails': app_thumbnails,
            'size': app_size,
            'version': app_version,
            'os': app_os,
            'content_rating': app_content_rating
        }
        return application
        pass

    @staticmethod
    def __get_app_title(content):
        return content('.info-container .document-title').text()
        pass

    @staticmethod
    def __get_app_icon(content):
        return content('img.cover-image')[0].attrib['src']
        pass

    @staticmethod
    def __get_app_price(content):
        price = ''
        button_buy = content('button.price.buy')
        price_meta_data = button_buy('meta')
        for price_meta in price_meta_data:
            if price_meta.attrib['itemprop'] == 'price':
                price = price_meta.attrib['content']
                pass
            pass
        return price
        pass

    @staticmethod
    def __get_number_of_badges(content):
        special_badges = content('.header-star-badge .badge')
        return len(special_badges)
        pass

    @staticmethod
    def __get_app_description(content):
        description_content = content('.description .id-app-orig-desc')
        return description_content.html()
        pass

    @staticmethod
    def __get_app_thumbnails(content):
        thumbnails_urls = []
        thumbnails_soups = content('.thumbnails .screenshot')
        for thumbnail in thumbnails_soups:
            try:
                thumbnail_url = thumbnail.attrib['src']
                thumbnails_urls.append(thumbnail_url)
            except KeyError:
                pass
            pass
        return thumbnails_urls
        pass

    @staticmethod
    def __get_additional_information(content):
        additional_meta_map = {
            'datePublished': '',
            'numDownloads': '',
            'fileSize': '',
            'softwareVersion': '',
            'operatingSystems': '',
            'contentRating': ''
        }

        additional_information_soup = content('.details-section-contents')
        additional_meta_data_soups = additional_information_soup('.meta-info')
        for additional_meta_soup in additional_meta_data_soups:
            meta_content = additional_meta_data_soups(additional_meta_soup)('.content')
            try:
                item_property_key = meta_content[0].attrib['itemprop']
                if item_property_key == 'datePublished':
                    additional_meta_map['datePublished'] = meta_content.text()
                    pass
                elif item_property_key == 'numDownloads':
                    additional_meta_map['numDownloads'] = meta_content.text()
                    pass
                elif item_property_key == 'fileSize':
                    additional_meta_map['fileSize'] = meta_content.text()
                    pass
                elif item_property_key == 'softwareVersion':
                    additional_meta_map['softwareVersion'] = meta_content.text()
                    pass
                elif item_property_key == 'operatingSystems':
                    additional_meta_map['operatingSystems'] = meta_content.text()
                    pass
                elif item_property_key == 'contentRating':
                    additional_meta_map['contentRating'] = meta_content.text()
                    pass
                else:
                    pass
                pass
            except KeyError:
                ## there can be situations additional_meta_content don't have 'itemprop'
                pass
            pass
        return additional_meta_map
        pass

    @staticmethod
    def __get_rating_information(content):
        rating_data_map = {
            'ratingValue': '',
            'ratingCount': ''
        }
        rating_box = content('.rating-box .score-container')
        rating_meta_data = rating_box('meta')
        for rating_meta in rating_meta_data:
            try:
                item_property_key = rating_meta.attrib['itemprop']
                if item_property_key == 'ratingValue':
                    rating_data_map['ratingValue'] = rating_meta.attrib['content']
                    pass
                elif item_property_key == 'ratingCount':
                    rating_data_map['ratingCount'] = rating_meta.attrib['content']
                    pass
                pass
            except KeyError:
                ## there can be situations additional_meta_content don't have 'itemprop'
                pass
            pass
        return rating_data_map
        pass
    pass