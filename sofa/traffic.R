#交通事故理赔审核
##http://sofasofa.io/competition.php?id=2#c1

##以下是数据处理
library(readr)
test <- read_csv("E:\\sofa\\traffic\\test.csv")
train <- read_csv("E:\\sofa\\traffic\\train.csv")
test <-as.matrix(test[,-1])
x<-as.matrix(train[,1:36])
y<-as.matrix(train[,37])
y<-as.factor(y)


##logitstic回归
library(glmnet)
cvfit = cv.glmnet(x, y, family = "binomial", type.measure = "class")
plot(cvfit)
##这里选择lambda.min预测，效果最好
result <- predict(cvfit, newx, type="class", s="lambda.min")
write.csv(result,file = "result.csv")
#这里没有看答案要求，要求是概率，我选了classification上去，所以结果很差，再改一遍应该会好很多。

#randomFroest
library(randomForest)
test <-test[,-1]
train <-train[,-1]
sapply(test, as.factor)
sapply(train, as.factor)
traffic.rf <- randomForest(Evaluation ~ ., data=train, type = 'classification')
result <- predict(traffic.rf, test)
write.csv(result,file = "result.csv")
#随机森林的结果很好，和第一名的差异也非常小