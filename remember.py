import subprocess

def main(remember_button):
    if(remember_button == "temperature"):
        for i in range(19, 30):# 19℃から29℃のボタンを記憶する
            cmd = "python3 irrp.py -r -g18 -f temperature" + str(i) + " light:on --no-confirm --post 130"
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if(result != ''):
                print("retry temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
            else:
                print("success temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
                # TODO:記憶した情報を「記憶したボタン, 情報」の形でファイルに保存する（ファイル名未定）
    else:
        cmd = "python3 irrp.py -r -g18 -f " + remember_button + " light:on --no-confirm --post 130"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if(result != ''):
            print("retry " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
        else:
            print("success " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
            # TODO:記憶した情報を「記憶したボタン, 情報」の形でファイルに保存する（ファイル名未定）


def test(remember_button):
    if(remember_button == "temperature"):
        for i in range(19, 30):# 19℃から29℃のボタンを記憶する
            cmd = "python3 irrp.py -r -g18 -f temperature" + str(i) + " light:on --no-confirm --post 130"
            result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
            if(result != ''):
                print("retry temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
            else:
                print("success temperature " + str(i))
                # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
                # TODO:記憶した情報を「記憶したボタン, 情報」の形でファイルに保存する（ファイル名未定）
    else:
        cmd = "python3 irrp.py -r -g18 -f " + remember_button + " light:on --no-confirm --post 130"
        result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
        if(result != ''):
            print("retry " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "retry"}をPOSTで送る
        else:
            print("success " + remember_button)
            # TODO:Raspi_receive.phpに{"status": "success"}をPOSTで送る
            # TODO:記憶した情報を「記憶したボタン, 情報」の形でファイルに保存する（ファイル名未定）


if __name__ == "__main__":
    test("cooling")