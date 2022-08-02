#Universidad del Valle de Guatemala 
#Gráficos por computador 
#Gabriela Paola Contreras Guerra 20213
#Libreria Matematica a utilizar 

#Function use to create a matrix, these is used based on a list that conteins all the data that I want on my matrix
#also it allows me to set the size of the matrix 
def createMatrix(row, column, List):
    mat = []
    for i in range(row):
        rowList = []
        for j in range(column):
            rowList.append(List[row * i + j])
        mat.append(rowList)

    return mat

#Function use to muliply 2 matrix using a comprehenshion list 
def multiplyMatrix(A,B):
    result = [[(sum(a * b for a, b in zip(B_row, A_col)))
                            for A_col in zip(*B)]
                                for B_row in A]
    return result

#Funtion use to multiply a matrix and a vector and save the result on a list 
def matmulvec(Matrix, vector):
    if len(Matrix[0]) != len(vector):
        return None
    result = []
    
    for i in range(len(Matrix)):
        suma = 0
        for j in range(len(Matrix[0])):
            suma += Matrix[i][j]*vector[j]
        result.append(suma)

    return result
