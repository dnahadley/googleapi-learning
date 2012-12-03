'''
Created on 2012-12-01
Google Books simple api test and shit...
This is almost word for word typed from the google api python client library
get started simple page
https://developers.google.com/api-client-library/python/start/get_started#simple

@author: Dan
'''
# import pprint
import sys
from apiclient.discovery import build


    
# for this example, the api key is provided as a cmd argument
api_key = sys.argv[1]

# The apiclient.discovery.build() function returns an instance of an API
# object that can be used to make API calls. The object is constructed with
# methods specific to the books API. The arguments provided are:
#    name of the api (books)
#    version of the API you are using (v1)
#     API key
service = build('books', 'v1', developerKey=api_key)

# the books api has a volumes().list() method that is used to list
# books given search criteria.  Arguments provided are:
#   volumes source ('public')
#   search query ('android')
# The method returns an apiclient.http.HttpRequest object that encapsulates
# all information needed to make the request, but it  does not call the API
request = service.volumes().list(source='public', q='android')

# the execute() function on the httprequest object actually calls the api.
# it returns a python object built from the  JSON response. You can print this
# object or refer to the Books API documentation to determine its structure.
response=request.execute()
# pprint.pprint(response)

# Accessing the response like a dict object with an 'items' key returns a list
# of item objects (books). The item object is a dict object with a volumeInfo
# key. The volumeInfo object is a dict with keys 'title' and 'authors'

print 'Found %d books:' % len(response['items'])
for book in response.get('items', []):
    print 'Title: %s, Authors: %s' % (
        book['volumeInfo']['title'],
        book['volumeInfo']['authors']
            )
