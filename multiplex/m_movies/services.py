from __future__ import print_function
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


os.environ['KMP_DUPLICATE_LIB_OK']='True'

'''
https://arxiv.org/abs/1511.06434
Unsupervised Representation Learning 
with Deep Convolutional Generative Adversarial Networks
Alec Radford, Luke Metz, Soumith Chintala
In recent years, supervised learning with convolutional networks (CNNs) 
has seen huge adoption in computer vision applications. 
Comparatively, unsupervised learning with CNNs has received less attention. 
In this work we hope to help bridge the gap 
between the success of CNNs for supervised learning and unsupervised learning. 
We introduce a class of CNNs called 
deep convolutional generative adversarial networks (DCGANs), 
that have certain architectural constraints, and demonstrate 
that they are a strong candidate for unsupervised learning. 
Training on various image datasets, we show convincing evidence 
that our deep convolutional adversarial pair learns a hierarchy of representations 
from object parts to scenes in both the generator and discriminator. 
Additionally, we use the learned features for novel tasks 
- demonstrating their applicability as general image representations.
'''
class DcGan(object):
    def __init__(self):
        # Root directory for dataset
        self.dataroot = r'C:\Users\AIA\PycharmProjects\djangoRestProject\multiplex\data'
        # number of workers for dataloader
        self.workers = 2
        # Batch size during training
        self.batch_size = 128
        # Spatial size of training images. All images will be resized to this
        #   size using a transformer.
        self.image_size = 64
        # number of channels in the training images. For color images this is 3
        self.nc = 3
        # Size of z latent vector (i.e. size of generator input)
        self.nz = 100
        # Size of feature maps in generator
        self.ngf = 64
        # Size of feature maps in discriminator
        self.ndf = 64
        # number of training epochs
        self.num_epochs = 1
        # Learning rate for optimizers
        self.lr = 0.0002
        # Beta1 hyperparam for Adam optimizers
        self.beta1 = 0.5
        # number of GPUs available. Use 0 for CPU mode.
        self.ngpu = 1
        self.manualSeed = 999
        self.device = None
        self.dataloader = None
        self.netD = None
        self.netG = None

    def hook(self):
        self.show_face()
        self.weights_init()
        self.print_netG()
        self.print_netD()
        self.generate_fake_faces()

    def show_face(self) -> str:
        manualSeed = self.manualSeed
        dataroot = self.dataroot
        image_size = self.image_size
        batch_size = self.batch_size
        workers = self.workers
        ngpu = self.ngpu
        print("Random Seed: ", manualSeed)
        random.seed(manualSeed)
        torch.manual_seed(manualSeed)
        dataset = dset.ImageFolder(root=dataroot,
                                   transform=transforms.Compose([
                                       transforms.Resize(image_size),
                                       transforms.CenterCrop(image_size),
                                       transforms.ToTensor(),
                                       transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                                   ]))

        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size,
                                         shuffle=True, num_workers=workers)
        device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
        real_batch = next(iter(dataloader))
        plt.figure(figsize=(8,8))
        plt.axis("off")
        plt.title("Training Images")
        plt.imshow(np.transpose(vutils.make_grid(real_batch[0].to(device)[:64], padding=2, normalize=True).cpu(),(1,2,0)))
        plt.show()

        self.dataloader = dataloader
        self.device = device

    # custom weights initialization called on netG and netD
    def weights_init(self, m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            nn.init.normal_(m.weight.data, 0.0, 0.02)
        elif classname.find('BatchNorm') != -1:
            nn.init.normal_(m.weight.data, 1.0, 0.02)
            nn.init.constant_(m.bias.data, 0)

    def print_netG(self):
        # Create the generator
        ngpu = self.ngpu
        device = self.device
        netG = Generator(ngpu).to(device)


        # Handle multi-gpu if desired
        if (device.type == 'cuda') and (ngpu > 1):
            netG = nn.DataParallel(netG, list(range(ngpu)))

        # Apply the weights_init function to randomly initialize all weights
        #  to mean=0, stdev=0.02.
        netG.apply(self.weights_init)

        # Print the model

        self.netG = netG
        print(netG)


    def print_netD(self):
        ngpu = self.ngpu
        device = self.device
        # Create the Discriminator
        netD = Discriminator(ngpu).to(device)


        # Handle multi-gpu if desired
        if (device.type == 'cuda') and (ngpu > 1):
            netD = nn.DataParallel(netD, list(range(ngpu)))
        netD.apply(self.weights_init)

        # Print the model
        self.netD = netD
        print(netD)




    def generate_fake_faces(self):
        pass

    def train(self):
        nz = self.nz
        ngpu = self.ngpu
        beta1 = self.beta1
        lr = self.lr
        num_epochs = self.num_epochs
        dataloader = self.dataloader
        netG =self.netG
        netD=self.netD
        device = self.device


        criterion = nn.BCELoss()
        fixed_noise = torch.randn(64, nz, 1, 1, device=device)
        real_label = 1.
        fake_label = 0.
        optimizerD = optim.Adam(netD.parameters(), lr=lr, betas=(beta1, 0.999))
        optimizerG = optim.Adam(netG.parameters(), lr=lr, betas=(beta1, 0.999))

        img_list = []
        G_losses = []
        D_losses = []
        iters = 0
        print("Starting Training Loop...")
        for epoch in range(num_epochs):
            for i, data in enumerate(tqdm(dataloader)):
                netD.zero_grad()
                real_cpu = data[0].to(device)
                b_size = real_cpu.size(0)
                label = torch.full((b_size,), real_label, dtype=torch.float, device=device)
                output = netD(real_cpu).view(-1)
                errD_real = criterion(output, label)
                errD_real.backward()
                D_x = output.mean().item()
                noise = torch.randn(b_size, nz, 1, 1, device=device)
                fake = netG(noise)
                label.fill_(fake_label)
                output = netD(fake.detach()).view(-1)
                errD_fake = criterion(output, label)
                errD_fake.backward()
                D_G_z1 = output.mean().item()
                errD = errD_real + errD_fake
                optimizerD.step()

                netG.zero_grad()
                label.fill_(real_label)  # fake labels are real for generator cost
                output = netD(fake).view(-1)
                errG = criterion(output, label)
                errG.backward()
                D_G_z2 = output.mean().item()
                optimizerG.step()
                if (iters % 500 == 0) or ((epoch == num_epochs - 1) and (i == len(dataloader) - 1)):
                    with torch.no_grad():
                        fake = netG(fixed_noise).detach().cpu()
                    img_list.append(vutils.make_grid(fake, padding=2, normalize=True))

                iters += 1
            # Output training stats
            print('[%d/%d]\tLoss_D: %.4f\tLoss_G: %.4f\tD(x): %.4f\tD(G(z)): %.4f / %.4f'
                  % (epoch, num_epochs, errD.item(), errG.item(), D_x, D_G_z1, D_G_z2))

            # Save Losses for plotting later
            G_losses.append(errG.item())
            D_losses.append(errD.item())

        real_batch = next(iter(dataloader))

        # Plot the real images
        ngpu, workers = 0, 0  # M1 MPS에서 dataloader 오류. CPU로 전환.
        device = self.device

        plt.figure(figsize=(15, 15))
        plt.subplot(1, 2, 1)
        plt.axis("off")
        plt.title("Real Images")
        plt.imshow(
            np.transpose(vutils.make_grid(real_batch[0].to(device)[:64], padding=5, normalize=True).cpu(), (1, 2, 0)))

        # Plot the fake images from the last epoch
        plt.subplot(1, 2, 2)
        plt.axis("off")
        plt.title("Fake Images")
        plt.imshow(np.transpose(img_list[-1], (1, 2, 0)))
        plt.show()

    def my_dlib(self):
        that = MyDlib()
        that.hook()

class Generator(nn.Module):
    def __init__(self, ngpu):
        super(Generator, self).__init__()
        self.ngpu = ngpu
        that = DcGan()
        nz = that.nz
        ngf = that.ngf
        nc = that.nc

        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self, ngpu):
        super(Discriminator, self).__init__()
        self.ngpu = ngpu
        that = DcGan()
        nc = that.nc
        ndf = that.ndf

        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(nc, ndf, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            nn.Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            nn.Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ndf * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            nn.Conv2d(ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        return self.main(input)



import sys
import dlib  # conda install -c conda-forge dlib
import cv2
import openface
'''
mkdir openface
cd openface
git clone https://github.com/cmusatyalab/openface.git ~/openface
cd ./~
cd openface
python setup.py install
'''
class MyDlib(object):
    def __init__(self):
        pass
    def hook(self):
        # http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
        predictor_model = "./files/shape_predictor_68_face_landmarks.dat"
        face_detector = dlib.get_frontal_face_detector() # HOG 이용한 얼굴 감지 클래스 생성 - dlib
        face_pose_predictor = dlib.shape_predictor(predictor_model)
        # 랜드마크를 이용해 얼굴을 정렬할 클래스 생성 - Openface
        face_aligner = openface.AlignDlib(predictor_model)
        image = cv2.imread('../fruits-360-5/lena.jpg')
        detected_faces = face_detector(image, 1)
        for i, face_rect in enumerate(detected_faces):
            print(
                "- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(),
                                                                                   face_rect.top(),
                                                                                   face_rect.right(),
                                                                                   face_rect.bottom()))

            # 얼굴 위치에서 랜드마크 찾기
            pose_landmarks = face_pose_predictor(image, face_rect)

            alignedFace = face_aligner.align(532, image, face_rect,
                                             landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

            cv2.imwrite("./fruits-360-5/aligned_face_{}.jpg".format(i), alignedFace)


def spec(param):
    (lambda x: print(f"--- 1.Shape ---\n{x.shape}\n"
                     f"--- 2.Features ---\n{x.columns}\n"
                     f"--- 3.Info ---\n{x.info}\n"
                     f"--- 4.Case Top1 ---\n{x.head(1)}\n"
                     f"--- 5.Case Bottom1 ---\n{x.tail(3)}\n"
                     f"--- 6.Describe ---\n{x.describe()}\n"
                     f"--- 7.Describe All ---\n{x.describe(include='all')}"))(param)
dc_menu = ["Exit", #0
                "/mplex/m_movies/fake-faces",# 1. Loading CelebA Dataset
                "/mplex/m_movies/find-face",#2.
                ]
dc_lambda = {
    "1" : lambda x: x.hook(),
    "2" : lambda x: x.my_dlib()
}
if __name__ == '__main__':
    dc = DcGan()
    while True:
        [print(f"{i}. {j}") for i, j in enumerate(dc_menu)]
        menu = input('Choose Menu: ')
        if menu == '0':
            print("Exit")
            break
        else:
            try:
                dc_lambda[menu](dc)
            except KeyError as e:
                if 'Some error message' in str(e):
                    print('Caught error message')
                else:
                    print("Didn't catch error message")