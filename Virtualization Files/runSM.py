import subprocess
import time


if __name__ == '__main__':
    print("Smart Meter 1")
    subprocess.call("python Virtualization\ Files/SmartMeterClient.py 1", shell=True)
    time.sleep(1)
    print("Smart Meter 2")
    subprocess.call("python Virtualization\ Files/SmartMeterClient.py 2", shell=True)
    time.sleep(1)
    print("Smart Meter 3")
    subprocess.call("python Virtualization\ Files/SmartMeterClient.py 3", shell=True)
