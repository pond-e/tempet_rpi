import subprocess
import requests
import bme280

def main():
    print("active function")
    
    bme280.readData()
    temp = bme280.temperature
    
    r = requests.post("https://tempet.sakura.tv/tempet/Raspi_bme.php", data={'data': temp})
    
    pet = requests.get("https://tempet.sakura.tv/tempet/Raspi_selected_pet.txt")
    preset = res.content.decode()
    dog = 'dog' in preset
    cat = 'cat' in preset
    bird = 'bird' in preset
    rabbit = 'rabbit' in preset

    # エアコンをつける室温の閾値の設定
    # dog[18:28], cat[20:28], bird[20:28], rabbit[18:24]
    if(rabbit):
        lower = 18
        upper = 24
    elif((not dog) and (not rabbit) and (cat or bird)):
        lower = 20
        upper = 28
    else:
        lower = 18
        upper = 20

    if(temp < lower):
        cmd = "ls"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if('power' in result.stdout):
            cmd = "python3 irrp.py -p -g17 -f "+"power "+"light:on"
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if(result != ''):
                print("powerが失敗しました。")
        
        cmd = "python3 irrp.py -p -g17 -f "+"heating "+"light:on"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if(result != ''):
            print("heatingが失敗しました。")
    elif(temp > upper):
        cmd = "ls"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if('power' in result.stdout):
            cmd = "python3 irrp.py -p -g17 -f "+"power "+"light:on"
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if(result != ''):
                print("powerが失敗しました。")
        
        cmd = "python3 irrp.py -p -g17 -f "+"cooling "+"light:on"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if(result != ''):
            print("coolingが失敗しました。")
