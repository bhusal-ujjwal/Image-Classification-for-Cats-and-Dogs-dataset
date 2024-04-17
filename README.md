# Neural-Network-for-Cats-and-Dogs-dataset
Implement a convolutional neural network (CNN) to classify images of cats and dogs from the Microsoft cats and dogs dataset. 
Also implement a function to test the trained model on new images.

The requirements for the assignment are as follows:
Download the Microsoft cats and dogs dataset from the following link: https://www.microsoft.com/en-us/download/details.aspx?id=54765

Implement a Python class for your CNN. The class should include the following:
3 convolutional layers, each followed by a max pooling layer and ReLU activation function.
A few dense layers, with the final layer being a softmax activation function.
The ability to save and load the trained model.
Train your CNN on the Microsoft cats and dogs dataset.

Implement a function to test your trained model on new images. The function should do the following:

Take an image file path as input.
Load the image and preprocess it.
Use the trained model to classify the image as a cat or dog.
Print a message indicating whether the image is classified as a cat or dog.
