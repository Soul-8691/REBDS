# import requests
# import json

# f = open("YGOProDeck_Card_Info.json", "w")
# url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
# res = requests.get(url)
# data = json.dumps(res.json(), indent=4)
# f.write(data)
# f.close()

import requests
import json
import os

card_info_data = open('YGOProDeck_Card_Info.json')
card_info_data = json.load(card_info_data)
card_info = {}
for data in card_info_data['data']:
    card_name = data['name']
    for card_image in data['card_images']:
        card_id = str(card_image['id'])
        image_url = 'https://images.ygoprodeck.com/images/cards/' + card_id + '.jpg'
        image_url_small = 'https://images.ygoprodeck.com/images/cards_small/' + card_id + '.jpg'
        image_url_cropped = 'https://images.ygoprodeck.com/images/cards_cropped/' + card_id + '.jpg'
        res = requests.get(image_url)
        filename = card_id + '.jpg'
        if not os.path.exists(filename):
            print('Now downloading ' + card_name)
            with open(filename, 'wb') as file:
                file.write(res.content)
        res = requests.get(image_url_small)
        filename = card_id + '_small.jpg'
        if not os.path.exists(filename):
            with open(filename, 'wb') as file:
                file.write(res.content)
        res = requests.get(image_url_cropped)
        filename = card_id + '_cropped.jpg'
        if not os.path.exists(filename):
            with open(filename, 'wb') as file:
                file.write(res.content)