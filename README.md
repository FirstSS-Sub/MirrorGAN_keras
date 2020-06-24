# MirrorGAN_keras

## 導入
- Dockerの導入をまだ行っていない場合は https://github.com/FirstSS-Sub/Docker-Mnist の手順で導入する
- このリポジトリをclone
- 研究室の `share/members/saito/MirrorGAN_keras` にある`data`フォルダと`model`フォルダを、cloneしてきたこのリポジトリの直下に配置
    - なお、必要なのは`model/cnn_rnn_encoder.h5`だけなので、それ以外のファイルはどちらでも良い

## 実行
```
sudo docker build -t mirrorgan .
sudo docker run --gpus all --runtime=nvidia --rm -it mirrorgan
```
でコンテナを立ち上げてコンテナ内に入れます。  
その後、pretrainかtrainを選択し、EPOCH数とMAX_BRANCH数を選択したら学習が始まります。  
学習のさせ方は https://github.com/komiya-m/MirrorGAN を参照。
  
`sudo docker exec -it mirrorgan bash`でコンテナ内に入って任意の操作をすることもできます。  
コンテナから抜けるときは`Ctrl+p`、`Ctrl+q`で抜けられます。  
抜けたあとも`docker logs mirrorgan -f`でログを見ることができます。