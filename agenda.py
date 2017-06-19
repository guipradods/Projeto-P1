import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração.

def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição.
  
  novaAtividade = ''
  if descricao  == '' :
    return False
  else:
    if dataValida(extras[0]) == True:
      novaAtividade = novaAtividade + extras[0] + ' '
    if horaValida(extras[1]) == True:
      novaAtividade = novaAtividade + extras[1] + ' '
    if prioridadeValida(extras[2]) == True:
      novaAtividade = novaAtividade + extras[2] + ' '
    novaAtividade += descricao + ' '
    if contextoValido(extras[3]) == True:
      novaAtividade = novaAtividade + extras[3] + ' '
    if projetoValido(extras[4]) == True:
      novaAtividade = novaAtividade + extras[4] + ' '
    novaAtividade = novaAtividade.strip()



  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  listaLetras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  if (len(pri) != 3) or (pri[0] != '(') or (pri[2] != ')'):
    return False
  else:
    for letra in listaLetras:
      if pri[1].upper() == letra:
        return True
    return False
    
      

# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if ((int(horaMin[0] + horaMin[1]) >= 0) and (int(horaMin[0] + horaMin[1]) <= 23)) and ((int(horaMin[0] + horaMin[1]) >= 0) and (int(horaMin[0] + horaMin[1]) <= 59)):
      return True
    else:
      return False
      

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False
  elif (int(data[4] + data[5] + data[6] + data[7]) < 2017) or (int(data[2] + data[3]) < 0) or (int(data[2] + data[3]) > 12):
      return False
  else:
    if (int(data[2] + data[3]) == 1) or (int(data[2] + data[3]) == 3) or (int(data[2] + data[3]) == 5) or (int(data[2] + data[3]) == 7) or (int(data[2] + data[3]) == 8) or (int(data[2] + data[3]) == 10) or (int(data[2] + data[3]) == 12):
      if (int(data[0] + data[1]) < 0) or (int(data[0] + data[1]) > 31):
        return False
      else:
        return True
    elif (int(data[2] + data[3]) == 4) or (int(data[2] + data[3]) == 6) or (int(data[2] + data[3]) == 9) or (int(data[2] + data[3]) == 11):
      if (int(data[0] + data[1]) < 0) or (int(data[0] + data[1]) > 30):
        return False
      else:
        return True
    elif (int(data[2] + data[3]) == 2):
      if (int(data[0] + data[1]) < 0) or (int(data[0] + data[1]) > 29):
        return False
      else:
        return True                                  

                                                                                
                              
# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if (len(proj) < 2) or (proj[0] != '+'):
    return False
  else:
    return True
    
  

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if (len(cont) < 2) or (cont[0] != '@'):
    return False
  else:
    return True
 

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras
    

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    ################ COMPLETAR

    
    for x in tokens:
      if prioridadeValida(x) == False and horaValida(x) == False and dataValida(x) == False and projetoValido(x) == False and contextoValido(x) == False:
        desc = desc + x + ' '
      elif dataValida(x) == True:
        data = x
      elif horaValida(x) == True:
        if desc == "":
          hora = x
        else:
          desc = desc + x + " "
      elif prioridadeValida(x) == True:
        if desc == '':
          pri = x
        else:
          desc = desc + x + " "
      elif contextoValido(x) == True:
        contexto = x
      elif projetoValido(x) == True:
        projeto = x

    if desc != '':
      desc = desc.strip()
      itens.append((desc, (data, hora, pri, contexto, projeto)))


  return itens


def formatarData(data):
  if data == "":
    return ""
  else:
    return data[0] + data[1] + '/' + data[2] + data[3] + '/' + data[4] + data[5] + data[6] + data[7] + " "


def formatarHora(hora):
  if hora == "":
    return ""
  else:
    return hora[0] + hora[1] + 'h' + hora[2] + hora[3] + "m "

def formatarPrioridade(pri):
  if pri == "":
    return ""
  else:
    return pri + " "



 
