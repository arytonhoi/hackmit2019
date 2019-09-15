from nlp.article import Article

if __name__ == '__main__':
  url = 'https://www.cnn.com/2019/09/11/politics/wiliam-bill-happer-leaves-national-security-council-donald-trump/index.html'
  title = 'Climate change skeptic leaves White House National Security Council'
  with open('fox1.txt', 'r') as file:
    content = file.read().replace('\n', '')

  a = Article(url,title,content)    
  print(a.source_name)
  # a.print_topic_info()
  # a.make_gsearch_query()
  a.get_agreeing_articles()
  a.get_disagreeing_articles()
  a.get_neutral_articles()