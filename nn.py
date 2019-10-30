import numpy as np
import tensorflow as tf
from constants import *


class PolicyNet:
    def __init__(self, model=None):
        # >>> input layer
        # use the positions of the black and white stones, the last place and the side
        # of the last place as the input, 4 layers in total
        self.input = tf.keras.backend.placeholder(dtype=tf.float32,
                                                  shape=(None, SIZE, SIZE, 4))
        # <<< input layer

        # >>> convolution layers
        self.conv1 = tf.keras.layers.Convolution2D(inputs=self.input,
                                                   filter=16, kernal_size=[3, 3],
                                                   padding='same',
                                                   data_format='channels_last',
                                                   activation=tf.nn.relu)
        self.conv2 = tf.keras.layers.Convolution2D(inputs=self.conv1,
                                                   filter=32, kernal_size=[3, 3],
                                                   padding='same',
                                                   data_format='channels_last',
                                                   activation=tf.nn.relu)
        self.conv3 = tf.keras.layers.Convolution2D(inputs=self.conv2,
                                                   filter=64, kernal_size=[3, 3],
                                                   padding='same',
                                                   data_format='channels_last',
                                                   activation=tf.nn.relu)
        # <<< convolution layers

        # >>> action network
        # this network gives the prior probabilities of choosing different actions
        self.action_conv = tf.keras.layers.Convolution2D(inputs=self.conv3,
                                                         filters=4, kernel_size=[1, 1],
                                                         padding='same',
                                                         data_format='channels_last',
                                                         activation=tf.nn.relu)

        # flatten
        self.action_flatten = tf.reshape(self.action_conv, [-1, SIZE ** 2 * 4])

        self.action_prior_probabilities = tf.keras.layers.Dense(inputs=self.action_flatten,
                                                                units=SIZE ** 2,
                                                                activation=tf.nn.log_softmax)
        # <<< action network

        # >>> evaluation network
        # this network gives the evaluation of the node
        self.evaluation_conv = tf.keras.layers.Convolution2D(inputs=self.conv3,
                                                             filters=2, kernel_size=[1, 1],
                                                             padding='same',
                                                             data_format='channel_last',
                                                             avtivation=tf.nn.relu)

        # flatten
        self.evaluation_flatten = tf.reshape(self.evaluation_conv, [-1, SIZE ** 2 * 2])

        self.evaluation_fc1 = tf.keras.layers.Dense(inputs=self.evaluation_flatten,
                                                    units=SIZE ** 2,
                                                    activation=tf.nn.relu)
        self.evaluation_fc2 = tf.keras.layers.Dense(inputs=self.evaluation_fc1,
                                                    units=1,
                                                    activation=tf.nn.tanh)
        # <<< evaluation network

        # >>> loss function
        # win - lose
        self.labels = tf.keras.backend.placeholder(tf.float32, shape=(None, 1))

        # value loss
        self.value_loss = tf.keras.losses.MSE(self.labels, self.evaluation_fc2)

        # prior probabilities
        self.prior_probabilities = tf.keras.backend.placeholder(tf.float32,
                                                                shape=(None, SIZE ** 2))

        # policy loss
        self.policy_loss = tf.negative(tf.reduce_mean(
            tf.reduce_sum(tf.multiply(self.prior_probabilities, self.action_prior_probabilities), 1)
        ))

        # l2 normalization
        self.l2 = L2_BETA * tf.add_n(
            [tf.nn.l2_loss(x) for x in tf.trainable_variables()
             if 'bias' not in x.name.lower()]
        )

        # loss
        self.loss = self.value_loss + self.policy_loss + self.l2
        # <<< loss function

        # >>> optimizer
        self.learning_rate = tf.keras.backend.placeholder(tf.float32)
        self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
        # <<< optimizer

        # >>> session
        self.session = tf.compat.v1.Session()
        init = tf.compat.v1.global_variables_initializer()



# testing
if __name__ == "__main__":
    print(tf.__version__)