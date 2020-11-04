#----------LOading the file-------------------
A=read.csv(file.choose())
#View(A)

summary(A)

#----------Number of Coulmns and Rows-------------------

cat("Number of Columns :",ncol(A))
cat("Number of Rows :",nrow(A))
dim(A)
#------Checking Column names-------------------------------

colnames(A)

#----------Checking Number of NA values-------------------

col_sumofNA <- function(){ 
  for (i in 1:ncol(A)) {
    if(sum(is.na(A[i]))>0) # checking NA values using is.na() function
      cat(colnames(A[i])," contains ",sum(is.na(A[i])),"  NA values \n")
    # print the NA Values containing column in dataset
  }
}

col_sumofNA()
# col_sumofNA function will tell us which column contains NA values


#-----------Checking Outliers----------------------------------
# Only for Numerical Data
outliers1 <- boxplot(A$Interest.Rate,plot = FALSE)$out

#--------genrating a box plot of categorical data & Numerical----------


# windows(30,15)

barplot(table(A$Loan.Status))

#----------------Feature Selection ------------------------
# Feature Selection
set.seed(111)
boruta <- Boruta(Loan.Status ~ ., data = B, doTrace = 2, maxRuns = 500)
print(boruta)
plot(boruta, las = 2, cex.axis = 0.6)
plotImpHistory(boruta)

# Tentative Fix
bor <- TentativeRoughFix(boruta)
print(bor)
attStats(boruta)

#-------------------column name cleaning--------------------

library(janitor)

#can be done by simply
ctm2 <- clean_names(A)

#or piping through `dplyr`
ctm2 <- A %>%
  clean_names()

#------------------------------------------------------------