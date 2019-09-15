from nlp.article import Article

if __name__ == '__main__':
  url = 'https://www.allsides.com/news/2019-08-23-0733/plan-end-gun-violence-students-who-survived-it'
  title = 'Lara Trump: 2020 budget child care proposal will tackle very real crisis threatening American families'
  with open('fox1.txt', 'r') as file:
    content = file.read().replace('\n', '')

  a = Article(url,title,content)    
  print(a.source_name)
  a.print_topic_info()