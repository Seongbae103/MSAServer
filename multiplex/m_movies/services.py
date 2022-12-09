from __future__ import print_function
import argparse
import os
import random
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
from tqdm import tqdm

DCGAN_MENUS = ["종료", #0
                "시드",
               "이미지 출력"] #1
dcgan_menu = {
    "1" : lambda t: t.manualseed(),
    "2" : lambda t: t.showceleba()
}

class DcGan(object):
    def __init__(self):
        self.dataroot = "../data/celeba/"
        self.workers = 2
        self.batch_size = 128
        self.image_size = 64
        self.nc = 3
        self.nz = 100
        self.ngf = 64
        self.ndf = 64
        self.num_epochs = 10
        self.lr = 0.0002
        self.beta1 = 0.5
        self.ngpu = 1

    def showceleba(self):
        manualSeed = 999
        print("Random Seed: ", manualSeed)
        random.seed(manualSeed)
        torch.manual_seed(manualSeed)
        dataset = dset.ImageFolder(root=self.dataroot,
                                   transform=transforms.Compose([
                                       transforms.Resize(self.image_size),
                                       transforms.CenterCrop(self.image_size),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                                   ]))
        # Create the dataloader
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=self.batch_size,
                                                 shuffle=True, num_workers=self.workers)

        # Decide which device we want to run on
        device = torch.device("cuda:0" if (torch.cuda.is_available() and self.ngpu > 0) else "cpu")

        # Plot some training images
        # real_batch = next(iter(dataloader))
        # plt.figure(figsize=(8,8))
        # plt.axis("off")
        # plt.title("Training Images")
        # plt.imshow(np.transpose(vutils.make_grid(real_batch[0].to(device)[:64], padding=2, normalize=True).cpu(),(1,2,0)))

# custom weights initialization called on netG and netD
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        nn.init.normal_(m.weight.data, 1.0, 0.02)
        nn.init.constant_(m.bias.data, 0)

def my_menu(ls):
    for i, j in enumerate(ls):
        print(f"{i}. {j}")
    return input('메뉴선택: ')

if __name__ == '__main__':
    t = DcGan()
    while True:
        menu = my_menu(DCGAN_MENUS)
        if menu == '0':
            print("종료")
            break
        else:
            try:
                dcgan_menu[menu](t)
            except KeyError:
                print(" ### Error ### ")



# 1. 이미지 보기