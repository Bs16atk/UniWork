import geneticalgorithm as ga
import numpy as numpy
from random import random
from random import randrange


class MLP(object):
    """A Multilayer Perceptron class.
    """

    def __init__(self, noinputs, hidden, nooutputs):
        """Constructor for the MLP. Takes the number of inputs,
            a variable number of hidden layers, and number of outputs
        Args:
            noinputs (int): Number of inputs
            hidden (list): A list of ints for the hidden layers
            nooutputs (int): Number of outputs
        """

        self.noinputs = noinputs
        self.hidden = hidden
        self.nooutputs = nooutputs
        weights = []
        derivatives = []
        layeroutputs = []

        # create a generic representation of the layers
        layers = [noinputs] + hidden + [nooutputs]

        #weight matrix at each layer, for each layer, as random arrays
        # create random connection weights for the layers
        for i in range(len(layers) - 1):
            w = numpy.random.rand(layers[i], layers[i + 1])
            weights.append(w)
        
        # save derivatives per layer
        #number of derivatives equal to number of weight matrices, hence the -1, 2D array
        #the matrix
        for i in range(len(layers) - 1):
            d = numpy.zeros((layers[i], layers[i + 1]))
            derivatives.append(d)
        
        # save layeroutputs per layer
        #creating dummy activation array for each layer of zeros,
        #amount of zeros equal to num of neurons in each layer for each layer
        for i in range(len(layers)):
            a = numpy.zeros(layers[i])
            layeroutputs.append(a)
        
        self.weights = weights
        self.derivatives = derivatives
        self.layeroutputs = layeroutputs


    def feedforwards(self, inputs):
        """Computes forward propagation of the network based on input signals.
        Args:
            inputs (ndarray): Input signals
        Returns:
            layeroutputs (ndarray): Output values
        """

        # the input layer activation is just the input itself
        layeroutputs = inputs

        # save the layeroutputs for backpropogation
        self.layeroutputs[0] = layeroutputs

        # iterate through the network layers
        for i, w in enumerate(self.weights):
            # calculate (dot product) matrix multiplication between 
            #previous activation and weight matrix
            thenetworkinputs = numpy.dot(layeroutputs, w)

            # apply sigmoid activation function
            layeroutputs = self.sigmoidfunction(thenetworkinputs)

            # plus one because activation from layer is input for next layer
            # save the layeroutputs for backpropogation
            self.layeroutputs[i + 1] = layeroutputs
        

        # return output layer activation
        return layeroutputs


    def back_propagation(self, errors):
        """Backpropogates an errors signal.
        Args:
            errors (ndarray): The errors to backprop.
        Returns:
            errors (ndarray): The final errors of the input
        """
        sequence = range(len(self.derivatives))
        reversing = reversed(sequence)
        # iterate backwards through the network layers
        for i in reversing:

            # get activation for previous layer
            layeroutputs = self.layeroutputs[i+1]

            # apply sigmoid derivative function
            delta = errors * self.sigmoidsderivatives(layeroutputs)

            # reshape delta as to have it as a 2d array, native method in numpy
            deltareshaping = delta.reshape(delta.shape[0], -1).T

            # get layeroutputs for current layer
            presentactivations = self.layeroutputs[i]

            # reshape layeroutputs as to have them as a 2d column matrix
            presentactivations = presentactivations.reshape(presentactivations.shape[0],-1)
            
            # save derivative after applying matrix multiplication
            self.derivatives[i] = numpy.dot(presentactivations, deltareshaping)

            # backpropogate the next errors
            errors = numpy.dot(delta, self.weights[i].T)


    def train(self, inputs, targets, learning_rate):
        """Trains model running forward prop and backprop
        Args:
            inputs (ndarray): X
            targets (ndarray): Y
            epochs (int): Num. epochs we want to train the network for
            learning_rate (float): Step to apply to gradient descent
        """
        # now enter the training loop
        sum_errors = 0

        # iterate through all the training data
        for j, input1 in enumerate(inputs):
            target = targets[j]
            # activate the network!
            output = self.feedforwards(input1)

            n_particles = input1.shape[0]
            j = [self.feedforwards(input1[i]) for i in range(n_particles)]
            return numpy.array(j)

            errors = target - output

            self.back_propagation(errors)

                # now perform gradient descent on the derivatives
                # (this will update the weights
            self.gradientsdescent(learning_rate)

                # keep track of the MSE for reporting later
            sum_errors += self.mse(target, output)

        # Epoch complete, report the training errors
        print("At Epoch Number" , i+1 , " Error Value Of " , format(sum_errors / len(items)))

    #implenting stochastic gradient descent, an optimisation algorith for minimising the loss of a predictive model.
    def gradientsdescent(self, learningRate=1):
        """Learns by descending the gradient
        Args:
            learningRate (float): How fast to learn.
        """
        # update the weights by stepping down the gradient
        for i in range(len(self.weights)):
            weights = self.weights[i]
            derivatives = self.derivatives[i]
            weights += derivatives * learningRate


    def sigmoidfunction(self, x):
        """Sigmoid activation function
        Args:
            x (float): Value to be processed
        Returns:
            y (float): Output
        """

        y = 1.0 / (1 + numpy.exp(-x))
        return y


    def sigmoidsderivatives(self, x):
        """Sigmoid derivative function
        Args:
            x (float): Value to be processed
        Returns:
            y (float): Output
        """
        return x * (1.0 - x)


    def mse(self, target, output):
        """Mean Squared Error loss function
        Args:
            target (ndarray): The ground trut
            output (ndarray): The predicted values
        Returns:
            (float): Output
        """
        return numpy.average((target - output) ** 2)


if __name__ == "__main__":

    # create a dataset to train a network for the sum operation
    items = numpy.array([[random()/2 for _ in range(2)] for _ in range(1000)])
    targets = numpy.array([[i[0] + i[1]] for i in items])

    # create a Multilayer Perceptron with one hidden layer of 10 neurons
    mlp = MLP(2, [10], 1)

    

    # train network
    numberofepochs = 100
    for i in range(numberofepochs):
            mlp.train(items, targets, 0.1)

    # create testing data
    input1 = numpy.array([0.5, 0.3])

    # get a prediction
    output = mlp.feedforwards(input1)
    multiplier = 10
    print("According to the trained network ", (input1[0]*multiplier), " plus ", (input1[1] *multiplier), " equals ", (output *multiplier))
