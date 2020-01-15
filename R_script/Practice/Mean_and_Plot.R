  dir <- '~/Desktop/Rits-genome-engineering/R_script'
  setwd(dir)
  getwd()
  DATE <- Sys.Date()

  #make filename
  #Season <- readline("When is the season? : ")
  Season <- '2'
  fname <- paste("Mapoly_S",Season, sep="")
  csv_fname <- paste(fname,".csv", sep="")
  fname_with_directory <- paste("Assets/Assets_Input/",csv_fname, sep="")
  fname_with_directory #check

  #set file
  Rawdata_csv<-read.csv(fname_with_directory, header=FALSE, row.names = 1, stringsAsFactors=F)
  matdata_csv=as.matrix(Rawdata_csv)
  pic_name <- paste("../Assets/Assets_Output/Mapoly_Practice_means_",DATE,"_",Season, ".jpeg")
  fig_title <- fname
  jpeg(pic_name,width=900,height=675)

  df #check
  Marchantia_Area_Reversed<- t(matdata_csv) #It reverses the rows and the columns
  Marchantia_Area <- data.frame(Marchantia_Area_Reversed, stringsAsFactors=F)
  Marchantia_Area

  Strain_type <- c("Tak-1", "Citrine", "CRISPR")
  Days <- c(4:17)
  num<-1
  plot_points_color<-c("red","blue","green")
  plot_points_color[1]
  for(i in Strain_type){
    Strain_name <- paste("Marchantia_Area_", i)
    Strain_labels<-c(paste(i, seq(1,15,1)))
    table_Area<- dplyr::filter(Marchantia_Area, Strain==i)
    #means
    table_Area_numeric <- as.data.frame(apply(table_Area[(1:14),Days], 2, as.numeric))  # Convert all variable types to numeric
    #sapply(table_Area_numeric, class)
    print(colMeans(table_Area_numeric, na.rm=TRUE))
    this_color<-plot_points_color[num]
    plot(colMeans(table_Area_numeric, na.rm=TRUE), xlab="days", ylab="Area [cm2]", main=paste(fig_title,'   (Tak-1:Red / Citrine:Blue / CRISPR:Green)'), cex.main='2.2', tck=0.1, xlim=c(0,15), ylim=c(0,6), col=this_color, type='b')
    #points(colMeans(table_Area_numeric, na.rm=TRUE), xlab="days", ylab="Area [cm2]", main=paste(fig_title,'   (Tak-1:Red / Citrine:Blue / CRISPR:Green)'), xlim=c(0,15), ylim=c(0,6), col=this_color)
    par(new=T)
    num<-num+1
  }
  dev.off()
