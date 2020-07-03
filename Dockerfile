FROM nvidia/cuda:9.0-cudnn7-devel

WORKDIR /MirrorGAN_keras
COPY . .

RUN apt update && apt install -y python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow-gpu==1.12.0 keras==2.2.4 \
easydict==1.9 nltk==3.5 torch==1.4.0 torchvision==0.5.0 \
numpy pandas matplotlib
# kerasのバージョンはこれじゃないとエラーが出るはず

CMD ["python3", "main.py"]