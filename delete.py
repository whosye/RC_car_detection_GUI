
stringos = "16:40:45  SignalTracer:366   INFO            added bookmark: Speed [100] rpm, Torque [35] Nm"

import re




bookmark = []
with open("New Text Document.txt", 'r') as file: 
    for i, line in enumerate(file):
        if  "added bookmark:" in line:
            pattern = r"Speed \[(\d+(?:\.\d+)?)\] rpm, Torque \[(\d+(?:\.\d+)?)\] Nm"

            result = re.findall(pattern= pattern, string=line)
            speed, torque = result[0]
            print(f"speed = {(speed)}, torque= {(torque)}")
   


