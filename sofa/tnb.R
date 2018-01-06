train<-read_csv("F:\\sofa\\tnb\\train.csv")
colnames(train)<-1:40
summary(train)

缺失值填补：
library(mice)

'''
1/6修改:
对性别做了one-hot，然后删掉了缺失值较多的几列，重新读一遍数据
做数值转换后573行性别是NA，删掉：is.na(train)
'''
train<-read_csv("F:\\sofa\\tnb\\train16.csv")
train$'1_for_man'<-as.numeric(train$'1_for_man')
summary(train)

#删掉一行中缺失值大于10个的,删完还有4430个
list <- which(rowSums(is.na(train))>10)
train1 <- train[-list,]

#缺失值填充
train1_mice<-mice(train)
train1_c <- complete(train1_mice)

#lasso回归，用mse作为回归预测标准，预测ROC，10折交叉验证
train_cv_mse = cv.glmnet(x, y,  type.measure = "mse"， nfolds = 10)
plot(train_cv_mse)



##读test数据
test<-read_csv("F:\\sofa\\tnb\\test16.csv")
test$'1_for_man'<-as.numeric(test$'1_for_man')

test1_mice<-mice(test)
test1 <- complete(test1_mice)
test1<-as.matrix(test1)

##这里选择lambda.min预测，效果最好
result <- predict(train_cv_mse, test1, s="lambda.min")

write.csv(result,file = "result.csv")
getwd()