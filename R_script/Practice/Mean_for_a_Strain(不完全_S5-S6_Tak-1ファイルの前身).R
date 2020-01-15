dir <- '~/Desktop/Rits-genome-engineering/R_script'
setwd(dir)
getwd()
DATE <- Sys.Date()

#make filename
#Season <- readline("When is the season? : ") #本番
Season <- 5 #テスト
fname <- paste("Mapoly_S",Season, sep="")
csv_fname <- paste(fname,".csv", sep="")
fname_with_directory <- paste("Assets/Assets_Input",csv_fname, sep="")
fname_with_directory #check
#set file
Rawdata_csv<-read.csv(fname_with_directory, header=FALSE, row.names = 1)
#df #check
Marchantia_Area_Reversed<- t(Rawdata_csv) #It reverses the rows and the columns
Marchantia_Area <- data.frame(Marchantia_Area_Reversed)
Marchantia_Area

#plot_functoion
Save_figure <- function(table_name,filter_name){
  pic_name <- paste("Assets/Assets_Output/",fname,"_", DATE,".jpeg", sep="")
  fig_title <-paste(fname, "_",filter_name,sep="") #変更
  jpeg(pic_name,width=900,height=675)
  for (j in 1:length(table_name[,c("ID")])){
    plot(t(table_name[j,c(3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)]),xlab="days", ylab="Area [cm2]", main= fig_title, xlim=c(0,10), ylim=c(0,7), col = rainbow(j))
    par(new=T)
  }
  dev.off()
}

Strain_type <- c("Tak-1")
for(i in Strain_type){
  table_name <- paste("Marchantia_Area_", i)
  table_name <- dplyr::filter(Marchantia_Area, Strain==i)
  Save_figure(table_name, i)
}

