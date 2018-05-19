#划分测试集
#先用item_id 举例子
train_list <- fct_count(subset(train,train$context_timestamp != 6)$item_id)$f
ifelse(train[which(train$context_timestamp == 6),]$item_id %in% train_list, train[which(train$context_timestamp == 6),]$item_id ,-1)