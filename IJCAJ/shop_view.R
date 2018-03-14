# 观察shop，每个城市is_trade卖出的数量，感觉没什么明显区别
shop1<-subset(train, select = c('shop_id','is_trade' ))
shop1<-as.data.frame(table(shop1))
shop1<-subset(shop1, is_trade == 0)
shop0<-fct_count(train$shop_id)
colnames(shop0)<-c('shop_id','n')
shopid <- merge(shop0,shop1,by.x = 'shop_id')
shopid$frequ <- 1-shopid$Freq/shopid$n
shopid<-shopid[,-c(2,3,4)]
boxplot(shopid$frequ)
subset(shopid, shopid$frequ>0.4)