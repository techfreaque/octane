from tensorflow import keras
from keras import backend


def custom_activation(x):
    # Adjust the output layer activation function
    weights = [1.0, 2.0, 1.0]  # Higher weight for neutral class
    x = backend.exp(x) * weights
    return x / backend.sum(x, axis=-1, keepdims=True)


keras.utils.get_custom_objects()["custom_activation"] = custom_activation
