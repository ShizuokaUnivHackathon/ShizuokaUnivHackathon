import json
import requests
import gmplot

url = 'https://api.flickr.com/services/rest/'
api_key = 'apikey'
search_query = {
        'method': 'flickr.photos.search',
        'api_key': api_key,
        'per_page': '2', 
        'has_geo':'1',       
        'text':'静岡',
        'format': 'json',
        'nojsoncallback': '1'
}

geo_getLocation_query = {
    'method': 'flickr.photos.geo.getLocation',
    'api_key': api_key,
    # Later update 'photo_id'
    'format': 'json',
    'nojsoncallback': '1'
}

r = requests.get(url, params=search_query)
data_list = json.loads(r.text)
data_list = data_list['photos']['photo']

geo_data=[]
lon=[]
lat=[]
for data in data_list:
    geo_getLocation_query.update({'photo_id':data['id']})
    r = requests.get(url, params=geo_getLocation_query)
    getted_data = json.loads(r.text)

    print(float(getted_data['photo']['location']['longitude']))
    lon.append(float(getted_data['photo']['location']['longitude']))
    lat.append(float(getted_data['photo']['location']['latitude']))
    # id = getted_data['photo']['id']#画像id取得
    # longitude= getted_data['photo']['location']['longitude']#経度取得
    # latitude= getted_data['photo']['location']['latitude']#緯度取得
    # geo_data.append({'id':id, 'longitude':longitude, 'latitude':latitude})

# geo_data
#        =>[0]
#            =>'id':1234
#            =>'longitude': 23.324
#            =>'latitude' :123.329
#        =>[1]
#            =>'id':5678
#            =>'longitude': 43.436
#            =>'latitude' :533.345
#          :
#          :
#          :
 

gmap = gmplot.GoogleMapPlotter(float(lat[0]), float(lon[0]), 16)
#gmap.scatter(lat, lon, '#FF0000', edge_width=10)
#gmap.heatmap(lat, lon,size=1500,marker=False)
gmap.scatter(lat, lon, '#FF0000', size=1500, marker=False)
gmap.draw("mymap.html")

# gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
# gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
# gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
# gmap.heatmap(heat_lats, heat_lngs)

# gmap.draw("mymap.html")