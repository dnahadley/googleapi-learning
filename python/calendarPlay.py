"""
Google Calendar example from 
https://developers.google.com/api-client-library/python/start/get_started#installed
"""

import httplib2
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

# in this example the client id and client secret are command-line arguments
client_id = sys.argv[1]
client_secret = sys.argv[2]

# the scope URL for read/write access to a user's calendar data
scope='https://www.googleapis.com/auth/calendar'

# create flow object.  This object holds the client_id, client_secret, and 
# scope.  It assists with OAuth 2.0 steps to get user authorization and
# credentials
flow = OAuth2WebServerFlow(client_id, client_secret, scope)

def main():
    # Create a Storage object. This object holds the credentials that yoy
    # application needs to authorize access to the user's data. The name of the
    # credentials file is provided. If the file does not exist it is created.
    # This object can only hold credentials for a single user, so as-written
    # this script can only handle a single user
    storage = Storage('credentials.dat')
    
    # If no credentials are found or the credentials are invalid due to 
    # expiration, new credentials need to be obtained from the authorization
    # server page in your default web browser. The server asks the user to
    # grant your application access to the user's data. If the user grants
    # access, the run() function returns new credentials. the new credentials
    # are also stored in the supplied Storage object, which updates the
    # credentials.dat file
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)
        
    # create an httplib2.Http object to handle our HTTP requests, and authorize
    # it using the credentials.authorize() function.
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    
    # The apiclient.discovery.build() function returns an instance of an API
    # object which can be used to make API calls.  The object is constructed
    # with methods specific to the calendar API. The arguments provided are:
    #   name of the API ('calendar')
    #   version of the API ('v3')
    #   authorized httplib2.Http() object that can be used for API calls
    service = build('calendar', 'v3', http=http)
    
    try:
        # The Calendar API's events().list method returns paginated results,
        # so we have to execute the request in a paging loop. First, build the
        # request object. The arguments provided are:
        #   primary calendar for user
        request = service.events().list(calendarId='primary')
        # Loop until all pages have been processed
        while request != None:
            # Get the next page
            response = request.execute()
            # Accessing the response like a dict object with an 'items' key
            # returns a list of item objects (events)
            for event in response.get('items', []):
                # the event object is a dict object with a 'summary' key.
                print repr(event.get('summary', 'NO SUMMARY')) + '\n'
            # Get the next request object by passing the previous request object
            # to the list_next method.
            request = service.events().list_next(request, response)
            
    except AccessTokenRefreshError:
        # The accessTokenRefreshError exception is raised if the credentials
        # have been revoked by the user or they have expired.
        print ('the credentials have been revoked or expired, please re-run '
               'the application to re-authorize')
        
if __name__ == '__main__':
    main()
