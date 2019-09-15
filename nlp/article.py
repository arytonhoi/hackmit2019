from nlp.nlp import NLP
from nlp.topic import Topic
import tldextract #library for url domain name extraction
from googleapiclient.discovery import build # google search api

# represents an Article
class Article:
    # Constructor
    def __init__(self, url=None,title=None,text_content=None):
        self.url = url # url of article
        self.title = title
        self.text_content = text_content # article text
        
        # values computed later
        self.source_name = None # (Ex. CNN or Fox)
        self.topics = [] # list of topic objects from content
        self.title_topics = [] # list of topics from title
        self.citations = [] #list of citation objects
        self.date = None # date of article
        
        self.related_articles = [] # list of related articles

        self.nlp = NLP()
        self.get_source_name()
        self.get_topics()
        
   
    # gets source name (Ex. CNN or Fox) of Article based on url
    def get_source_name(self):
        extraction = tldextract.extract(self.url)
        self.source_name = extraction.domain

    # Uses GCloud NPL api to parse text for topics (entities)
    # topics are keywords to the article
    def get_topics(self, salience_threshold=0.02,language='en'):
        self.topics = self.nlp.get_topics(self.text_content,salience_threshold,language=language)
        if self.title:
            self.title_topics = self.nlp.get_topics(self.title,salience_threshold,language=language)
        return None        

    # get most important keywords of article
    def get_keywords(self,num=3):
        all_topics = self.title_topics + self.topics
        # sort by salience
        keywords = sorted(all_topics,key=Topic.get_salience)
        return keywords[:num]

    # form query from keywords
    def make_gsearch_query(self,num_results=10):
        query = ""
        keywords = self.get_keywords()
        for count,keyword in enumerate(keywords):
            if count == len(keywords) - 1:
                query += 'allintext: ' + keyword.get_name()
            else:
                query += 'allintext: ' + keyword.get_name() + ' OR '

        service = build("customsearch", "v1",developerKey="AIzaSyDmMtbto7Wpq_BoCwSI9jzruHi7mwOKQZk")
        print(query)
        results = service.cse().list(
            q=query,#query
            cx='001726485510114792400:d0dxila2d96',#search engine id
            num=num_results # number of results to give
            ).execute()

        related_article_urls = []
        for result in results['items']:
            related_article_urls.append(result['link'])

        print(related_article_urls)
        return related_article_urls
        

    # Gets other articles that agree with this one
    def get_agreeing_articles(self,amount=5):
        return None

    # Gets other articles that are neutral on this one's topic
    def get_neutral_articles(self,amount=5):
        return None

    # Gets other articles that disagree with this one's stance
    # on the topic
    def get_disagreeing_articles(self,amount=5):
        return None

    # prints topic info
    def print_topic_info(self):
        for topic_list in [self.title_topics,self.topics]:
            if topic_list:
                print('Topics Set ...')
                for topic in topic_list:
                    salience = topic.salience
                    sentiment = topic.sentiment

                    statement = "Topic:{} type:{} salience:{:.2f} sentiment:{:.2f},{:.2f}"
                    print(statement.format(topic.topic_name,
                                        topic.topic_type,
                                        topic.salience,
                                        topic.sentiment.score,
                                        topic.sentiment.magnitude))
