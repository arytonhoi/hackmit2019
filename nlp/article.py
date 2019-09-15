from counter_point.nlp.nlp import NLP

# represents an Article
class Article:
    # Constructor
    def __init__(self, url=None,title=None,text_content=None):
        self.url = url # url of article
        self.title = title
        self.text_content = text_content # article text
        
        # values computed later
        self.news_source = None # (Ex. CNN or Fox)
        self.topics = [] # list of topic objects
        self.citations = [] #list of citation objects
        self.date = None # date of article

        self.nlp = NLP()
   
    # gets source name (Ex. CNN or Fox) of Article based on url
    def get_source_name(self):
        return None

    # Uses GCloud NPL api to parse text for topics (entities)
    # topics are keywords to the article
    def get_topics(self, salience_threshold=0.01):
        self.topics = self.nlp.get_topics(self.text_content,salience_threshold,title=self.title,language='en')

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
    def print_info(self):
        if self.topics: # check not empty
            for topic in self.topics:
                salience = topic.salience
                sentiment = topic.sentiment

                statement = "Topic:{} type:{} salience:{:.2f} sentiment:{:.2f},{:.2f}"
                print(statement.format(topic.topic_name,
                                    topic.topic_type,
                                    topic.salience,
                                    topic.sentiment.score,
                                    topic.sentiment.magnitude))


# if __name__ == '__main__':
#     title = 'A plan to end gun violence from students who survived it'
#     content = 'They demanded change and ignited a grass-roots movement that has given youthful new vigor to the fight for gun safety. Now, these young activists have put forward a bold gun-control proposal that aims to reframe the debate on gun policy.'

#     a = Article('rip.com',title,content)    
#     print(a.text_content)
#     a.get_topics()
#     a.print_info()