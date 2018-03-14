# 观察city，每个城市is_trade卖出的数量，感觉没什么明显区别
city1<-subset(train, select = c('item_city_id','is_trade' ))
city1<-as.data.frame(table(city1))
city1<-subset(city1, is_trade == 0)
city0<-fct_count(train$item_city_id)
colnames(city0)<-c('item_city_id','n')
cityid <- merge(city0,city1,by.x = 'item_city_id')
cityid$frequ <- 1-cityid$Freq/cityid$n
cityid<-cityid[,-c(2,3,4)]
boxplot(cityid$frequ)
subset(brandid, brandid$frequ>0.4)