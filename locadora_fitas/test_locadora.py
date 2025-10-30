import pytest
from datetime import datetime, timedelta

from locadora import (
    FitaCassete, 
    Cliente, 
    ErroLocacao, 
    FitaIndisponivelError, 
    FitaNaoAlugadaError, 
    LimiteAlugueisError
)

@pytest.fixture
def cliente_padrao():

    return Cliente(nome="Carlos", id_cliente="RA001", limite_fitas=3)

@pytest.fixture
def fita_disponivel():
   
    return FitaCassete(
        titulo="De Volta para o Futuro", 
        genero="Ficção", 
        codigo="DVF001",
        dias_emprestimo=3, 
        multa_diaria=1.00    
    )

@pytest.fixture
def lista_de_fitas():
    return [
        FitaCassete(titulo="Fita 1", genero="A", codigo="F1"),
        FitaCassete(titulo="Fita 2", genero="B", codigo="F2"),
        FitaCassete(titulo="Fita 3", genero="C", codigo="F3"),
        FitaCassete(titulo="Fita 4", genero="D", codigo="F4")
    ]


def test_cliente_aluga_fita_com_sucesso(cliente_padrao, fita_disponivel):
    
    cliente_padrao.pegar_emprestado(fita_disponivel)
    
    assert fita_disponivel.disponivel == False
    assert fita_disponivel in cliente_padrao.fitas_alugadas
    assert len(cliente_padrao.fitas_alugadas) == 1
    assert fita_disponivel.data_aluguel is not None
    assert fita_disponivel.data_devolucao_prevista is not None

def test_cliente_devolve_fita_com_sucesso(cliente_padrao, fita_disponivel):

    cliente_padrao.pegar_emprestado(fita_disponivel)
    
    multa_recebida = cliente_padrao.devolver_fita(fita_disponivel)
    
    assert fita_disponivel.disponivel == True
    assert fita_disponivel not in cliente_padrao.fitas_alugadas
    assert len(cliente_padrao.fitas_alugadas) == 0
    assert multa_recebida == 0.0 

def test_erro_ao_tentar_alugar_fita_indisponivel(cliente_padrao, fita_disponivel):

    cliente_ana = Cliente(nome="Ana", id_cliente="RA002")
    
    cliente_padrao.pegar_emprestado(fita_disponivel)
    
    with pytest.raises(FitaIndisponivelError):
        cliente_ana.pegar_emprestado(fita_disponivel)

def test_erro_ao_exceder_limite_de_emprestimos(cliente_padrao, lista_de_fitas):
    cliente_padrao.pegar_emprestado(lista_de_fitas[0])
    cliente_padrao.pegar_emprestado(lista_de_fitas[1])
    cliente_padrao.pegar_emprestado(lista_de_fitas[2])
    
    with pytest.raises(LimiteAlugueisError):
        cliente_padrao.pegar_emprestado(lista_de_fitas[3])

def test_erro_ao_devolver_fita_nao_alugada_pelo_cliente(cliente_padrao, fita_disponivel):
    with pytest.raises(FitaNaoAlugadaError):
        cliente_padrao.devolver_fita(fita_disponivel)
        
def test_erro_ao_devolver_fita_que_ja_esta_disponivel(cliente_padrao, fita_disponivel):
    cliente_padrao.pegar_emprestado(fita_disponivel)
    cliente_padrao.devolver_fita(fita_disponivel)
    
    with pytest.raises(FitaNaoAlugadaError):
        cliente_padrao.devolver_fita(fita_disponivel)

def test_calculo_de_multa_por_atraso(cliente_padrao, fita_disponivel):
    cliente_padrao.pegar_emprestado(fita_disponivel)

    fita_disponivel.data_devolucao_prevista = datetime.now() - timedelta(days=5)
    
    multa_recebida = cliente_padrao.devolver_fita(fita_disponivel)
    
    assert multa_recebida == 5.00