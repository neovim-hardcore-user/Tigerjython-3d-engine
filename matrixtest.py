def matrix_multiply(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

print(matrix_multiply([[0.995004165278, 0, 0.0998334166468, 0], 
[0, 1, 0, 0], 
[-0.0998334166468, 0, 0.995004165278, 0], 
[0, 0, 0, 1]]
, [[1, 0, 0, 0], 
[0, 1.0, -0.0, 0], 
[0, 0.0, 1.0, 0], 
[0, 0, 0, 1]]))

