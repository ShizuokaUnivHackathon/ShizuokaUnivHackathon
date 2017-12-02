## TODO bluetoothのsocket通信の部分 
## TODO filename = 時刻にする
## ディスプレイにカメラの様子を映して、それを見ながら撮影したほうがいいかも
import bluetooth
import threading
import sys
import evdev
import subprocess
import picamera
import time
import pygame.mixer

host_mac_address = 'raspi mac address'
port = 3454
clients = []


#smart phone#
def BLE_server_start():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.bind((host_mac_address, port))
    sock.listen(1)

    while True:
        print("waiting for access.")
        con, address = sock.accept()
        print("[connect]{}".format(address))
        clients.append((con, address))
        handle_thread = threading.Thread(target=handler,args=(con, address),daemon=True)
        handle_thread.start()


def handler(con,address):
    ##撮影信号を受け取り、画像を送信
    while True:
        try:
            data = con.recv(1024) 
        except ConnectionResetError:
            remove_conection(con, address)
            break
        else:
            if not data:
                remove_conection(con, address)
                break
            else:
                print("[accept]{} - {}".format(address, data.decode("utf-8")))


def remove_conection(con, address):     
    print('[disconnect]{}'.format(address))
    con.close()
    clients.remove((con, address))

#button#
def button_listen():
    filename = "sample.jpg"
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    is_button_down = False
    
    if len(devices) == 0:
        print ("No devices found, try running with sudo")
        sys.exit()
    
    for device in devices:
        #print(device.name)
        if device.name == 'AB Shutter3       ':
            print(device)
            for event in device.read_loop():
                if event.type == evdev.ecodes.EV_KEY and event.code == 115:
                    if(is_button_down == False):
                        is_button_down = True
                    else:
                        is_button_down = False
                        print("camera ON!")
                        #take_picture(filename) #Please,call take picture function
                        #print_picture(filename)
                    # print(evdev.util.categorize(event))


def print_picture(filename):
    res = subprocess.call(['lp',filename])
    if(res == 0):
        print("printing now!")
    else:
        print("lp command error")
        sys.exit()


def take_picture(filename):
    camera = picamera.PiCamera()
    sound1 = pygame.mixer.Sound("chime01.ogg")
    sound2 = pygame.mixer.Sound("nc2036.wav")
    camera.resolution = (2592,1944) 
	
    camera.start_preview()
    time.sleep(3)
    camera.stop_preview()
	
	for x in range(1,4)
		sound1.play()
		time.sleep(1)
	
	sound2.play()
	
    camera.capture(filename)

if __name__ == "__main__":
    button_thread = threading.Thread(target=button_listen)
    button_thread.start()
    BLE_server_start()
    
 
