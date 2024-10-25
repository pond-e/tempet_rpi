# tempet_rpi
Python 3.9.2

PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=raspbian
ID_LIKE=debian

main.pyをsudoで動かす

#### シーケンス
- `main.py`
  - Raspi_state.txtを見に行く
  - Raspi_state.txtの記述に応じて条件分岐をして、それぞれのモジュールの関数を実行する
  - 10秒間動作を停止
  - 以上を無限ループ
- `active.py`
  - Raspiの温度を取得する
  - 取得した温度をRaspi_bme.phpに送る
  - Raspi_selected_pet.txtを見てどのプリセットを使うか確認する
  - 温度が低（高）ければ、エアコンの電源をつけて（電源がある場合）暖房（冷房）をつける、温度を指定する
  - return でmain.pyに戻る
- `remember.py`
  - 関数の引数として「cooling」などの文字を受け取る
  - 記憶開始
  - 記憶終了
  - Raspi_receive.phpに「success」を送る
  - return でmain.pyに戻る
  - ※温度の記憶の場合は2番目から4番目を19℃から29℃まで繰り返す
- `stop.py`
  - エアコンに停止を命令する
  - return でmain.pyに戻る 