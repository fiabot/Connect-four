import pandas
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np

#tf.enable_eager_execution()

#import file
c4_data = pandas.read_csv("c4_data.csv")

#replace strings with numbers 
c4_data =c4_data.replace(to_replace = "b", value = 0)#blank space 
c4_data = c4_data.replace(to_replace = "x", value = 1)#player 1 move
c4_data = c4_data.replace(to_replace = "o", value = 2)#player 2 move 
c4_data = c4_data.replace(to_replace = "win", value = 1)#player 1 won
c4_data = c4_data.replace(to_replace = "loss", value = 2)#player 2 won
c4_data = c4_data.replace(to_replace = "draw", value = 0)#draw

#seperate data and targets
data = c4_data.drop("winner", axis = 1)
target = c4_data['winner']

target= target.astype('int')


#seperate training and test sets
data_train, data_test, target_train, target_test = train_test_split(
    data, target, test_size=0.10, random_state=42)


def multilayer_perceptron(x, weights, biases, keep_prob):
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    layer_1 = tf.nn.dropout(layer_1, keep_prob)
    out_layer = tf.matmul(layer_1, weights['out']) + biases['out']
    return out_layer

n_hidden_1 = 38
n_input = data_train.shape[1]
n_classes = target_train.shape[0]
print(n_input)
print(n_classes) 

weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, n_classes]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

keep_prob = tf.placeholder("float")

training_epochs = 5000
display_step = 1000
batch_size = 32

x = tf.placeholder("float", [None, 42])
y = tf.placeholder("float", [n_classes])

predictions = multilayer_perceptron(x, weights, biases, keep_prob)

cost = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(logits=predictions, labels=y))

optimizer = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)



with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for epoch in range(training_epochs):
        avg_cost = 0.0
        total_batch = int(len(data_train) / batch_size)
        x_batches = np.array_split(data_train, total_batch)
        y_batches = np.array_split(target_train, total_batch)
        for i in range(total_batch):
            batch_x, batch_y = x_batches[i], y_batches[i]
            _, c = sess.run([optimizer, cost], 
                            feed_dict={
                                x: batch_x, 
                                y: batch_y, 
                                keep_prob: 0.8
                            })
            avg_cost += c / total_batch
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", \
                "{:.9f}".format(avg_cost))
    print("Optimization Finished!")
    correct_prediction = tf.equal(tf.argmax(predictions, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: data_test, y: target_test, keep_prob: 1.0}))
