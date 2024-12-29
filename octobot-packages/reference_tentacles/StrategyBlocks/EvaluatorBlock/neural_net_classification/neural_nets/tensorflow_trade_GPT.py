# a42.ch CONFIDENTIAL
# __________________
#
#  [2021] - [∞] a42.ch Incorporated
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of a42.ch Incorporated and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to a42.ch Incorporated
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from a42.ch Incorporated.
#
# If you want to use any code for commercial purposes,
# or you want your own custom solution,
# please contact me at max@a42.ch

import torch
import torch.nn as nn
import torch.optim as optim

from tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets import (
    abstract_tensorflow_neural_net,
)
import tentacles.StrategyBlocks.EvaluatorBlock.neural_net_classification.neural_nets.abstract_neural_net as abstract_neural_net
import tentacles.Meta.Keywords.basic_tentacles.matrix_basic_keywords.tools.utilities as utilities


class TradeGptModel(nn.Module):
    def __init__(self, features_count, max_bars_back, network_size):
        super(TradeGptModel, self).__init__()
        self.max_bars_back = max_bars_back
        self.input_shape = (self.max_bars_back, features_count)
        if network_size == abstract_neural_net.NETWORK_SIZE_DEEP:
            num_layers = 12
            hidden_size = 768
            num_heads = 12
            ff_dim = 3072
            dropout_prob = 0.1
        elif network_size == abstract_neural_net.NETWORK_SIZE_VERY_DEEP:
            num_layers = 24
            hidden_size = 1024
            num_heads = 16
            ff_dim = 4096
            dropout_prob = 0.1
        elif network_size == abstract_neural_net.NETWORK_SIZE_SUPER_DEEP:
            num_layers = 32
            hidden_size = 1280
            num_heads = 20
            ff_dim = 5120
            dropout_prob = 0.1
        else:
            raise ValueError("Invalid network size.")

        # Positional Encoding
        self.positional_encoding = PositionalEncoding(hidden_size, max_bars_back)

        # Transformer Encoder Layers
        encoder_layers = nn.TransformerEncoderLayer(
            hidden_size, num_heads, dim_feedforward=ff_dim, dropout=dropout_prob
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)

        # Fully connected layer for classification
        self.fc = nn.Linear(
            hidden_size, 3
        )  # 3 classes for classification (Long, Short or Neutral)

    def forward(self, x):
        # Positional Encoding
        x = self.positional_encoding(x)

        # Transformer Encoder
        x = self.transformer_encoder(x)

        # Global average pooling
        x = torch.mean(x, dim=1)

        # Classification
        x = self.fc(x)

        return x

    def save_weights(self, filepath):
        torch.save(self.state_dict(), filepath)

    def load_weights(self, filepath):
        self.load_state_dict(torch.load(filepath))

    def predict(self, x):
        self.eval()  # Set model to evaluation mode
        with torch.no_grad():
            output = self(x)
            _, predicted = torch.max(output, 1)
        return predicted

    def fit(
        self,
        training_indicator_data,
        training_predictions,
        epochs,
        learning_rate_init,
        validation_data,
        batch_size,
    ):
        class TrainDataset(torch.utils.data.Dataset):
            def __init__(self, indicator_data, predictions):
                self.indicator_data = indicator_data
                self.predictions = predictions

            def __len__(self):
                return len(self.indicator_data)

            def __getitem__(self, idx):
                return self.indicator_data[idx], self.predictions[idx]

        train_loader = torch.utils.data.DataLoader(
            TrainDataset(training_indicator_data, training_predictions),
            batch_size=batch_size,
            shuffle=True,
        )

        # Define loss function and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.parameters(), lr=learning_rate_init)
        self.train()  # Set model to training mode
        for epoch in range(epochs):
            running_loss = 0.0
            for inputs, labels in train_loader:
                optimizer.zero_grad()
                outputs = self(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
            print(f"Epoch {epoch+1}, Loss: {running_loss}")
        print("Training finished")

    def summary(self):
        print(self)
        print("\n")
        print("Input shape:", self.input_shape)
        print("\n")
        summary = []
        total_params = 0
        for name, param in self.named_parameters():
            if param.requires_grad:
                summary.append(
                    (name, param.data.size(), sum(p.numel() for p in param.data))
                )
                total_params += sum(p.numel() for p in param.data)
        print("Model Summary:")
        print("Layer Name\t\t\t\t\t\tShape\t\t\t\t\t\tParameters")
        print("=" * 100)
        for layer in summary:
            print("{:<60} {:<25} {:<15}".format(layer[0], str(layer[1]), layer[2]))
        print("=" * 100)
        print(f"Total Trainable Parameters: {total_params}")


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len):
        super(PositionalEncoding, self).__init__()
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float()
            * (-torch.log(torch.tensor(10000.0)) / d_model)
        )
        self.register_buffer("positional_encoding", torch.zeros(max_len, d_model))
        self.positional_encoding[:, 0::2] = torch.sin(position * div_term)
        self.positional_encoding[:, 1::2] = torch.cos(position * div_term)

    def forward(self, x):
        output = []
        for sublist in x:
            encoded_sublist = []
            for tensor in sublist:
                # Add positional encoding to each tensor
                encoded_tensor = tensor + self.positional_encoding
                encoded_sublist.append(encoded_tensor)
            output.append(encoded_sublist)
        return output


class TensorflowTradeGPT(abstract_tensorflow_neural_net.AbstractTensorflowNeuralNet):
    NEURAL_NET_TITLE = "TensorFlow Trade GPT"
    MESSAGE_PRINT_PREFIX = f" {NEURAL_NET_TITLE} - "
    NEURAL_NETS_FOLDER_NAME = "tensorflow_trade_GPT"
    model: TradeGptModel

    NETWORK_SIZES: list = [
        abstract_neural_net.NETWORK_SIZE_DEEP,
        abstract_neural_net.NETWORK_SIZE_VERY_DEEP,
        abstract_neural_net.NETWORK_SIZE_SUPER_DEEP,
    ]

    def create_model(
        self,
        batch_size: int,
        learning_rate_init: float,
        n_iter_no_change: int,
        features_count: int,
    ) -> None:
        self.model = TradeGptModel(
            features_count=features_count,
            max_bars_back=self.max_bars_back,
            network_size=self.network_size,
        )

    def train_model_epoch(
        self,
        training_indicator_data,
        training_predictions,
        testing_indicator_data,
        testing_prediction_data,
        epoch_print_prefix: str,
        batch_size: int,
        learning_rate_init: float,
        epochs: int,
        callbacks,
    ):
        m_time = utilities.start_measure_time(
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Training model"
        )
        self.model.fit(
            training_indicator_data,
            training_predictions,
            epochs=epochs,
            learning_rate_init=learning_rate_init,
            validation_data=(testing_indicator_data, testing_prediction_data),
            batch_size=batch_size,
            # use_multiprocessing=True,
        )
        utilities.end_measure_time(
            m_time,
            f"{self.MESSAGE_PRINT_PREFIX}{epoch_print_prefix}Training model",
        )

    def compile_model(self, learning_rate_init):
        pass

    def get_training_callbacks(
        self,
        learning_rate_init,
        tentacles_setup_config,
        enable_tensorboard,
        epochs,
        prev_val_loss,
        save_model_based_on: str,
    ):
        pass
