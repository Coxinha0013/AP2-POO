from locadora import (
    FitaCassete, 
    Cliente, 
    ErroLocacao 
)
from datetime import datetime, timedelta 

def main():
    print("==============================================")
    print("--- 📼 Locadora de Fita Cassete! 📼 ---")
    print("==============================================")
    
    print("\n[CONFIGURAÇÃO] Cadastrando fitas no sistema...")
    fita_futuro = FitaCassete("De Volta para o Futuro", "Ficção", "DVF001", dias_emprestimo=3)
    fita_caca = FitaCassete("Os Caça-Fantasmas", "Comédia", "CFA001", dias_emprestimo=3)
    fita_top = FitaCassete("Top Gun - Ases Indomáveis", "Ação", "TOP001", dias_emprestimo=2)
    fita_jones = FitaCassete("Indiana Jones", "Aventura", "IND001", dias_emprestimo=3)
    
    print(fita_futuro)
    print(fita_caca)
    print(fita_top)
    print(fita_jones)
    
    print("\n[CONFIGURAÇÃO] Cadastrando clientes no sistema...")
    cliente_carlos = Cliente("Carlos", "RA001", limite_fitas=3)
    cliente_ana = Cliente("Ana", "RA002", limite_fitas=2) # Ana tem limite menor
    
    print(cliente_carlos)
    print(cliente_ana)

    print("\n==============================================")
    print("--- SIMULAÇÃO ---")
    print("==============================================")
    

    print("\n[Cena 1] Carlos aluga 'De Volta para o Futuro' (Sucesso) ---")
    try:
        cliente_carlos.pegar_emprestado(fita_futuro)
        print(f"Estado atual da fita: {fita_futuro}")
        print(f"Estado atual do cliente: {cliente_carlos}")
    except ErroLocacao as e:
        print(f"FALHA NA LOCAÇÃO: {e}")
        
    print("\n[Cena 2] Ana tenta alugar a mesma fita (Erro Esperado) ---")
    try:
        cliente_ana.pegar_emprestado(fita_futuro)
    except ErroLocacao as e:
        print(f"FALHA NA LOCAÇÃO: {e}") 
        
    print("\n[Cena 3] Ana aluga 2 fitas e tenta a 3ª (Erro Esperado) ---")
    try:
        print("[Ana] Pegando 'Caça-Fantasmas' (1/2)...")
        cliente_ana.pegar_emprestado(fita_caca)
        print("[Ana] Pegando 'Top Gun - Ases Indomáveis' (2/2)...")
        cliente_ana.pegar_emprestado(fita_top)
        print(f"Estado atual da cliente: {cliente_ana}")
        
        print("\n[Ana] Tentando pegar 'Indiana Jones' (3/2)...")
        cliente_ana.pegar_emprestado(fita_jones) 
    except ErroLocacao as e:
        print(f"FALHA NA LOCAÇÃO: {e}") 
        
    print("\n[Cena 4] Carlos tenta devolver 'Indiana Jones' (Erro Esperado) ---")
    try:
        print(f"[Carlos] Tentando devolver '{fita_jones.titulo}' (que ele não pegou)...")
        cliente_carlos.devolver_fita(fita_jones)
    except ErroLocacao as e:
        print(f"FALHA NA DEVOLUÇÃO: {e}")

    print("\n[Cena 5] Carlos devolve 'De Volta para o Futuro' COM ATRASO (Multa) ---")
    try:
        print(f"[SIMULANDO] O tempo passou... A fita de Carlos está 5 dias atrasada.")

        fita_futuro.data_devolucao_prevista = datetime.now() - timedelta(days=5)
        
        print(f"[Carlos] Devolvendo '{fita_futuro.titulo}'...")
        multa = cliente_carlos.devolver_fita(fita_futuro)
        
        print(f"Multa paga: R$ {multa:.2f}")
        print(f"Estado atual da fita: {fita_futuro}")
        print(f"Estado atual do cliente: {cliente_carlos}")
    except ErroLocacao as e:
        print(f"FALHA NA DEVOLUÇÃO: {e}")
        
    print("\n==============================================")
    print("--- FIM DA SIMULAÇÃO ---")
    print("==============================================")

if __name__ == "__main__":
    main()