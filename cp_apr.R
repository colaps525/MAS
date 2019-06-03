data <- read.table("/Users/kojimajun/MultiAspectSpotting/result_edit_anno_id.csv", header=F, sep=",")

subs = data[,1:3]
vals = data[,4]

max_col1 = max(data[,1])
max_col2 = max(data[,2])
max_col3 = max(data[,3])

X=list(subs=subs,vals=vals,size=c(max_col1,max_col2,max_col3))

set.seed(12345)#for reproducability
library(RDFTensor)
P1=cp_apr(X,10,opts=list(alg='mu'))

write.table(P1$M$u[1], "/Users/kojimajun/MultiAspectSpotting/PTF_mode1.csv",row.names = FALSE,col.names = FALSE,sep =",")
write.table(P1$M$u[2], "/Users/kojimajun/MultiAspectSpotting/PTF_mode2.csv",row.names = FALSE,col.names = FALSE,sep =",")
write.table(P1$M$u[3], "/Users/kojimajun/MultiAspectSpotting/PTF_mode3.csv",row.names = FALSE,col.names = FALSE,sep =",")

write.table(matrix(P1$M$lambda), "/Users/kojimajun/MultiAspectSpotting/PTF_lambda.csv",row.names = FALSE,col.names = FALSE,sep =",")

