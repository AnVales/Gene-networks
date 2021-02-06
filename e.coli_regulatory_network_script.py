from timeit import default_timer
import numpy as np
import timeit


# Abrimos el archivo
file2 = open("path/network_tf_gene.txt", "r")
# file2 = open("path", "r")

# Número de factores de transcripción y genes diferentes
TF={}

for line in file2.readlines():
    words = line.split()
    if words[0] == "#":
        continue
    for r in [0,1]:
        if words[r].lower() not in TF: # Si no está este TF o gen en el diccionario lo metemos
            TF[words[r].lower()]=words[r].lower()    

print('numero de genes diferentes:',len(TF))


# Empezar a leer desde el inicio
file2.seek(0)


# El número de relaciones que tienen factores de transcripción con genes
TFPAR={}

for line in file2.readlines():
    words = line.split()
    if words[0] == "#":
        continue
    if ((words[0].lower(), words[1].lower())) not in TFPAR:  # Si no tenemos esta relación del TF con el gen en el diccionario lo metemos
        TFPAR[(words[0].lower(), words[1].lower())] = (words[0].lower(), words[1].lower())
    
print('numero de relaciones que tienen los factores de transcripcion con genes, es decir, los 1s:',len(TFPAR))


# Hacemos la matriz llena de 0s
matriz0 = np.zeros((len(TF), len(TF)))

# Ponemos los 1s SIN MEZCLAR
contador = 0
for r in range(len(matriz0)):
    for c in range(len(matriz0[r])):
        matriz0[r][c] = 1
        contador+=1
        if contador == len(TFPAR):
            break
    if contador == len(TFPAR):
        break


# REMOVEMOS los 1s en la matriz y además lo transformamos a un diccionario con las relacciones 
def matrizADic(matriz):
    dic = {}

    matriz = matriz.ravel() # Se pasa la matriz a 1D
    np.random.shuffle(matriz) # Se distribuye de forma aleatoria los números
    matrizfinal = matriz.reshape(len(TF), len(TF)) # Se le vuelve a dar su forma de matriz

    for r in range(len(matrizfinal)):
        for c in range(len(matrizfinal[r])):
            if matrizfinal[r][c] == 1: # Si en un valor encuentra un 1
                tuplaAux = (r, c) # Guardamos la fila y la columna de donde está 
                if r not in dic: # Si no tenemos el diccionario de ese TF se crea
                    dic[r] = {}
                dic[r][tuplaAux] = tuplaAux # Metemos en el diccionario del TF como clave la relación y como valor la relación
                if c not in dic: # Se crea un diccionario del gen porque sino luego peta, si lo creamos vacío no pasa
                    dic[c] = {}
                
    return dic


# Empezar a leer desde el inicio
file2.seek(0)


# Creamos el diccionario de las dos columnas
def crearDic(file):
    dic = {}
    for line in file.readlines():
        words = line.split()
        if words[0] == "#": # Las lineas que empiecen por # las pasamos
            continue
        tuplaAux = (words[0].lower(), words[1].lower()) # Hacemos una tupla con el TF y los genes
        if words[0].lower() not in dic: # Si no hay diccionario del TF se crea
            dic[words[0].lower()] = {}
        dic[words[0].lower()][tuplaAux] = tuplaAux # Se mete la relación el diccionario del TF 
        if words[1].lower() not in dic:
            dic[words[1].lower()] = {} # Se hace un diccionario del gen
    return dic

# Longitud del diccionario de la matriz y el de la tabla
def lenDic(dic):
    total = 0
    for e in dic.values():
        total +=len(e)
    return total


# Se transforma la matriz sin mezclar a diccionario, confirmamos su longitud para ver que tenemos el mismo número de relaciones 
# Que de 1s que se han metido
dictmatriz = matrizADic(matriz0)
longitudDictMatriz = lenDic(dictmatriz)
print('numero de relaciones que tiene el diccionario de la matriz:',longitudDictMatriz)

# Hacemos un diccionario con el archivo
dictFile = crearDic(file2)
longitudDictFile = lenDic(dictFile)
print('numero de relaciones que tiene el diccionario del archivo:', longitudDictFile)

# CONTAR AUTORREGULACIONES 

def contarAutoregulaciones(dic):
    contador = 0
    for key in dic:
        for a,b in dic[key].keys():
            if a == b:
                contador+=1

    return contador

