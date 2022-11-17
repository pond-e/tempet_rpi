import subprocess
import re

def main():
    print("stop function")
    cmd =  "python3 irrp.py -p -g17 -f "+"stop_button "+"light:on"
    result = subprocess.run()
    if(result!=''):
        print("stop_buttonが失敗しました。")
    else:
        print("top_buttonが成功しました。")