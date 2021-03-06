from tensorflow.keras import backend as K
from tensorflow.python.keras.engine import Layer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Dense, Activation, Input, Concatenate, Lambda
# from tensorflow.keras.layers import LSTM, GRU, CuDNNLSTM, CuDNNGRU, Dropout
# from tensorflow.keras.layers import Reshape, LeakyReLU, ZeroPadding2D
# from tensorflow.keras.layers import Conv1D, Add, Conv2D, UpSampling2D
# from keras.layers.wrappers import Bidirectional
# from tensorflow.keras.layers import Bidirectional
# from keras.layers.normalization import BatchNormalization
# from tensorflow.keras.layers import BatchNormalization
# from keras.layers.embeddings import Embedding
# from tensorflow.keras.layers import Embedding
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.xception import Xception
import tensorflow.keras
from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.backend import tf as ktf
from config import cfg
from dataset import TextDataset
from generator import DataGenerator
from model import *
from model_load import model_create
from keras.losses import categorical_crossentropy, binary_crossentropy
import torchvision.transforms as transforms
from copy import deepcopy
from keras.preprocessing.image import load_img
import matplotlib.pyplot as plt
from tqdm import tqdm


def main():
    print("BRANCH_NUM ?: ", end="")
    branch_num = int(input())
    print("MAX_EPOCH ?: ", end="")
    max_epoch = int(input())
    
    #DataGenerator
    imsize = cfg.TREE.BASE_SIZE * (2**(branch_num - 1))  #64, 3
    image_transform = transforms.Compose([
        transforms.Resize(int(imsize * 76 / 64)),
        transforms.RandomCrop(imsize),
        transforms.RandomHorizontalFlip()
    ])
    #cfg.DATA_DIR = "data/birds"
    dataset = TextDataset(
        cfg.DATA_DIR,
        "train",
        base_size=cfg.TREE.BASE_SIZE,
        transform=image_transform)
    assert dataset

    traingenerator = DataGenerator(dataset, batchsize=cfg.TRAIN.BATCH_SIZE)

    ##Create model
    G_model, D_model, GRD_model, CR_model, RNN_model = model_create(dataset)
    print("loadmodel_completed")

    #Preparation for learning
    total_epoch = max_epoch
    batch_size = traingenerator.batchsize
    step_epoch = int(len(dataset) / batch_size)
    wrong_step = 3
    wrong_step_epoch = int(step_epoch / wrong_step)

    image_list, captions_ar, captions_ar_prezeropad, \
        z_code, eps_code, mask, keys_list, captions_label, \
            real_label, fake_label = next(traingenerator)
    traingenerator.count = 0
    #for image plot
    test_noise = deepcopy(z_code[:20])
    test_eps = deepcopy(eps_code[:20])
    test_cap_pd = deepcopy(captions_ar_prezeropad[:20])
    test_cap = deepcopy(captions_ar[:20])
    test_mask = deepcopy(mask[:20])
    test_mask = np.where(test_mask == 1, -float("inf"), 0)

    #Start learning
    print("batch_size: {}  step_epoch : {} srong_step_epoch {}".format(
        batch_size, step_epoch, wrong_step_epoch))

    for epoch in range(total_epoch):
        total_D_loss = 0
        total_D_acc = 0
        total_D_wrong_loss = 0
        total_D_wrong_acc = 0
        total_G_loss = 0
        total_G_des_loss = 0
        total_G_enc_loss = 0

        print("----------------EPOCH: {} START----------------".format(epoch))

        for batch in tqdm(range(step_epoch)):

            image_list, captions_ar, captions_ar_prezeropad, \
                z_code, eps_code, mask, keys_list, captions_label, \
                    real_label, fake_label = next(traingenerator)

            mask = np.where(mask == 1, -float("inf"), 0)

            if branch_num == 1:
                real_image = image_list[0]
            if branch_num == 2:
                real_image = image_list[1]
            if branch_num == 3:
                real_image = image_list[2]
            #D learning
            if branch_num == 1:
                fake_image = G_model.predict(
                    [captions_ar_prezeropad, eps_code, z_code])
            else:  # 2 or 3
                fake_image = G_model.predict(
                    [captions_ar_prezeropad, eps_code, z_code, mask])

            if batch % 1 == 0:
                histDr = D_model.train_on_batch(
                    [real_image, captions_ar_prezeropad],
                    [real_label, real_label],
                )
                total_D_loss += histDr[0]
                total_D_acc += (histDr[3] + histDr[4]) / 2

                histDf = D_model.train_on_batch(
                    [fake_image, captions_ar_prezeropad],
                    [fake_label, fake_label],
                )
                total_D_loss += histDf[0]
                total_D_acc += (histDf[3] + histDf[4]) / 2

            if batch % wrong_step == 0:
                histDw = D_model.train_on_batch(
                    [real_image[:-1], captions_ar_prezeropad[1:]],
                    [fake_label[:-1], fake_label[:-1]],
                )
                total_D_wrong_loss += histDw[0]
                total_D_wrong_acc += (histDw[3] + histDw[4]) / 2

            #G learning
            if branch_num == 1:
                histGRD = GRD_model.train_on_batch(
                    [captions_ar_prezeropad, eps_code, z_code, captions_ar],
                    [real_label, real_label, captions_label],
                )
            else:  # 2 or 3
                histGRD = GRD_model.train_on_batch(
                    [captions_ar_prezeropad, eps_code, z_code, mask, captions_ar],
                    [real_label, real_label, captions_label],
                )
            total_G_loss += histGRD[0]
            total_G_des_loss += (histGRD[1] + histGRD[2]) / 2
            total_G_enc_loss += histGRD[3]

        #Calculation of loss
        D_loss = total_D_loss / step_epoch / 2
        D_acc = total_D_acc / step_epoch / 2
        D_wrong_loss = total_D_wrong_loss / wrong_step_epoch
        D_wrong_acc = total_D_wrong_acc / wrong_step_epoch
        G_loss = total_G_loss / step_epoch
        G_des_loss = total_G_des_loss / step_epoch
        G_enc_loss = total_G_enc_loss / step_epoch

        print(
            "D_loss: {:.5f} D_wrong_loss: {:.5f} D_acc:  {:.5f} D_wrong_acc:  {:.5f}"
            .format(D_loss, D_wrong_loss, D_acc, D_wrong_acc))
        print(
            "G_loss:  {:.5f} G_discriminator_loss:  {:.5f} G_encoder_loss:  {:.5f}"
            .format(G_loss, G_des_loss, G_enc_loss))

        if epoch % 4 == 0:
            G_save_path = "model/G_epoch{}.h5".format(epoch)
            G_model.save_weights(G_save_path)
            D_save_path = "model/D_epoch{}.h5".format(epoch)
            D_model.save_weights(D_save_path)

        #Save image
        if epoch % 1 == 0:
            sample_images(branch_num, epoch, test_noise, test_eps, test_cap_pd, test_mask, G_model)


def sample_images(branch_num, epoch, noise, eps, cap_pd, mask, G_model):
    r, c = 5, 4
    if branch_num == 1:
        gen_imgs = G_model.predict([cap_pd, eps, noise])
    else:
        gen_imgs = G_model.predict([cap_pd, eps, noise, mask])
    # Rescale images
    gen_imgs = (gen_imgs * 127.5 + 127.5).astype("int")
    fig, axs = plt.subplots(r, c)
    cnt = 0
    for i in range(r):
        for j in range(c):

            axs[i, j].imshow(gen_imgs[cnt])
            axs[i, j].axis('off')
            cnt += 1
    fig.savefig("gan_img/%d.png" % epoch)
    plt.close()


if __name__ == '__main__':
    main()