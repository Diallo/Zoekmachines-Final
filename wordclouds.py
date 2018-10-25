from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib.pyplot as plt

# Start with one review:
text = "This is some awesome text"

# If we want to update the set of stopwords
# stopwords = set(STOPWORDS)
# stopwords.update(["TED"])
# add stopwords=stopwords to WordCloud(..)

wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

wordcloud.to_file("src/static/img/WordCloudOfQuery.png")