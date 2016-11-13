import vk
import time
print('VKPhotos Geo Location')
session = vk.Session('ec2edf2987c25a6af8f2c5b4f7a4d6ec884d007e49043f67344c385bb7bda77922abcd2c02921d7528648')
api = vk.API(session)
friends = api.friends.get()
friends_info = api.users.get(user_ids=friends)
geolocation = []

# Получаем геоданные всех фотографий каждого друга
# Цикл перебирающий всех друзей
for friend in friends_info:
        print('ID: %s Имя: %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))
        id = friend['uid']
        # Получаем все альбомы пользователя, кроме служебных
        albums = api.photos.getAlbums(owner_id=id)
        print('\t...альбомов % s...' % len(albums))
        # Цикл перебирающий все альбомы пользователя
        for album in albums:
            # Обрабатываем исключение для приватных альбомов/фото
            try:
                # Получаем все фотографии из альбома
                photos = api.photos.get(owner_id=id, album_id=album['aid'])
                print('\t\t...обрабатываем фотографии альбома...')
                # Цикл перебирающий все фото в альбоме
                for photo in photos:
                    # Если в фото имеются геоданны, то добавляем их в список geolocation
                    if 'lat' in photo and 'long' in photo:
                        geolocation.append((photo['lat'], photo['long']))
                print('\t\t...найдено %s фото...' % len(photos))
            except:
                pass
            # Задержка между запросами photos.get
            time.sleep(0.5)
        # Задержка между запросами photos.getAlbums
        time.sleep(0.5)
js_code = ""

# Проходим по всем геоданным и генерирум JS команду добавления маркера
for loc in geolocation:
    js_code += 'new google.maps.Marker({position: {lat: %s, lng: %s}, map: map }); \n' % (loc[0], loc[1])

# Считываем из файла-шаблона html данные
html = open('map.html').read()

# Заменяем placeholder на сгенерированный код
html = html.replace('/* PLACEHOLDER */ ', js_code)

# Записываем данные в новый файл
f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()
