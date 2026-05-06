from sqlalchemy import String, Integer, Float, Column, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dataclasses import dataclass


class Base(DeclarativeBase):
    pass

@dataclass
class Produto(Base):
    __tablename__ = 'Produtos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f'<Produto(nome="{self.nome}", preco="{self.preco}", quantidade"{self.quantidade}")>'

@dataclass
class Cliente(Base):
    __tablename__ = 'Cliente'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    
    def __repr__(self):
        return f'<Cliente(nome="{self.nome}", email="{self.email}")>'

engine = create_engine('sqlite:///mercado_legal.db', echo=True)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print('Arquivo "mercado_legal" criado com sucesso!')