import subprocess
import re
import requests
import wpi3_bme280

def main():
    print("active function")
    
    wpi3_bme280.readData()
    temp = wpi3_bme280.temp
    
    r = requests.post("https://tempet.sakura.tv/tempet/Raspi_bme.php", data={'data': temp})
    
    pet = requests.get("https://tempet.sakura.tv/tempet/Raspi_selected_pet.txt")
    preset = res.content.decode()