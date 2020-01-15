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
Marchantia_Area_dish1 <- dplyr::filter(Marchantia_Area, Dish=='1')
Marchantia_Area_dish1[1,c(4,5,6,7,8,9,10,11,12,13,14,15,16,17)]
#plot practice
f1 <- "../Assets/Assets_Output/Mapoly_Practice_figure1.jpeg"
jpeg(f1,width=900,height=675)
for (i in 1:length(Marchantia_Area[,c("ID")])){
  plot(t(Marchantia_Area_dish1[i,c(4,5,6,7,8,9,10,11,12,13,14,15,16,17)]), xlab="days", ylab="Area [cm2]", main= "Mapoly_S2_Dish1", xlim=c(0,14), ylim=c(0,5))
  par(new=T)
}
dev.off()
