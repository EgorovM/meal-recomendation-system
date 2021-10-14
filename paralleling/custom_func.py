import pymorphy2
import pandas as pd

morph = pymorphy2.MorphAnalyzer()

def parse(content):
    return " ".join([morph.parse(word)[0].normal_form for word in content.split()])

def to_lower(content):
    if pd.isna(content):
        return content
    
    return content.lower()