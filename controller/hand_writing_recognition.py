# Import Tensorflow libraries 
import tensorflow as tf

# Tensorflow 
# We can build machine learning model by it.
# We use it to train model.

# The MNIST dataset from Keras
# Contains 60,000 images for training. 
# Contains 10,000 images for testing.
# From zero to nine
# The Handwritten Digits Images Are Represented As A 28×28 Matrix Where Each Cell Contains Grayscale Pixel Value.

# Load and preprocess the training data
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Neural Network required input rang (0 : 1);
# Our photos is Grayscale so we will covert it (float32) then (/ 255)
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Build the CNN model
model = tf.keras.Sequential([
    # Convert (28, 28) to (28, 28, 1) -> (1) color channel.
    tf.keras.layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    # We use Activation Function (Rectified) 
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    # max value in window 2 * 2
    tf.keras.layers.MaxPooling2D((2, 2)),
    # convert from matrix to array
    tf.keras.layers.Flatten(),
    # We use Activation Function (Rectified) by 64 unit
    tf.keras.layers.Dense(64, activation='relu'),
    # We use Activation Function (softmax) by 10 unit
    tf.keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=20)

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(x_test, y_test)
print('Test accuracy:', test_acc)

# Save The Model
model.save('model.h5')

# import matplotlib.pyplot as plt

# Use the model to classify new images
# predictions = model.+(x_test)
# predicted_labels = np.argmax(predictions, axis=1)

# # Plot some examples of the model's predictions
# for i in range(10):
#     plt.imshow(x_test[i], cmap='gray')
#     plt.title('Predicted: {}'.format(predicted_labels[i]))
#     plt.show()