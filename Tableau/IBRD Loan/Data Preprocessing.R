################################################################
################################################################
###                                                          ###
###                DATA INPUT AND Preprocessing              ###
###                                                          ###
################################################################
################################################################

##=======================================================
##  Libraries & Dataset information
##=======================================================
library(tidyverse)
library(caret)
library(VIM)
library(readxl)

# Loading the comma separated file
A=read.csv("ibrd-statement-of-loans-historical-data.csv")
summary(A)

#----------Dimensions of Dataset----------------------------------

cat("Number of Columns :",dim(A)[1],"\n","Number of Rows :",dim(A)[2])

#--------- Column names of Dataset-------------------------------

colnames(A)

#----------Number of NA (Null) values in dataset -------------------

# Function for finding NA values
col_sumofNA <- function(n){ 
  for (i in 1:ncol(n)) {
    if(sum(is.na(n[i]))>0) # checking NA values using is.na() function
      cat(colnames(n[i])," contains ",sum(is.na(n[i])),"  NA values \n")
    # print the NA Values containing column in dataset
  }
}

col_sumofNA(A)

#visualization of Missing values
aggr(A)
a <- aggr(A)
# summary of missing values
summary(a)$missings[2]

##=============================================================
##  DATA CLEANING
##=============================================================

#----------------- Deleting columns from a dataset-------------

# Column Currency.of.Commitment doesn't contain any data

B <- A[ , -which(names(A) %in% c("Currency.of.Commitment"))]

# Unique columns not containing any useful information

B <- B[ , -which(names(B) %in% c("Loan.Number",
                                 "Country.Code",
                                 "Guarantor.Country.Code",
                                 "Project.ID"))]

# Dimensions of new dataset

cat("Number of Columns :",dim(B)[1],"\n","Number of Rows :",dim(B)[2])

#-------- Unique factor level in Loan Status column ---------

# Number of Factors in loan status column
str(B$Loan.Status)
# Factor levels are not Unique
levels(B$Loan.Status)

# Removing Whitespaces without changing dtypes of a particular column
B <- B %>% mutate_if(is.factor, funs(factor(trimws(.))))

# Unique Factor level in Loan status column 
levels(B$Loan.Status)

#--------------------Near Zero Variance -----------------------

# Removing NA rows for finding Near Zero Variance Columns
C <- na.omit(B)
# Dimensions of new dataset
cat("Number of Columns :",dim(C)[1],"\n","Number of Rows :",dim(C)[2])

# Finding near zero variance columns
nzv_1 <- nearZeroVar(C,freqCut = 15,uniqueCut = 12)
nzv_1

# Removing  near zero variance columns from original dataset
# containing NA values
filter_NZV <- B[,-nzv_1]
#filter_NZV <- C[,-c(9,11,12,14,15,16,17,18,19,20,21,28)]

# Dimensions of new dataset
cat("Number of Columns :",dim(filter_NZV)[1],"\n","Number of Rows :",dim(filter_NZV)[2])

#-----------------Adding Continent Column --------------------
C <- filter_NZV
# loading Country and Continent csv file 
Continent <- read_xlsx("Countries.xlsx")

str(Continent)

# Matching Country with Continent
C$continent=0
for (i in c(1:nrow(C))) {
  for (j in c(1:nrow(Continent))) {
    if(C$Country[i]==Continent$Country[j]){
      cat(i,Continent$Continent[j],"\n")
      C$continent[i]= Continent$Continent[j]
      
    }
  }
  
}

# Filtering Country having Null Continent  
z <- C %>% 
  filter(continent=="0")

# Matching Country key words
for (i in c(1:nrow(z))) {
  for (j in c(1:nrow(Continent))) {
    if(any(grep(Continent$Country[j],z$Country[i]))){
      cat(i,Continent$Continent[j],"\n")
      z$continent[i]= Continent$Continent[j]
      
    }
  }
  
}
# Removing all continent having Null values
zy <- z %>% 
  filter(!continent=="0")

zz <- C %>% 
  filter(!continent=="0")

# Combining the dataset
Final <- rbind(zz,zy)

#----------------------Final csv -------------------

write.csv(Final,"Final Data.csv")


a <- aggr(Final)
# summary of missing values
summary(a)$missings[2]