def listar():
  indice = 0
  arquivo = open(TODO_FILE,'r')
  linhas = arquivo.readlines()
  arquivo.close()
  lista = organizar(linhas)
  lista = ordenarPorDataHora(lista)
  lista = ordenarPorPrioridade(lista)

  while indice < len(lista):
    pri = lista[indice][1][2]
    texto = str(indice) + " " + formatarData(lista[indice][1][0]) + formatarHora(lista[indice][1][1]) + formatarPrioridade(pri) + lista[indice][0] + " " + lista[indice][1][3] + " " + lista[indice][1][4]
    if pri == "(A)":
      printCores(texto, GREEN + BOLD)
    elif pri == "(B)":
      printCores(texto, BLUE)
    elif pri == "(C)":
      printCores(texto, RED)
    elif pri == "(D)":
      printCores(texto, YELLOW)
    else:
      print(texto)
    indice += 1
    


def ordenarPorDataHora(listaDesordenada):
  listaSemDataEHora = []
  listaPraOrdenar = []
  
  for x in listaDesordenada:
    if x[1][0] == '':
      listaSemDataEHora.append(x)
    else:
      listaPraOrdenar.append(x)
 

  maior = listaPraOrdenar[0]
  cont = 1
  x= 0
  while (x < len(listaPraOrdenar)):
      j = cont
      while j < len(listaPraOrdenar):
          if (int(listaPraOrdenar[x][1][0][4] + listaPraOrdenar[x][1][0][5] + listaPraOrdenar[x][1][0][6] + listaPraOrdenar[x][1][0][7] + listaPraOrdenar[x][1][0][2] + listaPraOrdenar[x][1][0][3] + listaPraOrdenar[x][1][0][0] + listaPraOrdenar[x][1][0][1])) > (int(listaPraOrdenar[j][1][0][4] + listaPraOrdenar[j][1][0][5] + listaPraOrdenar[j][1][0][6] + listaPraOrdenar[j][1][0][7] + listaPraOrdenar[j][1][0][2] + listaPraOrdenar[j][1][0][3] + listaPraOrdenar[j][1][0][0] + listaPraOrdenar[j][1][0][1])):
              listaPraOrdenar[x], listaPraOrdenar[j] = listaPraOrdenar[j], listaPraOrdenar[x]
          elif (int(listaPraOrdenar[x][1][0][4] + listaPraOrdenar[x][1][0][5] + listaPraOrdenar[x][1][0][6] + listaPraOrdenar[x][1][0][7] + listaPraOrdenar[x][1][0][2] + listaPraOrdenar[x][1][0][3] + listaPraOrdenar[x][1][0][0] + listaPraOrdenar[x][1][0][1])) == (int(listaPraOrdenar[j][1][0][4] + listaPraOrdenar[j][1][0][5] + listaPraOrdenar[j][1][0][6] + listaPraOrdenar[j][1][0][7] + listaPraOrdenar[j][1][0][2] + listaPraOrdenar[j][1][0][3] + listaPraOrdenar[j][1][0][0] + listaPraOrdenar[j][1][0][1])):
            if (int(listaPraOrdenar[x][1][1][0] + listaPraOrdenar[x][1][1][1] + listaPraOrdenar[x][1][1][2] + listaPraOrdenar[x][1][1][3])) > (int(listaPraOrdenar[j][1][1][0] + listaPraOrdenar[j][1][1][1] + listaPraOrdenar[j][1][1][2] + listaPraOrdenar[j][1][1][3])):
              listaPraOrdenar[x], listaPraOrdenar[j] = listaPraOrdenar[j], listaPraOrdenar[x]
          j += 1
      cont += 1
      x += 1


  listaOrdenada = listaPraOrdenar + listaSemDataEHora
  
  return listaOrdenada


   
def ordenarPorPrioridade(listaDesordenada):
  listaSemPrioridade = []
  listaPraOrdenar = []

  for x in listaDesordenada:
    if x[1][2] == '':
      listaSemPrioridade.append(x)
    else:
      listaPraOrdenar.append(x)
  
  maior = listaPraOrdenar[0]
  cont = 1
  x= 0
  while (x < len(listaPraOrdenar)):
      j = cont
      while j < len(listaPraOrdenar):
          if listaPraOrdenar[x][1][2] > listaPraOrdenar[j][1][2]:
              listaPraOrdenar[x], listaPraOrdenar[j] = listaPraOrdenar[j], listaPraOrdenar[x]
          j += 1
      cont += 1
      x += 1


  listaOrdenada = listaPraOrdenar + listaSemPrioridade

  return listaOrdenada

