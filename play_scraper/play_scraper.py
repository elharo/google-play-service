__author__ = 'grainier'

from pyquery import PyQuery as pq
import redis
import pickle

scraped_applications = []
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
set_key = 'set_priority_x'
r_server = redis.Redis("localhost")
application_keys = r_server.smembers(set_key)


def get_app_title(content):
    return content('.info-container .document-title').text()
    pass


def get_app_icon(content):
    return content('img.cover-image')[0].attrib['src']
    pass


def get_app_price(content):
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


def get_number_of_badges(content):
    special_badges = content('.header-star-badge .badge')
    return len(special_badges)
    pass


def get_app_description(content):
    description_content = content('.description .id-app-orig-desc')
    return description_content.html()
    pass


def get_app_thumbnails(content):
    thumbnails_urls = []
    thumbnails_soups = body_content('.thumbnails .screenshot')
    for thumbnail in thumbnails_soups:
        try:
            thumbnail_url = thumbnail.attrib['src']
            thumbnails_urls.append(thumbnail_url)
        except KeyError:
            pass
        pass
    return thumbnails_urls
    pass


for application_key in application_keys:
    serialized_application_raw_data = r_server.get(application_key)
    application_raw_data = pickle.loads(serialized_application_raw_data)

    app_id = application_raw_data['app_id']
    app_url = application_raw_data['app_url']

    application_soup = pq(
        app_url,
        headers={'User-Agent': user_agent}
    )

    body_content = application_soup('#body-content')

    ## application title
    app_title = get_app_title(body_content)

    ## application thumbnail
    app_icon = get_app_icon(body_content)

    ## application price
    app_price = get_app_price(body_content)

    ## number of badges like Top Developer, Editors Choice
    app_badges_count = get_number_of_badges(body_content)

    ## application description
    app_description = get_app_description(body_content)

    ## application screen shots
    app_thumbnails = get_app_thumbnails(body_content)

    ## application rating value && count
    rating_box = body_content('.rating-box .score-container')
    rating_meta_data = rating_box('meta')
    app_rating_value = ''
    app_rating_count = ''
    for rating_meta in rating_meta_data:
        try:
            if rating_meta.attrib['itemprop'] == 'ratingValue':
                app_rating_value = rating_meta.attrib['content']
                pass
            elif rating_meta.attrib['itemprop'] == 'ratingCount':
                app_rating_count = rating_meta.attrib['content']
                pass
            pass
        except KeyError:
            ## there can be situations additional_meta_content don't have 'itemprop'
            pass

    ## application updated date and number of installs
    app_updated = ''
    app_installs = ''
    additional_information = body_content('.details-section-contents')
    additional_meta_data = additional_information('.meta-info')
    for additional_meta in additional_meta_data:
        additional_meta_content = additional_meta_data(additional_meta)('.content')
        # additional_meta_content = additional_meta('.content')
        try:
            if additional_meta_content[0].attrib['itemprop'] == 'datePublished':
                app_updated = additional_meta_content.text()
                pass
            elif additional_meta_content[0].attrib['itemprop'] == 'numDownloads':
                app_installs = additional_meta_content.text()
                pass
            else:
                pass
            pass
        except KeyError:
            ## there can be situations additional_meta_content don't have 'itemprop'
            pass

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
        'thumbnails': app_thumbnails
    }

    scraped_applications.append(application)
    pass

print('done')