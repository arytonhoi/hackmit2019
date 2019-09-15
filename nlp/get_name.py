import tldextract #library for url domain name extraction
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('url')
  args = parser.parse_args()

  extraction = tldextract.extract(args.url)
  print(extraction.domain)