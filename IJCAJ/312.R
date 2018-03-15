library(data.table)
library(readr)

train <- read_table2('E:\\sofa\\ijcai\\train.txt')

#时间序列处理 min：1537200001
train$context_timestamp  = train$context_timestamp - min(train$context_timestamp)

'''
context——page_id 处理 min: 4001
这列数据用box-plot画图，大部分都集中在第一页，可以观察一下第1页往后的概率
第一个nrow结果是1，第二个nrow结果是210626，占到总结果的44.05%
'''
train$context_page_id  = train$context_page_id - 4000
p = train[which((train$context_page_id > 1) && (train$is_trade == 1)),]
nrow(train[which((train$context_page_id > 1)),])
#在第1页之后买东西的那个用户有6条记录，每一条is_trade == 1
train[which(train$user_id == p$user_id),]



#删除重复insance_id数据 这里不能删
#train <- train[!duplicated(train$instance_id),]

'''
item里边 sales, collected, pv怀疑有高度相关
'''

train<-train[,-c(1,3,4)]
train<-train[,-16]
train<-train[,-1] #去掉item-id
 library(randomForest)

train$item_id<-as.factor(train$item_id)
train$item_brand_id<-as.factor(train$item_brand_id)
train$item_city_id<-as.factor(train$item_city_id)
train$user_id<-as.factor(train$user_id)
train$user_gender_id<-as.factor(train$user_gender_id)
train$user_occupation_id<-as.factor(train$user_occupation_id)
train$context_id<-as.factor(train$context_id)
train$shop_id<-as.factor(train$shop_id)
train$is_trade <- as.factor(train$is_trade)

#对因子变量降维,one-hot
library(nnet)
cityid <- class.ind(train$item_city_id)  

#对每一列数据与is_trade做分析,计频数
pp<-subset(train, select = c('item_brand_id','is_trade' ))
pp<-as.data.frame(table(pp))
pp0<-subset(pp, is_trade == 0)
pp1<-fct_count(train$item_brand_id)
colnames(pp1)<-c('item_brand_id','n')
brandid <- merge(pp0,pp1,by.x = 'item_brand_id')
brandid$frequ <- 1-brandid$Freq/brandid$n
brandid<-brandid[,-c(2,3,4)]
boxplot(brandid$frequ)
subset(brandid, brandid$frequ>0.4)
