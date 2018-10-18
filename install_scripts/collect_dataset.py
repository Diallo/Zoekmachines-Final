"""
Collect the dataset and place it within the data folder.
"""
import wget

url = "http://zoekmachinesdata.mdiallo.nl/datasets/ted_talks/ted-talks.zip"

file_name = wget.download(url)