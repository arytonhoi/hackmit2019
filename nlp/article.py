from counter_point.nlp.nlp import NLP
from counter_point.nlp.topic import Topic
import tldextract #library for url domain name extraction
from googleapiclient.discovery import build # google search api

liberal_sources = ['cnn.com','npr.org','cbsnews.com','buzzfeednews.com','nytimes.com']
neutral_sources = ['apnews.com','reuters.com','bloomberg.com','bbc.com','thehill.com']
conservative_sources = ['foxnews.com','nationalreview.com','washingtontimes.com','nypost.com','wsj.com']

# represents an Article
class Article:
    # Constructor
    def __init__(self, url=None,title=None,text_content=None):
        self.url = url # url of article
        self.title = title
        self.text_content = text_content # article text
        
        # values computed later
        self.source_name = None # (Ex. CNN or Fox)
        self.source_base_url = None
        self.topics = [] # list of topic objects from content
        self.title_topics = [] # list of topics from title
        self.citations = [] #list of citation objects
        self.document_sentiment = None

        self.nlp = NLP()
        self.get_source_name()
        self.get_topics()
        self.get_document_sentiment()
    
    def get_document_sentiment(self):
        self.document_sentiment = self.nlp.get_whole_sentiment(self.text_content,language='en') 
        self.document_sentiment.score = 50 * (self.document_sentiment.score + 1.0)
        print('score {} mag{}'.format(self.document_sentiment.score, self.document_sentiment.magnitude))
        return None
   
    # gets source name (Ex. CNN or Fox) of Article based on url
    def get_source_name(self):
        extraction = tldextract.extract(self.url)
        self.source_name = extraction.domain
        self.source_base_url = extraction.domain + '.' + extraction.suffix

    # Uses GCloud NPL api to parse text for topics (entities)
    # topics are keywords to the article
    def get_topics(self, salience_threshold=0.02,language='en'):
        # print("articles topics")
        if self.topics:
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
    def make_gsearch_query(self,sources=None,amount=2):
        query = ""
        keywords = self.get_keywords()
        for count,keyword in enumerate(keywords):
            if count == len(keywords) - 1:
                query += 'allintext:' + keyword.get_name()
            else:
                query += 'allintext:' + keyword.get_name() + ' OR '
        
        if sources:
            for count,source in enumerate(sources):
                if count == len(sources) - 1:
                    query += ' site:' + source
                else:
                    query += ' site:' + source + ' OR'

        service = build("customsearch", "v1",developerKey="AIzaSyDmMtbto7Wpq_BoCwSI9jzruHi7mwOKQZk")
        # print(query)
        results = service.cse().list(
            q=query,#query
            cx='001726485510114792400:d0dxila2d96',#search engine id
            num=amount # number of results to give
            ).execute()

        related_article_urls = []
        for result in results['items']:
            print(result['link'])
            related_article_urls.append(result['link'])

        # print(related_article_urls)
        return related_article_urls
        
    # Gets other articles that agree with this one
    def get_agreeing_articles(self,amount=5):
        if self.source_base_url in liberal_sources:
            return self.make_gsearch_query(sources=liberal_sources,amount=amount)
        else:
            return self.make_gsearch_query(sources=conservative_sources,amount=amount)

    # Gets other articles that are neutral on this one's topic
    def get_neutral_articles(self,amount=5):
        return self.make_gsearch_query(sources=neutral_sources,amount=amount)

    # Gets other articles that disagree with this one's stance
    # on the topic
    def get_disagreeing_articles(self,amount=5):
        if self.source_base_url in liberal_sources:
            return self.make_gsearch_query(sources=conservative_sources,amount=amount)
        else:
            return self.make_gsearch_query(sources=liberal_sources,amount=amount)

    # prints topic info
    def print_topic_info(self):
        for topic_list in [self.title_topics,self.topics]:
            if topic_list:
                for topic in topic_list:
                    salience = topic.salience
                    sentiment = topic.sentiment

                    statement = "Topic:{} type:{} salience:{:.2f} sentiment:{:.2f},{:.2f}"
                    print(statement.format(topic.topic_name,
                                        topic.topic_type,
                                        topic.salience,
                                        topic.sentiment.score,
                                        topic.sentiment.magnitude))