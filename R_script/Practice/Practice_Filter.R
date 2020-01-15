dir <- '~/Desktop/Rits-genome-engineering/R_script'
setwd(dir)
getwd()

#make filename
#Season <- readline("When is the season? : ") #本番
Season <- 2 #テスト
fname <- paste("Mapoly_S",Season, sep="")
csv_fname <- paste(fname,".csv", sep="")
fname_with_InputDirectory <- paste("../Assets/Assets_Input/", csv_fname, sep="")
fname_with_InputDirectory #check
#set file
Rawdata_csv<-read.csv(fname_with_InputDirectory, header=FALSE, row.names = 1)
Marchantia_Area_Reversed<- t(Rawdata_csv) #It reverses the rows and the columns
Marchantia_Area <- data.frame(Marchantia_Area_Reversed)
Marchantia_Area

#plot prepare
Save_figure <- function(table_name,filter_name){
  pic_name <- paste("../Assets/Assets_Output/Mapoly_Practice_",filter_name,".jpeg")
  fig_title <-paste("Mapoly_S2_",filter_name)
  jpeg(pic_name,width=900,height=675)
  for (i in 1:length(table_name[,c("ID")])){
    plot(t(table_name[i,c(4,5,6,7,8,9,10,11,12,13,14,15,16,17)]), xlab="days", ylab="Area [cm2]", main= fig_title, xlim=c(0,14), ylim=c(0,7))
    par(new=T)
  }
  dev.off()
}

Marchantia_Area_dish1 <- dplyr::filter(Marchantia_Area, Dish=='1')
Save_figure(Marchantia_Area_dish1, "Dish_1")

Marchantia_Area_Tak1 <- dplyr::filter(Marchantia_Area_Data2, Strain=='Tak-1')
Save_figure(Marchantia_Area_Tak1, "Tak-1")
