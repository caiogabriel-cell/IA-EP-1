import numpy as np
import random
import math
  
class A:
  def __init__(self):
    self.mapa = []
    self.terreno = ["TE","AG","AM","BA"]
    self.jogador = "JO"
    self.posicao = 0
    self.caminho = []
    self.ultimo_mov = [0]
    self.guarda_terreno = ""

  def inicializar(self, mapa = None):
    if (mapa is None):
      self.N = 8
      self.M = 8
      self.tamanho = self.M * self.N
      barreira = 0
      limite_barreira = math.floor((self.tamanho)* 0.1)
      
      for i in range(self.tamanho):
        self.mapa.append("")

      for i in range(self.tamanho):
        escolha = random.choice(self.terreno)
        
        if(escolha == "BA"):
          barreira += 1

        if(barreira > limite_barreira or self.guarda_terreno == escolha):
          while(escolha == "BA"):
            escolha = random.choice(self.terreno)
        
        if(i == self.tamanho-1):
          while(escolha == "BA"):
            escolha = random.choice(self.terreno)
          self.mapa[i] = escolha 
        else:  
          self.mapa[i] = escolha
          self.guarda_terreno = escolha
      
      while(((self.mapa[self.tamanho-2] == "BA") or (self.mapa[self.tamanho -(self.N+2)] == "BA") or (self.mapa[self.tamanho-(self.N+1)] == "BA")) and ((self.mapa[0] == "BA") or (self.mapa[1] == "BA") or (self.mapa[self.N] == "BA") or (self.mapa[self.N+1] == "BA"))):
        for i in range(self.tamanho):
          escolha = random.choice(self.terreno)
          
          if(i == self.tamanho-1):
            while(escolha == "BA"):
              escolha = random.choice(self.terreno)
            self.mapa[i] = escolha 
          else:  
            self.mapa[i] = escolha
        
    else:
      self.mapa = mapa

  def custo(self, proximo_movimento):
    if(proximo_movimento == self.terreno[0]):
      return 1/10
    if(proximo_movimento == self.terreno[1]):
      return 3/10
    if(proximo_movimento == self.terreno[2]):
      return 6/10
    if(proximo_movimento == self.terreno[3]):
      return 1000000

  def distancia_manhattan(self, x, y):
    x_final = self.M -1
    y_final = self.N -1
    resultado = abs(x - x_final) + abs(y - y_final)
    return resultado
    
  def distancia_euclidiana(self, x, y):
    x_final = self.M -1
    y_final = self.N -1
    resultado = np.sqrt(((x - x_final)**2 + (y - y_final)**2))
    return resultado
    
  def heuristica(self, lista_movimento, lista_posicoes, lista_coordenada):
    mov_minimo = ""
    pos_minimo = ""
    heuristica_minimo = 1000.0
    tamanho = len(lista_movimento)
    valor = 0
    
    for j in range(tamanho):
      valor = self.custo(lista_posicoes[j])
      x , y = self.retorna_coordenada(lista_coordenada[j])
      A_manhattan = valor + self.distancia_manhattan(x,y)
      if(A_manhattan < heuristica_minimo):
        heuristica_minimo = A_manhattan
        mov_minimo = lista_movimento[j]
        pos_minimo = lista_posicoes[j]
    
    
    # print("Manhattan")
    # print(A_manhattan)
    
    # for j in range(tamanho):
    #   valor = self.custo(lista_posicoes[j])
    #   x , y = self.retorna_coordenada(lista_coordenada[j])
    #   print(x,y)
    #   A_Euclidiana = valor + self.distancia_euclidiana(x,y)
    #   if(A_Euclidiana < heuristica_minimo):
    #     heuristica_minimo = A_Euclidiana
    #     mov_minimo = lista_movimento[j]
    #     pos_minimo = lista_posicoes[j] 
    
    # print("Euclidiana")
    # print(A_Euclidiana)
        
    return mov_minimo  

  
  def sucessora(self, posicao):
    retorno = []
    
    if(posicao % self.N != 0):
      retorno.append("trás")

    if(posicao >= self.N):
      retorno.append("cima")

    if((posicao+1) % self.N != 0):
      retorno.append("frente")

    if(posicao < self.N * (self.M -1)):
      retorno.append("baixo")

    if(posicao-1 >= self.N and (posicao % self.N != 0)):
      retorno.append("cima-esquerda")

    if((posicao+1 >= self.N) and (posicao+1) % self.N != 0):
      retorno.append("cima-direita") 

    if(posicao % self.N != 0 and (posicao-1 < self.N * (self.M -1))):
      retorno.append("baixo-esquerda") 

    if((posicao+1) % self.N != 0 and (posicao+1 < self.N * (self.M -1))):
      retorno.append("baixo-direita")  
    
    return retorno

  def retorna_estado(self):
    return self.mapa.copy()  

  def retorna_coordenada(self, indice):
    x = math.floor(indice / self.N)
    y = math.floor(indice % self.N)
    return x,y

  
  def jogar(self, posicao, copia):
    lista_movimentos = self.sucessora(posicao)
    lista_posicoes = []
    lista_coordenada = []
    mov_apagar = []
    movimento = ""
    
    for i in lista_movimentos:
      if(i == "frente"):
        posicao += 1
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)
            
      posicao = self.posicao
        
      if(i == "trás"):
        posicao -= 1
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)  
      posicao = self.posicao
              
      if(i == "cima"):
        posicao -= self.N
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)     
      posicao = self.posicao
        
      if(i == "baixo"):
        posicao += self.N
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)
      posicao = self.posicao
              
      if(i == "cima-esquerda"):
        posicao -= (self.N+1)
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)    
      posicao = self.posicao
        
      if(i == "cima-direita"):
        posicao -= (self.N-1)
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)
      posicao = self.posicao
              
      if(i == "baixo-direita"):
        posicao += (self.N+1)
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)
      posicao = self.posicao
        
      if(i == "baixo-esquerda"):
        posicao += (self.N-1)
        lista_coordenada.append(posicao)
        lista_posicoes.append(self.mapa[posicao])
        for j in range(len(self.ultimo_mov)):
          if(posicao == self.ultimo_mov[j]):
            lista_coordenada.remove(posicao)
            lista_posicoes.remove(self.mapa[posicao])
            mov_apagar.append(i)
          
      posicao = self.posicao

    for i in mov_apagar:
      lista_movimentos.remove(i)
      
    movimento = self.heuristica(lista_movimentos, lista_posicoes, lista_coordenada)
    
    
    proxima_posicao = ""
    
    self.mapa[self.posicao] = copia.mapa[self.posicao]
    
    if(movimento == "frente"):
      self.posicao += 1
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
    
    if(movimento == "trás"):
      self.posicao -= 1
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
              
    if(movimento == "cima"):
      self.posicao -= self.N
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
    
    if(movimento == "baixo"):
      self.posicao += self.N
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
              
    if(movimento == "cima-esquerda"):
      self.posicao -= (self.N+1)
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
    
    if(movimento == "cima-direita"):
      self.posicao -= (self.N-1)
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
              
    if(movimento == "baixo-direita"):
      self.posicao += (self.N+1)
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador
    
    if(movimento == "baixo-esquerda"):
      self.posicao += (self.N-1)
      proxima_posicao = self.mapa[self.posicao]
      self.mapa[self.posicao] = self.jogador

    self.ultimo_mov.append(self.posicao)
    if(len(self.ultimo_mov) > 4):
      del self.ultimo_mov[0]
    
    return proxima_posicao    

  def fimDeJogo(self):
    posicaoFinal = (self.M * self.N)-1
    if(self.posicao == posicaoFinal):
      return True
    return False  
  
  def __str__(self):
    m = self.mapa
    linha = self.N
    retorno = ""

    for i in range(self.tamanho):
      if((i+1) % linha == 0):
        retorno += m[i]
        retorno += "\n"

        for j in range(self.N):
          retorno += "-----"

        retorno += "\n"
      else:
        if((i+1) % linha == 1):
          retorno += " "

        retorno += m[i] + " | "

    return retorno 

j = A()
j.inicializar()

copia = A()
copia.inicializar()
copia.mapa = j.retorna_estado()

j.mapa[j.posicao] = j.jogador

while(not j.fimDeJogo()):
  j.caminho.append(j.jogar(j.posicao, copia))
  print(j)

print(j.caminho)