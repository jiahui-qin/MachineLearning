# 1. 数据读写
library('readr')
data = read_csv(filename, col_names = TRUE)
#做pca
data.pr <- princomp(data,cor=TRUE)
#碎石图
screeplot(data.pr,type="lines")
#lasso回归
library(glmnet)
fit = glmnet(x, y, family="gaussian", nlambda=50, alpha=1)
#x,y分别为自变量，应变量，alpha = 1代表lasso回归中的约束项
#https://cosx.org/2016/10/data-mining-1-lasso