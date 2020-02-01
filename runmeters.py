import subprocess
import SmartMeterClient
from py._builtin import execfile

if __name__ == '__main__':
    for i in range(0, 10):
        print("Smart Meter ", i)
        subprocess.call("python3 SmartMeterClient.py" [i])
