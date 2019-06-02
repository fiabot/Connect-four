import pandas
from sklearn.model_selection import train_test_split
import tensorflow as tf

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

"""training_dataset = (
    tf.data.Dataset.from_tensor_slices(
        (
            tf.cast(data_train.values, tf.float32),
            tf.cast(target_train.values, tf.int32)
        )
    )
)"""
"""data_train=tf.convert_to_tensor(data_train)
target_train=tf.convert_to_tensor(target_train)
print(data_train)
print(target_train) """

"""for features_tensor, target_tensor in training_dataset:
    print('features:' ,features_tensor," target:",target_tensor)"""

# Initialize placeholders 
x = tf.placeholder(dtype = tf.float32, shape =[None,42])
y = tf.placeholder(dtype = tf.int32, shape = [None])


# Fully connected layer 
logits = tf.contrib.layers.fully_connected(x, 3, tf.nn.relu)

# Define a loss function
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels = y, 
                                                                    logits = logits))
# Define an optimizer 
train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

# Convert logits to label indexes
correct_pred = tf.argmax(logits, 1)

# Define an accuracy metric
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

tf.set_random_seed(1234)
saver = tf.train.Saver()
sess = tf.Session()

sess.run(tf.global_variables_initializer())
accuracy_val = 5
drop_out = 0.8
i = 0 
for i in range(20000):
        
        _, accuracy_val = sess.run([train_op, accuracy],
                                   feed_dict={x: data_train,y: target_train})
        if i % 20 == 0:
            print('EPOCH', i)
            print("acc_vale: ", accuracy_val)
        i += 1

predicted = sess.run([correct_pred], feed_dict={x: data_test})[0]
print(predicted) 

# Calculate correct matches 
match_count = sum([int(y == y_) for y, y_ in zip(target_test, predicted)])


accuracy = float(match_count) / float(len(target_test))

saver.save(sess, 'my_test_model')

print("Accuracy:" , accuracy)

sess.close()

