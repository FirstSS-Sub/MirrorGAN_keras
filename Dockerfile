FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

WORKDIR /MirrorGAN_keras
COPY . .

RUN apt update && apt install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install tensorflow-gpu==1.14.0 keras==2.2.4 \
easydict==1.9 nltk==3.5 torch==1.5.1 torchvision==0.6.1 \
numpy==1.16.6 pandas==1.0.5 matplotlib==3.1.2
# kerasのバージョンはこれじゃないとエラーが出るはず

CMD ["python3", "main.py"]