def fazer(num):
  num = int(num)
  arquivo = open(TODO_FILE,'r')
  linhas = arquivo.readlines()
  arquivo.close()
  lista = organizar(linhas)
  lista = ordenarPorDataHora(lista)
  lista = ordenarPorPrioridade(lista)
  feita = ""

  if num >= len(lista):
    print("Essa posição da lista não existe")
    return False
  else:
    feita = lista.pop(num)
    arquivo = open(TODO_FILE,'w')
    for x in lista:
      saida = ""
      data = x[1][0]
      if data != "":
        saida = saida + ' ' + data
        
      hora = x[1][1]
      pri = x[1][2]
      desc = x[0]
      cont = x[1][3]
      proj = x[1][4]
      arquivo.write(limpaEspaco(data + " " + hora + " " + pri + " " + desc + " " + cont + " " + proj + " ").strip()+ '\n')
    arquivo.close()

  hora = feita[1][1]
  pri = feita[1][2]
  desc = feita[0]
  cont = feita[1][3]
  proj = feita[1][4]


  try: 
    arquivo = open(ARCHIVE_FILE, 'a')
    arquivo.write(limpaEspaco(data + " " + hora + " " + pri + " " + desc + " " + cont + " " + proj + " ").strip()+ '\n')
    arquivo.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + ARCHIVE_FILE)
    print(err)
    return False
    

def limpaEspaco(string):
  indice = 0
  final = ""
  while indice < len(string)-1:
    if (string[indice] == " ") and (string[indice + 1] == " "):
      final += string[indice]
      indice += 2
    else:
      final += string[indice]
      indice += 1

  return final
      


def remover(num):
  num = int(num)
  arquivo = open(TODO_FILE,'r')
  linhas = arquivo.readlines()
  arquivo.close()
  lista = organizar(linhas)
  lista = ordenarPorDataHora(lista)
  lista = ordenarPorPrioridade(lista)

  if num >= len(lista):
    print("Essa posição da lista não existe")
  else:
    del lista[num]
    arquivo = open('todo.txt','w')
    for x in lista:
      data = x[1][0]
        
      hora = x[1][1]
      pri = x[1][2]
      desc = x[0]
      cont = x[1][3]
      proj = x[1][4]
      arquivo.write(limpaEspaco(data + " " + hora + " " + pri + " " + desc + " " + cont + " " + proj + " ").strip()+ '\n')
    arquivo.close()
    


# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  indice = 0
  num = int(num)
  arquivo = open(TODO_FILE,'r')
  linhas = arquivo.readlines()
  arquivo.close()
  lista = organizar(linhas)
  lista = ordenarPorDataHora(lista)
  lista = ordenarPorPrioridade(lista)
  
  if num >= len(lista):
    print("Número inválido")
  else:
    arquivo = open('todo.txt','w')
    
    data = lista[num][1][0]
    hora = lista[num][1][1]
    pri = '(' + prioridade.upper() + ')'
    desc = lista[num][0]
    cont = lista[num][1][3]
    proj = lista[num][1][4]
    arquivo.write(limpaEspaco(data + " " + hora + " " + pri + " " + desc + " " + cont + " " + proj + " ").strip()+ '\n')
    
    del lista[num]
    for x in lista:
      data = x[1][0]
      hora = x[1][1]
      pri = x[1][2]
      desc = x[0]
      cont = x[1][3]
      proj = x[1][4]
      arquivo.write(limpaEspaco(data + " " + hora + " " + pri + " " + desc + " " + cont + " " + proj + " ").strip()+ '\n')
    arquivo.close()
     

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    listar()
    return

  elif comandos[1] == REMOVER:
    remover(comandos[2])
    return    


  elif comandos[1] == FAZER:
    fazer(comandos[2])
    return    


  elif comandos[1] == PRIORIZAR:
    priorizar(comandos[2],comandos[3])
    return    


  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
