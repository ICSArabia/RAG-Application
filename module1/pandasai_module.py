'''
This module is used to run the PandasAI module on the command line.
'''

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import os
import argparse
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY

argparser = argparse.ArgumentParser()
argparser.add_argument("--query", help="Question to ask")
argparser.add_argument("--path", help="Path to the document")

args = argparser.parse_args()

question = args.query
path = args.path

df = pd.read_csv(path)

llm = OpenAI(model='gpt-4-0613',temperature=0.0)
pandas_ai = PandasAI(llm)
x = pandas_ai.run(df, prompt=question)
print(x)

