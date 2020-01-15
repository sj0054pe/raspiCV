dir <- '~/Desktop/Rits-genome-engineering/R_script/'
setwd(dir)
getwd()
DATE <- Sys.Date()

#make filename
#Season <- readline("When is the season? : ")
Season <- '5'
fname <- paste("Mapoly_S",Season, sep="")
csv_fname <- paste(fname,".csv", sep="")
fname_with_directory <- paste("../Assets/Assets_Input/",csv_fname, sep="")
fname_with_directory #check

Days <- c(4:17)

#set file
Rawdata_csv<-read.csv(fname_with_directory, header=FALSE, row.names = 1, stringsAsFactors=F)
matdata_csv=as.matrix(Rawdata_csv)

df #check
Marchantia_Area_Reversed<- t(matdata_csv) #It reverses the rows and the columns
Marchantia_Area <- data.frame(Marchantia_Area_Reversed, stringsAsFactors=F)
Marchantia_Area

pic_name <- paste("Mapoly_variation_",Season, "_",DATE, ".jpeg")
fig_title <- fname
#jpeg(pic_name,width=900,height=675)

Strain_type <- c("Tak-1") #, "Citrine", "CRISPR")
num<-1
plot_points_color<-c("red","blue","green")
plot_points_color[1]
var_list <- list()
Sample_var_list <- list()
i<-1
j <- 1
for(i in Strain_type){
  Strain_name <- paste("Marchantia_Area_", i, sep="")
  print(Strain_name)
  Strain_labels<-c(paste(i, seq(1,15,1), sep=""))
  table_Area <- dplyr::filter(Marchantia_Area, Strain==i)
  table_Area
  this_color <- plot_points_color[num]
  table_Area_numeric <- as.data.frame(apply(table_Area[(1:42),Days], 2, as.numeric))  #Convert all variable types to numeric
  table_Area_numeric
  for(j in Days){
    new_j <- j-3
    rowdata <- c(table_Area_numeric[,new_j])
    #print(rowdata)
    var_list[new_j]=var(rowdata, na.rm=TRUE)
  }
  for(j in Days){
    new_j <- j-3
    rowdata <- c(table_Area_numeric[,new_j])
    #print(rowdata)
    Sample_rowdata <- sample(rowdata,36)
    Sample_var_list[new_j]=var(Sample_rowdata, na.rm=TRUE)
  }
  print(var_list)
  print(Sample_var_list)
  for(k in 1:14){
    print("-------------------------------")
    #is.numeric(var_list[k])
    print(k)
    print(var_list[k])
    print(Sample_var_list[k])
  }
  #plot(colvar(table_Area_numeric, na.rm=TRUE), xlab="days", ylab="Area [cm2]", main=paste(fig_title,'   (Tak-1:Red / Citrine:Blue / CRISPR:Green)'), cex.main='2.2', xlim=c(0,15), ylim=c(0,6), col=this_color, type='b')
  #par(new=T)
  num<-num+1
}
#dev.off()
