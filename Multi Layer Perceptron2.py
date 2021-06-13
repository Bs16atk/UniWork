import numpy as numpy 
from random import random
from random import randrange
class MLP(object):

    def __init__(self, noinputs, hidden, nooutputs):
        self.noinputs = noinputs
        self.hidden = hidden
        self.nooutputs = nooutputs
        weights = []
        derivatives = []
        layeroutputs = []

        layers = [noinputs] + hidden + [nooutputs]

        for i in range(len(layers) - 1):
            w = numpy.random.rand(layers[i], layers[i + 1])
            weights.append(w)
        
        for i in range(len(layers) - 1):
            d = numpy.zeros((layers[i], layers[i + 1]))
            derivatives.append(d)
        
        for i in range(len(layers)):
            a = numpy.zeros(layers[i])
            layeroutputs.append(a)
        
        self.weights = weights
        self.derivatives = derivatives
        self.layeroutputs = layeroutputs

    def feedforwards(self, inputs):
        layeroutputs = inputs

        self.layeroutputs[0] = layeroutputs

        for i, w in enumerate(self.weights):
            thenetworkinputs = numpy.dot(layeroutputs, w)

            layeroutputs = self.sigmoidfunction(thenetworkinputs)

            self.layeroutputs[i + 1] = layeroutputs

        return layeroutputs

    def back_propagation(self, errors):
        sequence = range(len(self.derivatives))
        reversing = reversed(sequence)
        for i in reversing:
            layeroutputs = self.layeroutputs[i+1]
            delta = errors * self.sigmoidsderivatives(layeroutputs)
            deltareshaping = delta.reshape(delta.shape[0], -1).T
            presentactivations = self.layeroutputs[i]
            presentactivations = presentactivations.reshape(presentactivations.shape[0],-1)
            self.derivatives[i] = numpy.dot(presentactivations, deltareshaping)
            errors = numpy.dot(delta, self.weights[i].T)


    def train(self, inputs, targets, learning_rate):
        sum_errors = 0

        for j, input1 in enumerate(inputs):
            target = targets[j]
            output = self.feedforwards(input1)

            errors = target - output

            self.back_propagation(errors)

            self.gradientsdescent(learning_rate)

            sum_errors += self.mse(target, output)

        print("At Epoch Number" , i+1 , " Error Value Of " , format(sum_errors / len(items)))

    def gradientsdescent(self, learningRate=1):
        for i in range(len(self.weights)):
            weights = self.weights[i]
            derivatives = self.derivatives[i]
            weights += derivatives * learningRate


    def sigmoidfunction(self, x):
        y = 1.0 / (1 + numpy.exp(-x))
        return y


    def sigmoidsderivatives(self, x):
        return x * (1.0 - x)


    def mse(self, target, output):
        return numpy.average((target - output) ** 2)


if __name__ == "__main__":

    items = numpy.array([[random()/2 for _ in range(2)] for _ in range(1000)])
    targets = numpy.array([[i[0] + i[1]] for i in items])

    mlp = MLP(2, [10], 1)

    numberofepochs = 100
    for i in range(numberofepochs):
            mlp.train(items, targets, 0.1)

    input1 = numpy.array([0.5, 0.3])

    output = mlp.feedforwards(input1)
    multiplier = 10
    print("According to the trained network ", (input1[0]*multiplier), " plus ", (input1[1] *multiplier), " equals ", (output *multiplier))
