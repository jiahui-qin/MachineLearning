[天池精准医疗大赛——人工智能辅助糖尿病遗传风险预测](https://tianchi.aliyun.com/competition/introduction.htm?spm=5176.100068.5678.1.53bde188MOYKlg&raceId=231638)

| 时间       | 成绩           | 方法  | 备注 |
| ------------- |:-------------:| -----:|-----:|
| 1/5     | 0.9004 | mice填补+lasso回归 | |
| 1/6     | 0.9403  |   mice填补+lasso回归 | 删掉了缺失特征较多的样本，性别one-hot |
| 1/7 |     0.9391  |  mice填补(贝叶斯回归)+lasso回归 | 进行predict时选择1se |
| 1/8 | 0.9487 | 随机森林填补 + lasso回归 | predict选择1se,test数据集填补用的还是mice |
| 1/8 | 0.9260 | 随机森林填补 + lasso回归 | predict选择min，其它同上 |

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

'''
1.6晚上修改：删除一部分数据集之后效果反而更差了，这次用全部数据集试试，同时换一下填补缺失值的方法
这次填补缺失值用的是 norm： bayesian liner regression,要求数据全是数值型，其实填补的话我感觉用kmeans是最好的吧，明天再试试。
关于预测中用1se还是min，试试1se的结果吧。
'''
train_mice <- mice(train,m=5,maxit=50,methoh='norm',seed=500)

result<-predict(cvtrain, test_c, s = 'lambda.1se')
