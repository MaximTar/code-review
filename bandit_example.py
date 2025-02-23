import subprocess

user_input = input("Enter command: ")
subprocess.run(user_input, shell=True)  # 🚨 Риск инъекции
