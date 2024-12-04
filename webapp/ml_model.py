import torch
import numpy as np
import joblib
from webapp.schemas import PredictPrice
from typing import List


def predict_price(independent_vars: List[List[PredictPrice]]) -> np.ndarray:
    """
    Função para prever o preço de ações usando um modelo LSTM salvo.

    Args:
        independent_vars (List[List[PredictPrice]]): Dados de entrada com os atributos financeiros.

    Returns:
        np.ndarray: Previsões dos preços em valores reais.
    """
    # Caminhos dos arquivos salvos
    model_path = './resources/model.pt'
    scaler_x_path = './resources/scalerX.pkl'
    scaler_y_path = './resources/scalerY.pkl'

    # Carregar o modelo e os escaladores
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LSTMModel()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    scaler_x = joblib.load(scaler_x_path)
    scaler_y = joblib.load(scaler_y_path)

    # Preparar os dados de entrada
    input_array = np.array([extract_attributes(price) for price in independent_vars[0]])
    input_normalized = scaler_x.transform(input_array)
    input_tensor = torch.tensor(input_normalized, dtype=torch.float32).unsqueeze(0).to(device)

    # Fazer a previsão
    with torch.no_grad():
        prediction = model(input_tensor)
        prediction_numpy = prediction.detach().cpu().numpy()
        prediction_real = scaler_y.inverse_transform(prediction_numpy[0])

    return prediction_real


def extract_attributes(prediction: PredictPrice) -> List[float]:
    """
    Extrai os atributos necessários para a previsão a partir de um objeto PredictPrice.

    Args:
        prediction (PredictPrice): Objeto com os atributos adj_close, high, low, open e volume.

    Returns:
        List[float]: Lista com os atributos extraídos na ordem correta.
    """
    return [prediction.adj_close, prediction.high, prediction.low, prediction.open, prediction.volume]


# Classe LSTMModel
class LSTMModel(torch.nn.Module):
    def __init__(self, input_size=5, hidden_size=100, num_layers=4, output_size=1):
        super(LSTMModel, self).__init__()
        self.lstm = torch.nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, output_size)

    def forward(self, x):
        output, _ = self.lstm(x)
        return self.fc(output)