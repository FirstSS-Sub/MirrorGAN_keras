# MirrorGAN_keras

## 導入
- Dockerの導入をまだ行っていない場合はhttps://github.com/FirstSS-Sub/Docker-Mnistの手順で導入する
- このリポジトリをclone
- 研究室の `share/members/sito/MirrorGAN_keras` にある、`data`フォルダをclone してきたこのリポジトリの直下に配置

## 実行
```
docker-compose build
docker-compose up
docker exec -it mirrorgan bash
```
でコンテナを立ち上げてコンテナ内に入れます。
その後、
```
python3 main.py
```
で実行。
pretrainかtrainを選択し、EPOCH数とMAX_BRANCH数を選択したら学習が始まります。
学習のさせ方はhttps://github.com/komiya-m/MirrorGANを参照。
  
コンテナから抜けるときは`Ctrl+p``Ctrl+q`で抜けられます。
抜けたあとも`docker logs mirrorgan -f`でログを見ることができます。