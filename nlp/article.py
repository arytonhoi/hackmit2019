from counter_point.nlp.nlp import NLP
import tldextract #library for url domain name extraction

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

    def get_keywords(self):
        return None

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
