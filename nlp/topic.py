class Topic:
    def __init__(self, topic_name,topic_type,salience,sentiment):
      self.topic_name = topic_name # topic name
      self.topic_type = topic_type # PERSON,LOCATION,etc
      self.salience = salience # prominence of topic to article
      self.sentiment = sentiment # sentiment of topic in article