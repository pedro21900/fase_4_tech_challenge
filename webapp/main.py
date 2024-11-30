import logging
from typing import List

from fastapi import FastAPI, Body
from starlette.responses import JSONResponse

from webapp.ml_model import predict_price as predict_price_model
from webapp.schemas import PredictPrice

# Inicializando o aplicativo FastAPI
app = FastAPI(root_path="/tech-challenge-fase-3")
logging.basicConfig(level=logging.INFO)

@app.post("/api/predict")
async def predict_price_endpoint(predict_price_input: List[List[PredictPrice]] = Body(
    ...,
    example=[
        [
            {
                "quilate": 0.23,
                "lg_topo": 55.0,
                "x": 3.95,
                "y": 3.98,
                "z": 2.43
            }
        ]
    ]
)) -> JSONResponse:
    """
    Endpoint para prever o preço com base nas características fornecidas.

    Args:
        predict_price_input (List[List[PredictPrice]]): Dados de entrada para previsão.

    Returns:
        JSONResponse: Resposta JSON contendo o preço previsto.
    """
    try:
        preco = predict_price_model(predict_price_input)
        logging.info("Previsão de preço realizada com sucesso.")
        return JSONResponse(status_code=200, content={"preco": preco.tolist()})
    except Exception as e:
        logging.error(f"Erro ao realizar a previsão de preço: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
