#!/usr/bin/env python
"""
Using custom colors
===================
Using the recolor method and custom coloring functions.
"""



import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import os
import random

from wordcloud import WordCloud, STOPWORDS



def create_cloud(doc_id,text):

    if os.path.isfile('static/img/{}.png".format(doc_id)'):
        return

    def grey_color_func(word, font_size, position, orientation, random_state=None,
                        **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # read the mask image taken from
    mask = np.array(Image.open(path.join(d, "src/static/img/TED.png")))


    # adding movie script specific stopwords
    stopwords = set(STOPWORDS)
    stopwords.add("ted")
    stopwords.add("talk")

    wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=10,
                   random_state=1, background_color="white").generate(text)

    wc.to_file("src/static/img/clouds/{}.png".format(doc_id))
