from datetime import datetime, timedelta

class ErroLocacao(Exception):
   
    pass
class FitaIndisponivelError(ErroLocacao):
    
    pass
class FitaNaoAlugadaError(ErroLocacao):
    pass

class LimiteAlugueisError(ErroLocacao):
    pass

class FitaCassete:
    
    def __init__(self, titulo: str, genero: str, codigo: str, dias_emprestimo: int = 3, multa_diaria: float = 1.00):
    
        self.titulo = titulo
        self.genero = genero
        self.codigo = codigo  
        self.disponivel = True 
        
        self.data_aluguel = None
        self.data_devolucao_prevista = None
        
        self.dias_emprestimo = dias_emprestimo
        self.multa_diaria = multa_diaria

    def __str__(self):
    
        status = "Disponível" if self.disponivel else "Alugada"
        return f"Fita: '{self.titulo}' (Código: {self.codigo}) - Status: {status}"

    def alugar(self):

        if not self.disponivel:

            raise FitaIndisponivelError(f"A fita '{self.titulo}' (Código: {self.codigo}) já está alugada.")
        
        self.disponivel = False
        self.data_aluguel = datetime.now() 
        self.data_devolucao_prevista = self.data_aluguel + timedelta(days=self.dias_emprestimo)
        
        print(f"'{self.titulo}' alugada com sucesso.")
        print(f"Devolver até: {self.data_devolucao_prevista.strftime('%d/%m/%Y')}")

    def devolver(self) -> float:
        

        if self.disponivel:
            raise FitaNaoAlugadaError(f"A fita '{self.titulo}' (Código: {self.codigo}) não pode ser devolvida pois já consta como disponível.")
        
        multa_total = 0.0
        
        if datetime.now() > self.data_devolucao_prevista:

            dias_atraso = (datetime.now() - self.data_devolucao_prevista).days
            multa_total = max(0, dias_atraso) * self.multa_diaria
            
        print(f"'{self.titulo}' devolvida.")
        if multa_total > 0:
            print(f"ATENÇÃO: Multa por atraso: R$ {multa_total:.2f}")

        self.disponivel = True
        self.data_aluguel = None
        self.data_devolucao_prevista = None
        
        return multa_total 

class Cliente:
    
    def __init__(self, nome: str, id_cliente: str, limite_fitas: int = 3):

        self.nome = nome
        self.id_cliente = id_cliente 
        
        self.fitas_alugadas = [] 
        
        self.limite_fitas = limite_fitas 

    def __str__(self):
        return f"Cliente: {self.nome} (ID: {self.id_cliente}) - Fitas alugadas: {len(self.fitas_alugadas)}"

    def pegar_emprestado(self, fita: FitaCassete):
        
        if len(self.fitas_alugadas) >= self.limite_fitas:
            raise LimiteAlugueisError(f"Cliente {self.nome} atingiu o limite de {self.limite_fitas} fitas.")
            
        if fita in self.fitas_alugadas:

            raise ErroLocacao(f"Cliente {self.nome} já está com a fita '{fita.titulo}'.")


        fita.alugar() 
        self.fitas_alugadas.append(fita)
        
        print(f"Cliente {self.nome} agora está com '{fita.titulo}'.")

    def devolver_fita(self, fita: FitaCassete):
        
        if fita not in self.fitas_alugadas:
            raise FitaNaoAlugadaError(f"O cliente {self.nome} não pode devolver a fita '{fita.titulo}' pois não a alugou.")
        
        multa = fita.devolver()
        self.fitas_alugadas.remove(fita)
        
        print(f"Cliente {self.nome} não está mais com '{fita.titulo}'.")
        return multa