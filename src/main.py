import time

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.future import select as future_select

from . import schemas
from .database import SessionLocal
from .models import Cliente, Transacao

app = FastAPI()


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.post("/clientes/{cliente_id}/transacoes", response_model=schemas.ClienteBase)
async def post_transacao(
    cliente_id: int,
    transacao: schemas.TransactionBase,
    session: Session = Depends(get_session),
):

    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Process transaction
    if transacao.tipo == "d":
        if cliente.saldo - transacao.valor < -cliente.limite:
            raise HTTPException(status_code=422, detail="Saldo insuficiente")
        cliente.saldo -= transacao.valor
    else:
        cliente.saldo += transacao.valor

    session.add(Transacao(**transacao.model_dump(), cliente_id=cliente_id))
    session.commit()

    return cliente


@app.get("/clientes/{id}/extrato")
async def get_extrato(id: int, session: Session = Depends(get_session)):
    """Optimized statement for fetching the last 10 transactions."""

    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    transactions_query = (
        future_select(Transacao)
        .filter(Transacao.cliente_id == id)
        .order_by(Transacao.id.desc())
        .limit(10)
    )
    transactions = session.execute(transactions_query)

    return {
        "saldo": {
            "total": cliente.saldo,
            "data_extrato": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "limite": cliente.limite,
        },
        "ultimas_transacoes": [
            schemas.Transaction.model_validate(t) for t in transactions.scalars()
        ],
    }
