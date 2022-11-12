import subprocess
import requests

def server_finish_wait():# 記憶が成功してmainに処理が戻ったときに、まだserverでstete.txtが変更されてなくてもう一度このファイルが呼び出されるのを防ぐ
    res = requests.get("https://tempet.sakura.tv/tempet/Raspi_state.txt")
    while(res.content.decode() != "none"):# 
        res = requests.get("https://tempet.sakura.tv/tempet/Raspi_state.txt")

def main(remember_button):
    temperature_bottom = 19
    temperature_top = 29
    if(remember_button == "temperature"):
        for i in range(19, temperature_top+1):# 19℃から29℃のボタンを記憶する
            cmd = "python3 irrp.py -r -g18 -f temperature" + str(i) + " light:on --no-confirm --post 130"
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if(result != ''):
                print("retry temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
            else:
                print("success temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
                if(i == temperature_top):
                    server_finish_wait()
    else:
        cmd = "python3 irrp.py -r -g18 -f " + remember_button + " light:on --no-confirm --post 130"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if(result != ''):
            print("retry " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
        else:
            print("success " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
            server_finish_wait()
    


def test(remember_button):
    temperature_bottom = 19
    temperature_top = 29
    if(remember_button == "temperature"):
        for i in range(19, temperature_top+1):# 19℃から29℃のボタンを記憶する
            cmd = "python3 irrp.py -r -g18 -f temperature" + str(i) + " light:on --no-confirm --post 130"
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if(result != ''):
                print("retry temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
            else:
                print("success temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
                if(i == temperature_top):
                    server_finish_wait()
    else:
        cmd = "python3 irrp.py -r -g18 -f " + remember_button + " light:on --no-confirm --post 130"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if(result != ''):
            print("retry " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
        else:
            print("success " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
            server_finish_wait()

if __name__ == "__main__":
    test("cooling")