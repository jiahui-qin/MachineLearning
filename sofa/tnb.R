train<-read_csv("F:\\sofa\\tnb\\train.csv")
colnames(train)<-1:40
summary(train)

缺失值填补：
library(mice)