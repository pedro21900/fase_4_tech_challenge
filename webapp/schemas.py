from typing import Optional
from pydantic import BaseModel


class PredictPrice(BaseModel):
    """
    Modelo de dados utilizado para prever o preço de ações com base em características financeiras.

    Atributos:
        adj_close (Optional[float]): Preço ajustado de fechamento (padrão: None).
        high (Optional[float]): Valor máximo do dia (padrão: None).
        low (Optional[float]): Valor mínimo do dia (padrão: None).
        open (Optional[float]): Preço de abertura (padrão: None).
        volume (Optional[float]): Volume negociado (padrão: None).
    """
    adj_close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    volume: Optional[float] = None
