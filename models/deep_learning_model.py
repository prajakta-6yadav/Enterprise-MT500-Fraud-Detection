import numpy as np
import pandas as pd

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Dense
)
from tensorflow.keras.optimizers import Adam

from sklearn.preprocessing import MinMaxScaler


class MT500DeepLearningModel:

    def __init__(self):

        self.scaler = MinMaxScaler()

        self.autoencoder = None

        print(
            "Enterprise Deep Learning Engine Initialized"
        )

    # -----------------------------------
    # Prepare Features
    # -----------------------------------

    def prepare_features(
        self,
        df
    ):

        numeric_columns = df.select_dtypes(
            include=["int64", "float64"]
        ).columns

        X = df[numeric_columns]

        X = X.fillna(0)

        X_scaled = self.scaler.fit_transform(X)

        return X_scaled

    # -----------------------------------
    # Build Autoencoder
    # -----------------------------------

    def build_autoencoder(
        self,
        input_dim
    ):

        input_layer = Input(
            shape=(input_dim,)
        )

        encoder = Dense(
            32,
            activation="relu"
        )(input_layer)

        encoder = Dense(
            16,
            activation="relu"
        )(encoder)

        decoder = Dense(
            32,
            activation="relu"
        )(encoder)

        decoder = Dense(
            input_dim,
            activation="sigmoid"
        )(decoder)

        autoencoder = Model(
            inputs=input_layer,
            outputs=decoder
        )

        autoencoder.compile(

            optimizer=Adam(
                learning_rate=0.001
            ),

            loss="mse"
        )

        self.autoencoder = autoencoder

    # -----------------------------------
    # Train
    # -----------------------------------

    def train(
        self,
        dataset_path
    ):

        X_scaled = dataset_path

        self.build_autoencoder(
            X_scaled.shape[1]
        )

        self.autoencoder.fit(

            X_scaled,
            X_scaled,

            epochs=10,

            batch_size=32,

            validation_split=0.2,

            verbose=1
        )

        print(
            "\nDeep Learning Autoencoder Training Complete"
        )

    # -----------------------------------
    # Detect Anomalies
    # -----------------------------------

    def detect_anomalies(         
        self,
        dataset_path
    ):

        df = pd.read_csv(
            dataset_path
        )

        X_scaled = self.prepare_features(df)
        if self.autoencoder is None:

            self.build_autoencoder(
                X_scaled.shape[1]
            )

            self.train(
                X_scaled
            )

        reconstructed = (
            self.autoencoder.predict(
                X_scaled
            )
        )

        reconstruction_error = np.mean(

            np.square(
                X_scaled - reconstructed
            ),

            axis=1
        )

        threshold = np.percentile(
            reconstruction_error,
            95
        )

        anomalies = (
            reconstruction_error > threshold
        )

        print("\nAnomaly Detection Complete")

        print(
            "Detected Anomalies:",
            anomalies.sum()
        )

        return anomalies