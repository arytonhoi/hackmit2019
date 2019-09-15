class Topic:
    def __init__(self, topic_name,topic_type,salience,sentiment):
      self.topic_name = topic_name # topic name
      self.topic_type = topic_type # PERSON,LOCATION,etc
      self.salience = salience # prominence of topic to article
      self.sentiment = sentiment # sentiment of topic in article

    def get_salience(self):
      return self.salience

    def get_name(self):
      return self.topic_name

    def get_sentiment(self):
      return self.sentiment