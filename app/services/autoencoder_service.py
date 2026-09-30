
import importlib.util


def tensorflow_available():

    return (
        importlib.util.find_spec(
            "tensorflow"
        ) is not None
    )


def build_autoencoder(
    input_dimension,
    encoding_dimension=8
):

    if not tensorflow_available():
        raise ImportError(
            "TensorFlow is not installed. "
            "Autoencoder is optional."
        )

    from tensorflow.keras import Model
    from tensorflow.keras.layers import (
        Input,
        Dense
    )

    inputs = Input(
        shape=(input_dimension,)
    )

    encoded = Dense(
        encoding_dimension,
        activation="relu"
    )(inputs)

    decoded = Dense(
        input_dimension,
        activation="linear"
    )(encoded)

    model = Model(
        inputs,
        decoded
    )

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    return model
