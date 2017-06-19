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



def printCores(texto, cor) :
  print(cor + texto + RESET)
  



def adicionar(descricao, extras):
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



  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


def prioridadeValida(pri):
  listaLetras = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  if (len(pri) != 3) or (pri[0] != '(') or (pri[2] != ')'):
    return False
  else:
    for letra in listaLetras:
      if pri[1].upper() == letra:
        return True
    return False
    
      

def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if ((int(horaMin[0] + horaMin[1]) >= 0) and (int(horaMin[0] + horaMin[1]) <= 23)) and ((int(horaMin[0] + horaMin[1]) >= 0) and (int(horaMin[0] + horaMin[1]) <= 59)):
      return True
    else:
      return False
      

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

                                                                                
                               
def projetoValido(proj):
  if (len(proj) < 2) or (proj[0] != '+'):
    return False
  else:
    return True
    
  

def contextoValido(cont):
  if (len(cont) < 2) or (cont[0] != '@'):
    return False
  else:
    return True
 

def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() 
    tokens = l.split() 
    

   
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
    
  

processarComandos(sys.argv)
