# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from counter_point.nlp.topic import Topic

class NLP:
    # Constructor
    def __init__(self):
        # Instantiates a client
        self.client = language.LanguageServiceClient()

    def get_topics(self,content,salience_threshold,language='en',
                type_=enums.Document.Type.PLAIN_TEXT, encoding_type=enums.EncodingType.UTF8):
        # print('getting topics')
        # topics list
        topics = []

        # call API to get entity analysis
        document = {"content": content, "type": type_, "language": language}
        api_response = self.client.analyze_entity_sentiment(document, encoding_type=encoding_type)

        # loop over entities in api response

        # # Detects the sentiment of the text
        # sentiment = client.analyze_sentiment(document=document).document_sentiment

        # print('Text: {}'.format(text))
        # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

        for entity in api_response.entities:
            entity_salience = entity.salience
            if entity_salience > salience_threshold:
                topics.append(Topic(entity.name,enums.Entity.Type(entity.type).name,
                                    entity_salience,entity.sentiment))   

        return topics