#对时间进行分箱，可以用cut函数，但是等距离分箱可以直接使用除法 %/%

train$context_timestamp <- train$context_timestamp %/% 1e5
train$context_timestamp <- as.factor(train$context_timestamp)

time1<-subset(train, select = c('context_timestamp','is_trade' ))
time1<-as.data.frame(table(time1))
time1<-subset(time1, is_trade == 0)
time0<-fct_count(train$context_timestamp)
colnames(time0)<-c('context_timestamp','n')
timeid <- merge(time0,time1,by.x = 'context_timestamp')
timeid$frequ <- 1-timeid$Freq/timeid$n
timeid<-timeid[,-c(2,3,4)]
boxplot(timeid$frequ)
subset(timeid, timeid$frequ>0.4)

'''
感觉时间上的区别不是很大，可以把前6组作为本地train，最后一组作为本地test
但是划分之前要先给train里没得属性设置为哑变量

以下是当前剩下的变量
 [1] "item_id"[factor]                   "item_brand_id"[factor]              
 [3] "item_city_id"[factor]                "item_price_level"         
 [5] "item_sales_level"          "item_collected_level"     
 [7] "item_pv_level"             "user_id"[factor]                    
 [9] "user_gender_id"            "user_age_level"           
[11] "user_occupation_id"        "user_star_level"          
[13] "context_id"[factor]                  "context_timestamp"        
[15] "context_page_id"[factor]             "shop_id"[factor]                    
[17] "shop_review_num_level"     "shop_review_positive_rate"
[19] "shop_star_level"           "shop_score_service"       
[21] "shop_score_delivery"       "shop_score_description"   
[23] "is_trade"  [factor]  
'''