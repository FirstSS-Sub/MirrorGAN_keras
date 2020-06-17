FROM nvidia/cuda:9.0-cudnn7-runtime

WORKDIR /MirrorGAN_keras
COPY . .

RUN apt update && apt install -y python3-pip --fix-missing
RUN pip3 install --upgrade pip==20.1.1
RUN pip3 install tensorflow-gpu==1.12.0 keras==2.2.4 \
easydict==1.9 nltk==3.5 torch==1.5.0 torchvision==0.6.0 \
numpy==1.16.6 pandas matplotlib
# kerasのバージョンはこれじゃないとエラーが出るはず