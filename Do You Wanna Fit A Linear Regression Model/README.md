# Do You Wanna Fit A Linear Regression Model

![do you want to build a snowman](https://github.com/kimpro82/God-Save-The-Queen/blob/master/images/do%20you%20want%20to%20build%20a%20snowman.png)


## Edcat / Doctor (2019?)
It is a forsaken file that can't be found when and why it has been written, but seems to be related with my wife's R study in 2019.  
But, one thing is for certain, it never would be written for me!

```R
## Read Data

  library(Ecdat)
  data(Doctor)

  str(Doctor)
  head(Doctor)
  head(Doctor[,2:4])


attach(Doctor)

  doctor.dep <- as.matrix(Doctor[,1])
  doctor.var <- as.matrix(Doctor[,2:4])

  solve(crossprod(doctor.var),t(doctor.var)%*%doctor.dep)

  lm(doctor~children+access+health)

detach(Doctor)
```

>                 [,1]  
> children 0.006557745  
> access   3.676781862  
> health   0.667708512

> Call:  
> lm(formula = doctor ~ children + access + health)  
>  
> Coefficients:  
> (Intercept)     children       access       health  
>      1.6075      -0.2512       1.4995       0.6506


## Matrix Operation (2019.03.17 Sun)
practice of matrix operation related with the linear regression analysis


```R
a <- matrix(rep(1:6), ncol=2)
a
```

![matrix a](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-17%20matrix%20a.PNG)

#### - `t()` : get the transpose matrix(전치행렬) of matrix x
```R
b <- t(a)
b
```

![matrix t(a)](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-17%20matrix%20t(a).PNG)


#### - Use of `%*%` operator and `crossprod()`

##### 1) good
```R
b %*% a
crossprod(a)
```

![crossprod(a)](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-17%20crossprod(a).PNG)

##### 2) bad
```R
a %*% b
crossprod(b)
```

![crossprod(b)](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-17%20crossprod(b).PNG)


## Iris (2019.03.15 Fri)

#### ※ Why do I choose the dataset `iris`?

That's just because it is a famous dataset for fool newbies.

I don't mean this data is suitable for a simple linear regression model.

It was just caused by your request of showing matrix operation and `lm()` function use.


### 1. Using `as.matrix()`

This function forces anything to matrix regadless of its will, such like your eyes have made me fall in love.

```R
iris.dep <- as.matrix(iris[,1])  
iris.var <- as.matrix(iris[,2:4])

lm(iris.dep~iris.var)
```
     
![1.as.matrix()](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-15%201.as.matrix().PNG)

### 2. Using `rbind()`/`cbind()`

```R
iris.dep2 <- cbind(iris[,1])
iris.var2 <- cbind(iris[,2:4])

lm(iris.dep2~iris.var2)
```

![2.cbind()](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-15%202.cbind().PNG)

I hate damn `rbind()`/`cbind()`.

### 3. Just input the dataset into `lm()` directly

Actually there's not any pre-processing necessary.

```R
attach(iris)

lm(Sepal.Length~Sepal.Width+Petal.Length+Petal.Width)
```

![3.attach()](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/2019-03-15%203.attach().PNG)

### 4. Bonus

If this story ends here, people will guess I am an idiot who doesn't understand `iris` data.

Please enjoy the real `iris` with the following.

```R
windows(width=7, height=7)
pairs(iris[1:4], pch=21,
      main="But I hate flowers",
      bg=c("red", "blue", "green")[unclass(Species)])
```

![iris_pairs](https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/iris_pairs_20190315.png)

Thank you.
I know you love me.

Yes I am a too much talker.
May I tell you my story when I was in LA?

![Too Much Talker_Park Chanho](
https://github.com/kimpro82/God-Save-The-Queen/blob/master/Do%20You%20Wanna%20Fit%20A%20Linear%20Regression%20Model/image/Too%20Much%20Talker_Park%20Chanho.jpg)
