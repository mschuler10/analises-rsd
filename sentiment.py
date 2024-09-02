from googletrans import Translator
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

class SentimentAnalysis:
    def __init__(self):
        pass

    @staticmethod
    def calculate_polarity(text, language='pt'):
        sid = SentimentIntensityAnalyzer()
        if language != 'en':
            translator = Translator()
            text = translator.translate(text, src=language, dest='en').text

        sentiment_scores = sid.polarity_scores(text)
        compound_score = sentiment_scores['compound']
        return 'pos' if compound_score >= 0.05 else 'neg' if compound_score <= -0.05 else 'neu'

if __name__ == "__main__":
    sa = SentimentAnalysis()

    texts = [
        "Estou muito feliz com o resultado!",
        "O dia está péssimo, tudo deu errado.",
        "Borboletas voam no Havaí."
    ]

    for text in texts:
        sentiment = sa.calculate_polarity(text)
        print(f"Texto: {text}\nSentimento: {sentiment}\n")
