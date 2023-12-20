'''
This module is used to run the PandasAI module on the command line.
'''

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import os
import base64
import time

def check_recent_files(folder_path):
    current_time = time.time()
    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            if current_time - creation_time <= 60:  # Checking if file was created in last 2 minutes (120 seconds)
                return True

def pandas_ai_function(question, path):
    
    base64_image = None
    result = None
    
    CWD = os.getcwd()
    if path == 'insurance':
        file_path = os.path.join(CWD, 'LangChainApp', 'module1_pandasai', 'documents', f'{path}.csv')
        df = pd.read_csv(file_path)
        
    elif path == 'AAPL10Y':
        file_path = os.path.join(CWD, 'LangChainApp', 'module1_pandasai','documents', f'{path}.xlsx')
        df = pd.read_excel(file_path)
        
    charts_path = r"charts"

    llm = OpenAI(model='gpt-4',temperature=0.0)
    # pandas_ai = PandasAI(llm)
    # x = pandas_ai.run(df, prompt=question)
    # print(x)

    sdf = SmartDataframe(df, config={"llm": llm, "save_charts": True,"save_charts_path": charts_path, "enable_cache": False, "open_charts": False })

    result = sdf.chat(question)


    if check_recent_files(charts_path):
        png_files = []
        for filename in os.listdir(charts_path):
            if filename.endswith(".png"):
                png_files.append(filename)

        # Sort the PNG files by creation date, newest first.
        png_files.sort(key=lambda filename: os.path.getctime(os.path.join(charts_path, filename)), reverse=True)

        # Get the path to the latest PNG file.
        if len(png_files) >= 0:
            latest_png_file_path = os.path.join(charts_path, png_files[0])

        with open(latest_png_file_path, "rb") as f:
            image_bytes = f.read()

        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
    return result, base64_image