autoregulationRnd = contarAutoregulaciones(dictmatriz)
autoregulation = contarAutoregulaciones(dictFile)
print('las autoregulaciones del archivo son ', autoregulation,' mientras que las de la matriz aleatoria son: ', autoregulationRnd)


# Sería mejor no probar solo con una matriz aleatoria

n = 10
autoregulationRnd10=[]

print('es mejor probar con más matrices aleatorias, en este caso tan solo se va a probar con', n, 'por los tiempos de carga')

def contarAutoregulaciones10(matriz):
    for i in range(n):
        matrizDic1 = matrizADic(matriz)
        autoregulationRndi = contarAutoregulaciones(matrizDic1)
        autoregulationRnd10.append(autoregulationRndi)

contarAutoregulaciones10(matriz0)
print('las autoregulaciones de las diferentes' ,n, 'matrices aleatorias son',autoregulationRnd10)

# CONTAR feed-forward loop

def contarFFL(dic):
    contador = 0
    for key in dic:
        for a, b in dic[key].keys():
            if a == b:
                continue
            for c, d in dic[b].keys():
                if b != c or c==d or (c == a):
                    continue
                if (a, d) in dic[a]:
                    contador+=1


    return contador
    
FFLRnd = contarFFL(dictmatriz)
FFL = contarFFL(dictFile)
print('los FFL del archivo son ', FFL,' mientras que las de la matriz aleatoria son: ', FFLRnd)


# Sería mejor no probar solo con una matriz aleatoria

n = 10
FFLRnd10=[]

print('es mejor probar con más matrices aleatorias, en este caso tan solo se va a probar con', n, 'por los tiempos de carga')

def contarFFLRnd10(matriz):
    for i in range(n):
        matrizDic1 = matrizADic(matriz)
        FFLRnd10i = contarFFL(matrizDic1)
        FFLRnd10.append(FFLRnd10i)

contarFFLRnd10(matriz0)
print('los FFL de las diferentes' ,n, 'matrices aleatorias son',FFLRnd10)

# MAXIMO CASCADE

def convertir(grafo):
    grafoConvertido = {}
    for key in grafo.keys(): # las keys A
        adj = []
        for value in grafo[key]: # valores de la key A:A-B,A-C,A-D
            adj.append(value[1]) # guarda B,C,D
        grafoConvertido[key] = adj # key: A, value: adj: B,C,D
    return grafoConvertido


def initVisited(grafo):
    visited = {} # hash de visitados
    for key in grafo.keys(): # key: A
        visited[key] = False # key: A, value: False
    return visited # hash de keys False

def dfs(grafo, nodoFuente, prev_len, maxLen, visited):
    visited[nodoFuente] = True # la key pasa a ser visitada
    currLen = 0 # la longitud ahora mismo es 0

    for adj in grafo[nodoFuente]:
        if not visited[adj]:
            currLen = prev_len + 1
            dfs(grafo, adj, currLen, maxLen, visited)
        
        if maxLen[0] < currLen:
            maxLen[0] = currLen
        currLen = 0



def longitudMax(grafo):
    maxLen = [-9999999]
    for elem in grafo.keys(): # keys: A
        visited = initVisited(grafo) # nos da hash de Falsos
        dfs(grafo, elem, 0, maxLen, visited) # damos el grafo con info, la key que miramos, 0, la longitud maxima y los que estan visitados o no
    return maxLen


dictmatriz_conv = convertir(dictmatriz)
dictFile_conv = convertir(dictFile)

cascadeRnd = longitudMax(dictmatriz_conv)
cascade = longitudMax(dictFile_conv)
print('la longitud de cascada máximo del archivo es ', cascade[0]+1,' mientras que las de la matriz aleatoria es: ', cascadeRnd[0]+1)

n = 10
CascadeRnd10=[]

print('es mejor probar con más matrices aleatorias, en este caso tan solo se va a probar con', n, 'por los tiempos de carga')

def contarCascadeRnd10(matriz):
    for i in range(n):
        matrizDic1 = matrizADic(matriz)
        matrizDic1_conv = convertir(matrizDic1)
        CascadeRnd10i = longitudMax(matrizDic1_conv)
        CascadeRnd10.append(CascadeRnd10i[0]+1)

contarCascadeRnd10(matriz0)
print('las cascadas de las diferentes' ,n, 'matrices aleatorias son',CascadeRnd10)

