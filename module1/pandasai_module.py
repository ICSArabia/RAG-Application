import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import os
import sys

API_KEY = "**********"
os.environ["OPENAI_API_KEY"] = API_KEY

df = pd.read_csv(r"D:\ICS_Arabia\LLM_Langchain\module1\student.csv")

question = sys.argv[1]

llm = OpenAI()
pandas_ai = PandasAI(llm)
x = pandas_ai.run(df, prompt=question)

print(x)