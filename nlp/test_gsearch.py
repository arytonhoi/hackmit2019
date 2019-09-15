"""Simple command-line example for Custom Search.
Command-line application that does a search.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import pprint

from googleapiclient.discovery import build


def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyDmMtbto7Wpq_BoCwSI9jzruHi7mwOKQZk")

  results = service.cse().list(
      q='allintext:gun control OR allintext:school shootings',#query
      cx='001726485510114792400:d0dxila2d96',#search engine id
      num=2 # number of results to give
    ).execute()
  urls = []
  for result in results['items']:
    urls.append(result['link'])
  print(urls)

if __name__ == '__main__':
  main()