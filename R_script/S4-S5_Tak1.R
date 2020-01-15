dir <- '~/Desktop/Rits-genome-engineering/R_script'
setwd(dir)
getwd()
DATE <- Sys.Date()

#Condition
Strain_type <- c("Tak-1")
Days <- c(4:18) #5
#Days <- c(4:13) #S4

#make filename
#Season <- readline("When is the season? : ") #本番
#Season <- 4 #テスト
Season <- 5 #テスト
fname <- paste("Mapoly_S",Season, sep="")
csv_fname <- paste(fname,".csv", sep="")
fname_with_InputDirectory <- paste("Assets/Assets_Input/", csv_fname, sep="")
fname_with_InputDirectory #check
#set file
Rawdata_csv<-read.csv(fname_with_InputDirectory, header=FALSE, row.names = 1)
Marchantia_Area_Reversed<- t(Rawdata_csv) #It reverses the rows and the columns
Marchantia_Area <- data.frame(Marchantia_Area_Reversed)
Marchantia_Area

#plot practice
Output_Picname <- paste("Assets/Assets_Output/", fname, "_", DATE, ".jpeg", sep="")
jpeg(Output_Picname,width=900,height=675)

ID_num <- length(Marchantia_Area[,c("ID")])
color_num <- 0
for (i in 1:ID_num){
  color_num<-color_num+1
  plot(t(Marchantia_Area[i,Days]), xlab="", ylab="", main="", col=color_num,cex.main=2.5, xlim=c(0,15), ylim=c(0,5))
  par(new=T)
}

for(i in Strain_type){
  fig_title <- paste(fname, "_", i, sep="")
  table_Area<- dplyr::filter(Marchantia_Area, Strain==i)
  #means
  table_Area_numeric <- as.data.frame(apply(table_Area[(1:ID_num),Days], 2, as.numeric))  # Convert all variable types to numeric
  #sapply(table_Area_numeric, class) 
  print(colMeans(table_Area_numeric, na.rm=TRUE))
  plot(colMeans(table_Area_numeric, na.rm=TRUE), xlab="days", ylab="Area [cm2]", cex.main=2.5,main=fig_title, xlim=c(0,15), ylim=c(0,5), col="red", type = "b")
  par(new=T)
}
dev.off()

