'''
This file contains the helper functions that are used in the views.py file.
'''

import os
import subprocess

def activate_virtualenv(module, env_name, python_file, question, document_path):

    root_path = os.path.dirname(os.path.abspath(__file__))
    python_interpreter = os.path.join(root_path, module, f"{env_name}\Scripts\python.exe")

    python_file_path = os.path.join(root_path, module, f'{python_file}.py') 
    
    # question and document_path are passed as arguments to the python file
    command = f"{python_interpreter} {python_file_path} --query \"{question}\" --path \"{document_path}\""

    # Use subprocess to execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for the process to finish and get output
    output, error = process.communicate()
    print(output)

    if process.returncode == 0:
        print("Execution successful!")
    else:
        print("Error occurred:", error.decode())

    return output.decode()