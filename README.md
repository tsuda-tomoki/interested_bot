# Persopnal Discord bot (Python)
趣味で作成している Discord bot

## Enviroment
Linux

## Use Tech
* uv
* Python
* discord.py
* Annict API

## Use Info (Update)
起動しているプロセスを削除
```
ps aux | grep 'main.py'
kill -9 <PID> or pkill -f 'uv run main.py'
```

テスト時は
`uv run main.py`

アップデートが完了したら、接続断してもプロセスが動くようにnohupで実行
(テストしてたときは、プロセスを一回クリア)
`nohup uv run main.py &`
