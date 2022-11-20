import subprocess
import re

def main():
    print("stop function")
    cmd =  "python3 irrp.py -p -g17 -f "+"stop_button "+"light:on"
    result = subprocess.run(cmd, capture_output=True, shell=True, text=True)
    if(result!=''):
        print("stop_buttonが失敗しました。")
    else:
        print("top_buttonが成功しました。")