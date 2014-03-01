__author__ = 'grainier'

from pyquery import PyQuery as pq
import redis
import pickle

scraped_applications = []
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
set_key = 'set_priority_x'
r_server = redis.Redis("localhost")
application_keys = r_server.smembers(set_key)

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
    app_title = body_content('.info-container .document-title').text()

    ## application thumbnail
    app_icon = body_content('img.cover-image')[0].attrib['src']

    ## application price
    app_price = ''
    button_buy = body_content('button.price.buy')
    price_meta_data = button_buy('meta')
    for price_meta in price_meta_data:
        if price_meta.attrib['itemprop'] == 'price':
            app_price = price_meta.attrib['content']
            pass
        pass

    ## number of badges like Top Developer, Editors Choice
    special_badges = body_content('.header-star-badge .badge')
    number_of_badges = len(special_badges)

    ## application description
    description_content = body_content('.description .id-app-orig-desc')
    app_description = description_content.html()

    ## application rating value && count
    rating_box = body_content('.rating-box .score-container')
    rating_meta_data = rating_box('meta')
    rating_value = ''
    rating_count = ''
    for rating_meta in rating_meta_data:
        if rating_meta.attrib['itemprop'] == 'ratingValue':
            rating_value = rating_meta.attrib['content']
            pass
        elif rating_meta.attrib['itemprop'] == 'ratingCount':
            rating_count = rating_meta.attrib['content']
            pass
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

    ## screen shots
    app_thumbnails = []
    thumbnails_soups = body_content('.thumbnails .screenshot')
    for thumbnail in thumbnails_soups:
        thumbnail_url = thumbnail.attrib['src']
        app_thumbnails.append(thumbnail_url)
        pass

    ## make a application object
    application = {
        'id': app_id,
        'url': app_url,
        'title': app_title,
        'icon': app_icon,
        'badges': number_of_badges,
        'rating': rating_value,
        'rating_count': rating_count,
        'updated': app_updated,
        'installs': app_installs,
        'description': app_description,
        'price': app_price,
        'thumbnails': app_thumbnails
    }

    scraped_applications.append(application)
    pass

print('done')