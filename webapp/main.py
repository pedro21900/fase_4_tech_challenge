from typing import List

from fastapi import FastAPI, Body
from starlette.responses import JSONResponse

from webapp.ml_model import predict_price
from webapp.schemas import PredictPrice

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.post("/api/predict")
async def predict_price_endpoint(predict_price_input: List[List[PredictPrice]] = Body(
    ...,
    example=[
        [
            {
                "adj_close": 150.34,
                "high": 155.00,
                "low": 149.50,
                "open": 152.00,
                "volume": 2500000
            }
        ]
    ]
)):
    """
    Endpoint para prever o preço de fechamento de ações.

    Args:
        predict_price_input (List[List[PredictPrice]]): Dados financeiros de entrada.

    Returns:
        JSONResponse: Resposta com o preço previsto.
    """
    try:
        preco = predict_price(predict_price_input)
        return JSONResponse(status_code=200, content={"preco": preco.tolist()})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/health")
async def health_check():
    return {"status": "ok"}