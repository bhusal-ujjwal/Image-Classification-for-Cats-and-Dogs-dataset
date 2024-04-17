# -*- coding: utf-8 -*-
"""Cats and Dogs Dataset Task.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Db4bBpeQFHrry3XqW_m5umtZ4fcOQnDN
"""

import torch.nn as nn

class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()

  # Convolutional layers
    self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding = 1)
    self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding = 1)
    self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding = 1)

  #maxpooling layer
    self.pool = nn.MaxPool2d(kernel_size= 2, stride=2)

  # fully connected layers
    self.fc1 = nn.Linear(64 * 28 * 28, 500)
    self.fc2 = nn.Linear(500, 2)

  #Activation function
    self.relu = nn.ReLU()

  def forward(self , x):
    # Apply convolutional layers
    x = self.conv1(x)
    x = self.relu(x)
    x = self.pool(x)
    x = self.conv2(x)
    x = self.relu(x)
    x = self.pool(x)
    x = self.conv3(x)
    x = self.relu(x)
    x = self.pool(x)

    # Flattening the tensors before applying fully connected layer
    x = x.view(-1 , 64 * 28 * 28)

    # applying the fully connected layers
    x = self.fc1(x)
    x = self.relu(x)
    x = self.fc2(x)

    return x

from google.colab import drive

# Mounting your drive in colab
drive.mount("/content/drive")

# Switching the working directory
import os
os.chdir('/content/drive/MyDrive/cat_dog')

import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# Transforming the images
transform_train = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.transforms.Normalize(mean = [0.485, 0.456, 0.406],
                                    std = [0.229, 0.224, 0.225])

])

import os
print(os.getcwd())

# Loading the data in trainset
trainset = torchvision.datasets.ImageFolder(root = 'train', transform= transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size = 32, shuffle = True, num_workers=2)

# Loading the data in testset
testset = torchvision.datasets.ImageFolder(root = 'train', transform= transform_train)
testloader = torch.utils.data.DataLoader(testset, batch_size = 32, shuffle = False, num_workers=2)

images, labels = next(iter(trainloader))
classes = ("Cat", "Dog")
fig, axs = plt.subplots(1, 3 ,figsize = (10, 15))

for i in range(3):
  img = np.transpose(images[i], (1, 2, 0))
  axs[i].imshow(img)
  axs[i].set_title(str(classes[labels[i].item()]))
  axs[i].axis("off")
plt.show()

# Setting the device on GPU if available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device

# Defining the loss and optimiset
net = Net()
# net = net.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr = 0.001)
net

# Train the network

for epoch in range(10):
  running_loss = 0.0
  for i, data in enumerate(trainloader, 0):
    # get the input: data is list of inputs and labels
    input, labels = data
    # inputs, labels = data[0].to(device), data[1].to(device)


    # Cleainig the gradient
    optimizer.zero_grad()

    # forward + backaward + optimize

    outputs = net(input)
    loss = criterion(outputs, labels)

    loss.backward()
    optimizer.step()

    # Print steps
    running_loss += loss.item()
    if i %200 == 199:
      print("[%d, %d] loss: %.3f" %
            (epoch + 1, i+1, running_loss/200))
      running_loss = 0.0

print("Training done")

# Testing the model

correct = 0
total = 0

with torch.no_grad():
  for data in testloader:
    images, labels = data
    outputs = net(images)
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum().item()
print("Accuracy: ",100* correct/total )

PATH = 'cat_dog.pt'
torch.save(net.state_dict(), PATH)
print('Model saved at ', PATH)

import torch
import torchvision.transforms as transforms
from PIL import Image

# Loading the model
net = Net().to(device)
net.load_state_dict(torch.load(PATH))

from torch.cuda import is_available


def predict(model, input_path):
  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
  transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.transforms.Normalize(mean = [0.485, 0.456, 0.406],
                                    std = [0.229, 0.224, 0.225])
  ])

  model.eval()

  #Load the image
  image = Image.open(input_path)
  image = transform(image).to(device)
  image = image.unsqueeze(0) # Helps model to see images in batches
  with torch.no_grad():
    output = model(image)
    _, predicted = torch.max(output.data, 1) # getting the maximum probability of the class
    return predicted.item()

img = "cat.jpg"
pet = predict(net, img)
print("This animal looks like a", classes[pet])
pet

img = "dog.jpg"
pet = predict(net, img)
print("This animal looks like a", classes[pet])
0