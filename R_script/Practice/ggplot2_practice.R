dir <- '~/Desktop/Rits-genome-engineering/R_script'
setwd(dir)
getwd()
DATE <- Sys.Date()

#make filename
#Season <- readline("When is the season? : ") #本番
Season <- 5 #テスト
fname <- paste("Mapoly_S",Season, sep="")
csv_fname <- paste(fname,".csv", sep="")
fname_with_directory <- paste("Assets/Assets_Input/", csv_fname, sep="")
fname_with_directory #check
#set file
Rawdata_csv<-read.csv(fname_with_directory, header=FALSE, row.names = 1)
#df #check
Marchantia_Area_Reversed<- t(Rawdata_csv) #It reverses the rows and the columns
Marchantia_Area <- data.frame(Marchantia_Area_Reversed)
Marchantia_Area
ID_num <- length(Marchantia_Area[,c("ID")])

Days <- c(4:18)

Marchantia_Area_except_Dish<-Marchantia_Area[,-2]
Marchantia_Area_except_Dish_and_Strain<-Marchantia_Area_except_Dish[,-2]
Marchantia_Area_for_ggplot<-data.frame(t(Marchantia_Area_except_Dish_and_Strain))
Marchantia_Area_for_ggplot
a<-ggplot(data=Marchantia_Area_for_ggplot, aes(x=Days,y=)

Marchantia_Area

Marchantia_Area[,Days]
t(Marchantia_Area[,Days])


color_num <- 0
for (i in 1:ID_num){
  paste
   z<- ggplot(t(Marchantia_Area[,Days]))
  #par(new=T)
}
