  dir <- '~/Desktop/Rits-genome-engineering/R_script'
  setwd(dir)
  getwd()
  DATE <- Sys.Date()
  
  #make filename
  Season <- 9 #テスト
  row_Days<-(3:18)
  Days<-((3+1):(18))
  #Strain_type <- c("Tak-1", "Cisplatin", "nop1") #S6
  #Strain_type <- c("Tak-1", "Citrine", "CRISPR") #S2
  #Strain_type <- c("Tak-1", "UV", "Cisplatin") #S3
  Strain_type <- c("Tak-1", "nop1", "UV") #S9
   
  #Season <- readline("When is the season? : ") #本番
  fname <- paste("Mapoly_S",Season, sep="")
  csv_fname <- paste(fname,".csv", sep="")
  fname_with_directory <- paste("Assets/Assets_Input/", csv_fname, sep="")
  fname_with_directory #check
  #set file
  #Rawdata_csv<-read.csv(fname_with_directory, header=FALSE, row.names = 1)
  Rawdata_csv<-read.csv(fname_with_directory, header=FALSE, row.names = 1)
  #df #check
  Marchantia_Area_Reversed<- t(Rawdata_csv) #It reverses the rows and the columns
  Marchantia_Area <- data.frame(Marchantia_Area_Reversed)
  print(Marchantia_Area)
  
  print(t(Marchantia_Area)[Days,1])
  
  #plot_functoion
  Save_figure <- function(table_name,filter_name){
    #always
    pic_name <- paste("Assets/Assets_Output/Mapoly_S",Season,"_",filter_name,"_",DATE,".jpeg", sep="")
    fig_title <-paste(fname,"_",filter_name, sep="")
    jpeg(pic_name,width=900,height=675)
    #calculation
    print(table_name)
    for (j in 1:length(table_name[,c("ID")])){
      color_num<-color_num+1
      table_name$X4
      Days_matrix <- list(table_name$X4)
      Days_matrix
      Days_ave <- summary(Days_matrix)
      Days_ave
      plot(t(table_name[j,Days]), xlab="days", ylab="Area [cm2]", cex.main=2.5, main=fig_title, xlim=c(0,18), ylim=c(0,9),  col=color_num)
      par(new=T)
      table_name[j,Days]
    }
    dev.off()
  }
  
  color_num <- 0
  for(i in Strain_type){
    table_name <- paste("Marchantia_Area_", i, sep="")
    table_name <- dplyr::filter(Marchantia_Area, Strain==i)
    Save_figure(table_name, i)
  }
  
  #3つの平均を別のjpegにプロット
  pic_name_for_all <- paste("Assets/Assets_Output/",fname, "_each_Mean",".jpeg",sep="")
  fig_title_for_all <- paste(fname,"_each_mean", sep="")
  jpeg(pic_name_for_all,width=900,height=675)
  color_num <- 1
  for(i in Strain_type){
    color_num<-color_num+1
    Filter_Area<- dplyr::filter(Marchantia_Area, Strain==i)
    ID_num <- length(Filter_Area[,c("ID")])
    #means
    Filter_Area_numeric <- as.data.frame(apply(Filter_Area[(1:ID_num),Days], 2, as.numeric))  # Convert all variable types to numeric
    #sapply(table_Area_numeric, class) 
    #print('aaaaaaa')
    #print(Days)
    #print(Filter_Area_numeric)
    print(colMeans(Filter_Area_numeric, na.rm=TRUE))
    plot(colMeans(Filter_Area_numeric, na.rm=TRUE), xlab="days", ylab="Area [cm2]", cex.main=2.5, main=fig_title_for_all, xlim=c(0,18), ylim=c(0,5), col=color_num, type = "b")
    par(new=T)
  }
  
  #凡例を追加
  #data <- data.frame(Tak1  = c(1, 3, 4, 3, 2), #6
                     #Cisplatin = c(2, 4, 5, 5, 5),
                     #nop1 = c(3, 3, 1, 1, 1))
  #data <- data.frame(Tak1  = c(1, 3, 4, 3, 2), #2
                     #Citrine = c(2, 4, 5, 5, 5),
                     #CRISPR = c(3, 3, 1, 1, 1))
  #data <- data.frame(Tak1  = c(1, 3, 4, 3, 2),
  #data <- data.frame(Tak1  = c(1, 3, 4, 3, 2), #3
                     #UV = c(2, 4, 5, 5, 5),
                     #Cisplatin = c(3, 3, 1, 1, 1))
  data <- data.frame(Tak1  = c(1, 3, 4, 3, 2), #9
                     nop1 = c(2, 4, 5, 5, 5),
                     UV = c(3, 3, 1, 1, 1))
  cols <- c("red", "green", "blue")
  ltys <- c(1, 2, 4)
  pchs <- c(1,16)
  labels <- colnames(data)
  legend("topleft", legend = labels, cex=2.5, col = cols, pch = pchs, lty = ltys)
  dev.off()
  
