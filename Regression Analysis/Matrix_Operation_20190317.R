# practice of matrix operation related with the linear regression analysis

a <- matrix(rep(1:6), ncol=2)
a

# t() : get the transpose matrix(전치행렬) of matrix x
b <- t(a)
b


# Use of %*% operator and crossprod()

# 1) good
b %*% a
crossprod(a)

# 2) bad
a %*% b
crossprod(b)