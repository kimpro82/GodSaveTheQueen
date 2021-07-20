## For my wife who is a R newbie. And this is Sparta! - 2019.03.15 Fri


## Loading any famous dataset for fool newbies
data("iris")

## I don't mean this data is suitable for a simple linear regression model.
## It was just caused by your request of showing matrix operation and lm() function use.


## Several methods for skimming the dataset. You nahm sayin?
str(iris)
head(iris)
summary(iris)


## Do you want to adopt damn linear regression model by damn data?
## So, do you need to get seperated each matrices that consist of a Y variable and X variables?
## I don't agree it is necessary, but there's still no problem.


## 1. Using as.matrix()

## This function forces anything to matrix regadless of its will, such like your eyes have made me fall in love.

iris.dep <- as.matrix(iris[,1])     ## 'dep' means dependant variable(Y).
iris.var <- as.matrix(iris[,2:4])   ## Then you know what 'var' is(, or die).

## Additionally, do you understand what [,1] [,2:4] mean?
## You'd better search about [indexing & slicing].
## Don't be absorbed in slicing only sushi, but try also slicing your data.
## Please.

## Check the matrices before run lm()
head(iris.dep)
head(iris.var)
## Good

lm(iris.dep~iris.var)
## Good


## 2. Using rbind()/cbind()

## Hey matrix operation newbie, listen.

iris.dep2 <- cbind(iris[,1])
iris.var2 <- cbind(iris[,2:4])

## Check the matrices before run lm()
head(iris.dep2)
head(iris.var2)
## Good

lm(iris.dep2~iris.var2)
## Bad. What the hell
## I hate damn rbind()/cbind().


## 3. Actually there's not any pre-processing necessary.
## Just input the dataset into lm() directly.

## For input the variable's name directly, use attach().
attach(iris)
## This will make the crazy errors that you've been suffering just right now.

lm(Sepal.Length~Sepal.Width+Petal.Length+Petal.Width)
## Good


## 4. Bonus

## If this story ends here, people will guess I am an idiot who doesn't understand iris data.
## Please enjoy the real iris with the following.
windows(width=7, height=7)
pairs(iris[1:4], pch=21,
      main="But I hate flowers",
      bg=c("red", "blue", "green")[unclass(Species)])
## I am not an idiot. You idiot.

detach(iris)
## attach() loads the data on your poor memory, so we need to kill the dog after hunting is over.
## By detach(), prove your Machiavellian blood!


## Thank you.
## I know you love me.


## Yes I am a too much talker.
## May I tell you my story when I was in LA?