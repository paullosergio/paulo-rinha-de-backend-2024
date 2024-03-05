from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Cliente(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    saldo = Column(Integer)
    limite = Column(Integer)
    transacoes = relationship("Transacao", back_populates="cliente")


class Transacao(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clients.id"))
    valor = Column(Integer)
    tipo = Column(String)
    descricao = Column(String)
    realizada_em = Column(DateTime, default=datetime.now())
    cliente = relationship("Cliente", back_populates="transacoes")
