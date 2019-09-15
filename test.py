from nlp.article import Article

if __name__ == '__main__':
  url = 'https://www.foxnews.com/politics/california-newsom-abortion-pill-bill-public-university-campus'
  title = 'California bill on \'abortion pill\' access at public universities goes to governor\'s desk'
  with open('fox1.txt', 'r') as file:
    content = file.read().replace('\n', '')

  a = Article(url,title,content)    
  print(a.source_name)
  # a.print_topic_info()
  # a.make_gsearch_query()
  a.get_agreeing_articles()
  a.get_disagreeing_articles()
  a.get_neutral_articles()