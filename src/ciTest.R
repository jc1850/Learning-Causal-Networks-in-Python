library(bnlearn)
ciIndep <- function(x,y,S,df)
{
  x <- colnames(df)[x]
  y <- colnames(df)[y]
  indtoname <- function(a)
  {
    return(colnames(df)[a])
  }
  S <- sapply(S, indtoname)
  if(length(S) == 0)
  {
    print(1)
    return(ci.test(x, y, data = df, test='x2'))
  }
  return(ci.test(x, y, S, data = df, test='x2'))
  
}