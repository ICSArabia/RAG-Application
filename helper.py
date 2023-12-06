import os
import subprocess

def activate_virtualenv(module, env_name, python_file, question):

    root_path = "C:\llm_project\LLM_Langchain"
    python_interpreter = os.path.join(root_path, module, f"{env_name}\Scripts\python.exe")

    python_file_path = os.path.join(root_path, module, f'{python_file}.py') 
    print(question)
    
    command = f"{python_interpreter} {python_file_path} \"{question}\""

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