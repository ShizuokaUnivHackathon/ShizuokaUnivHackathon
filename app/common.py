
import subprocess

def pic_print(pic):
    res = subprocess.call(['lp',pic])
    if(res == 0):
        print("printing now!")
    else:
        print("lp command error")
