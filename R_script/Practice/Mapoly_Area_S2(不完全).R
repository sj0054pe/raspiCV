dir <- '~/Desktop/Rits-genome-engineering/R_script'
setwd(dir)
getwd()
df<-read.csv('../assets/Mapoly_S2.csv', header=FALSE, row.names = 1, stringsAsFactors=FALSE)
#df #check
Marchantia_Area_Data1<- t(df) #It reverses the rows and the columns
#Marchantia_Area_Data1 #check
Marchantia_Area_Data2 <- data.frame(Marchantia_Area_Data1, row.names=1, stringsAsFactors=FALSE)
Marchantia_Area_Data2
rownames(Marchantia_Area_Data2)
colnames(Marchantia_Area_Data2)

#Example↓
Marchantia_Area_Data2$Area_Day5
Marchantia_Area_Data2_dish1 <- dplyr::filter(Marchantia_Area_Data2, Dish=='1')
Marchantia_Area_Data2_dish1
Marchantia_Area_Data2_Tak1 <- dplyr::filter(Marchantia_Area_Data2, Strain=='Tak-1')
Marchantia_Area_Data2_Tak1
Marchantia_Area_Data2["1", "Area_Day5"]

Marchantia_Area_Data2$Area_Day4
Days_matrix <- Marchantia_Area_Data2$Area_Day4
Days_matrix
a <- 0
a
as.numeric(A)
for(i in Days_matrix){
  i <- i[(!is.na(i)) & (i > 0)]
  i
  as.numeric(i)
  i
  a <- type.convert(a) + type.convert(i) 
}
a
class(Days_matrix)
is.numeric(Days_matrix)
y <- Days_matrix[(!is.na(Days_matrix)) & (Days_matrix > 0)]
y <- Days_matrix
type.convert(y)
sum(y)
Days_ave <- mean(Days_matrix)
Days_ave
