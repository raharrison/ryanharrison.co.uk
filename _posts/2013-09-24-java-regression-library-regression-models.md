---
title: 'Java Regression Library – Regression Models'
layout: post
tags:
  - java
  - library
  - regression
---
## Part 1 – Regression Models

In this tutorial series we'll be going over how to create a simple Regression Analysis library in Java. If you have any prior knowledge of regression analysis you will probably know that this is a very large field with a great many applications. In this tutorial series we won't be covering any massively advanced techniques. Our final library will be able to produce the same results as you would find in Microsoft Excel (excluding the graph plotting), which in most basic circumstances will be plenty enough to get you some good results.

### Prerequisites –

It's best if you start this series with a sound knowledge of OOP (object-oriented programming) practices in Java as this series will include the use of abstract classes and polymorphism. You will also need a good knowledge of some of the more basic concepts in Java such as looping, methods and variables. I will do my best to explain the code as much as I can but it is advisable that you have some prior knowledge.

As this tutorial series will of course focus on mathematical concepts as regression analysis is a mathematical technique you will need a sound knowledge of algebra and graphs. I will again do my best to explain all of the concepts as much as possible to cater for beginners, people who have a basic algebra or statistics course under their belts will find things a lot easier.

### What is Regression Analysis?

So enough of all the introductions lets get straight in! If you haven't heard of regression analysis before you are probably already asking what is it and why is it useful? From the [Wikipedia article on regression analysis][1]:

  >"a statistical process for estimating the relationships among variables. It includes many techniques for modelling and analysing several variables, when the focus is on the relationship between a dependent variable and one or more independent variables. More specifically, regression analysis helps one understand how the typical value of the dependent variable changes when any one of the independent variables is varied, while the other independent variables are held fixed."

Well that hasn't really helped much now has it? It is much simpler to understand if you think about the variables as the `X` and `Y` coordinates on a graph. 

Consider the case where you have a simple scatter plot diagram. You have a set of `X` and `Y` coordinates that are plotted on a graph with two axis' – the `x` and `y`. For example this graph where the data runs up until an `X` value of 11. Say these values are from a particular stock on the stock exchange (regression analysis has a lot of applications in stocks and shares). The `X` values represent each a month in the year and the respective `Y` coordinates are the average price of the stock in that particular month. From the graph plot we can see that the price of shares is steadily increasing but we don't possess any data for the 12th month. Is the price going to increase or decrease in December? How can we find out? For market traders this is very important information that can make them or lose them millions. The answer – regression analysis!

![Scatter Plot][2]{: .center-image}

So we have data up to November and we want to find out what the `Y` value is when `X` is 12. The trouble is its not December yet so we don't know what it is. We need a forecast model. Lets revisit the situation. We have an `X` value and we need the `Y` value. Hopefully this is ringing some bells. It sounds an awful lot like a good use of an function such as `Y = aX + b` (or it could be any other function). We can insert an `X` value of 12 and we get back the corresponding `Y` value which is the average stock price for December. Sounds great but we have a problem. We don't know the variables `a` and `b`! The function could have any intercept and gradient. We currently don't have a clue. We could make one up but someone like a market trader doesn't want to risk their money on a made up value. We need a way to find the values of a and b which when put into the function will give us back an accurate value for the price in December.

Armed with that knowledge lets go back to the Wikipedia definition. 'estimating the relationships among variables' – this kind of makes more sense now. As `X` increases what does `Y` do? This is called the relationship between the two variables. If the `Y` values are increasing a lot as `X` increases, our forecast should reflect this relationship. We now need to label `X` and `Y` in more formal terms.

`Y` is the dependent variable. It depends on the values of the other independent variables and parameters a, `X` and b to give it a value.

We can now again go back to the Wikipedia definition. 'helps one understand how the typical value of the dependent variable changes when any one of the independent variables is varied, while the other independent variables or parameters are held fixed.' Again this makes more sense now. We want to analyse how the dependent variable `Y` changes as the independent `X` value is varied and the other parameters `a` and `b` are kept fixed. This is most often done through an function such as `Y = aX + b`.

So essentially we want to find some function that best fits the data points that we have for the other months. The function models the relationship between `X` and `Y`. Once we have this function we can plug in `X` values and get the `Y` values that follow the relationship. This has many uses!

Lets go back to our example. We want to find the forecast of the stock price in December. We therefore need to find some function that relates the month to the price. This is regression analysis in its simplest form. Things get harder when we have to figure out what function is best to use to model the relationship (is it a linear line, an exponential line etc) and how can we find out how good our model is at describing the relationship, but we will move onto that in later parts of this series.

The most basic form of regression analysis is linear regression – that is finding a linear function that best models the relationship between the two variables. The base linear line function is `Y = aX + b` from earlier. We want to find the price `Y` and `X` is the month. We need to find the best values for `a` and `b` that produce a line that follows our current data as much as possible. If the line is accurate, we can use it to forecast other months. Our function becomes `PRICE = a * MONTH + b`. A huge part of regression analysis is finding the best values of `a` and `b` that produce a line that closely models our current data set.

### What?

That's a lot of words but it will all make sense by the end of this tutorial series.

  * Regression analysis aims to model and analyse the relationship between variables (in this series we will be using one variable only `X`)
  * This involves creating functions that model the relationship. For example linear functions or exponential functions.
  * Once we have an accurate model of the sample data we can use it to forecast `Y` values for `X` values that were not in our original data set.

Lets put that into pictures. Take the simple scatter diagram we had before. We want to fit a line onto those data points that closely models the relationship between the variables – we can see this visually if the line that is created passes through or close to all the data points.

![Bad Model][3]{: .center-image}

This is not a good model of the data. It does not pass through the data points at all. If we were to use this function to model the stock price we would lose a lot of money. Lets see if we can do a little better

![Good Model][4]{: .center-image}

Much better. As you can see the new line passes through or very close to all of our data points. it should however be pointed out that this is not a *perfect* model, however a perfect fit is extremely unlikely unless there is complete correlation between `X` and `Y`. As it turns out this line is:

`Y = 4.1939X + 9.4763`

Seems pretty arbitrary but in fact this line is the best linear line that models our current data points. Thus if we used this function to forecast the month of December (by inserting 12 as `X`), we would have a better chance of making some money.

You may or may not be thinking that this looks a bit familiar. Isn't that just a line of best fit? I can do that in Excel by using TrendLines. The answer: yes! When you tell Excel to make a trendline or line of best fit of your data points, internally Excel is performing a Regression Analysis on those data points to find an function of a line that best describes the relationship between your data points. It doesn't call this regression analysis, yet it is in fact doing this exact thing. Pretty cool eh? In this tutorial series we will be using Java to perform this exact same thing on our data. We will even get the same results as Excel! If you look into the TrendLine options in Excel you will see that you have the option to match not only a linear line `Y = aX + b`, but also a whole load of others like logarithmic, exponential etc. If we select logarithmic Excel we perform another regression analysis on our data but this time to match a logarithmic function and not a linear one. This takes the form `Y = a * ln(X) + b`. As it turns out the best logarithmic function (in that form) we can fit to that data set is `Y = 21.688 * ln(x) – 1.0532`. This line doesn't match our data set that well at all yet it is best that the logarithmic regression model can do with two fixed parameter variables.

![Regression Types][5]{: .center-image}

I mentioned Regression Models before. More formally they are defined as:

![Regression Model][6]{: .center-image}

That is a `Y` dependent variable related to by a function of your varied independent variable X and and N other unknown fixed parameters `ß`.

In a linear regression model this function is normally `Y = ß1X + ß2`

In a logarithmic regression model this function is normally `Y = ß1 * ln(X) + ß2`

There are a load of different regression models that you can do, however the model that you choose should be relevant to the data set your are performing it on. For example logarithmic and exponential models are commonly used to analyse the stock market, however these models may not be relevant at all for other sets of data. They may model your current data nicely, however they may not provide good sources of forecasts. That is another area of Regression Analysis – which model should I use for my data and how good is it at modelling it?

It is also important to consider how many data points you have in your sample data set upon which your Regression Model will base its results from. The Wikipedia article explains this quite well.

  > Assume now that the vector of unknown parameters ß is of length k. In order to perform a regression analysis the user must provide information about the dependent variable Y:
  > If N data points of the form (Y,X) are observed, where N < k, most classical approaches to regression analysis cannot be performed: since the system of functions defining the regression model is underdetermined, there are not enough data to recover ß. If exactly N = k data points are observed, and the function f is linear, the functions Y = f(X, ß) can be solved exactly rather than approximately. This reduces to solving a set of N functions with N unknowns (the elements of ß), which has a unique solution as long as the X are linearly independent. If f is nonlinear, a solution may not exist, or many solutions may exist. The most common situation is where N > k data points are observed. In this case, there is enough information in the data to estimate a unique value for ß that best fits the data in some sense, and the regression model when applied to the data can be viewed as an overdetermined system in ß.

So basically if you have more unknown parameters than data points most models will not work and if there are more data points then you are able to estimate values for each parameter in `ß` to best fit your data.

In this tutorial series we will only be using one independent variable `X` as this matches up nicely to coordinates on a 2D graph for our models. Regression analysis can be done however with many independent variables however but these area harder to explain in a graphical manner. Most real world applications of regression analysis have multiple independent variables.

That is all the math over and done with for this tutorial! Phew! It may be a lot to take in for beginners but in each tutorial the basic fundamentals of regression analysis will be build upon. 

In each part of this tutorial series we will be covering a new Regression Model and adding an implementation to our Java Regression library. In the end we will be able to use our library to perform the same analysis as Microsoft Excel can perform on a data set.

### Let's start coding!

As I said in each part of this series we will be introducing a new regression model and adding a Java implementation. As we are good developers and want to minimize code duplication as much as possible, it makes sense to create a superclass to all of our model implementations. This is what we will do in this tutorial. There is more theory in this introduction tutorial than code, but there will be more in later tutorials.

So lets make a class called `RegressionModel` that will become a superclass to all of our models. It makes sense to make this abstract as you should only be instantiating concrete implementations of a particular model.

{% highlight java %}
public abstract class RegressionModel {
}{% endhighlight %}

Looks good. Now lets consider what field we need that are common to all models. As we are only using one independent variable `X`, we only need two fields that represent our data set. These are two arrays representing our data points of `X` and `Y` coordinates. There is then a computed flag that is set to true when the parameters are computed. The flag is used in the `getCoefficients()` and `evaluateAt(x)` methods to throw an exception is the computation has not yet happened.

{% highlight java %}
// The X values of the data set points 
protected double[] xValues;

// The X values of the data set points \*/  
protected double[] yValues;

// Have the unknown parameters been calculated yet?  
protected boolean computed;
{% endhighlight %}

We can only instantiate a model when we have supplied the data it should perform it on. So we need a constructor that allows us to pass in our data points. We also provide getters to allow users to retreve the data points:

{% highlight java %}  
/**  
* Construct a new RegressionModel object with the specified data points  
*  
* @param x  
* The X data points  
* @param y  
* The Y data points  
*/  
public RegressionModel(double[] x, double[] y) {  
    this.xValues = x;  
    this.yValues = y;  
    computed = false;  
}

/**  
* Get the X data points  
*  
* @return The X data points  
*/  
public double[] getXValues() {  
    return this.xValues;  
}

/**  
* Get the Y data points  
*  
* @return The Y data points  
*/  
public double[] getYValues() {  
    return this.yValues;  
}  
{% endhighlight %}

We could also add setters but my personal style is to make everything immutable. If you want to perform an analysis on another data set, another instance of the model would be needed.

We now define the abstract methods that all concrete implementations must provide.

{% highlight java %} 
/**  
* Get the computed coefficients from the model that best fit the data set  
*  
* @return The computed coefficients or parameters that have been fitted to the data set  
*/  
public abstract double[] getCoefficients();
{% endhighlight %}

This will return the computed values of the unknown parameters for the model. For example in a linear regression a and b would be returned

{% highlight java %} 
/**  
* Find the best fit values of the unknown parameters in this regression model  
*/  
public abstract void compute();
{% endhighlight %}

This method initiates the actual computation to retrieve values for the currently unknown parameters for the model. We could do this in the constructor, however for large data sets it may take time. It is therefore better to leave at the users discretion to when the computation will happen (perhaps in another thread). If `getCoefficients()` is called without calling `compute()` first, an exception should be thrown.

{% highlight java %} 
/**  
* Evaluate the computed model at a point x  
*  
* @param x  
* The point to evaluate the model at  
* @return The underlying models computed function evaluated at x  
*/  
public abstract double evaluateAt(double x);
{% endhighlight %}

This method will be used to evaluate the model's result function at a certain point `x`. For example if the computation resulted in parameter values of 5 and 7, Y, which would become `5*x + 7` is returned. This is an interface to use the result function in forecasts. If `evaluateAt(x)` is called without calling `compute()` first, an exception should be thrown.

Here is the full code for the `RegressionModel` class. It is not that big at the moment but we will expand on it in future tutorials:

{% highlight java %}  
/**  
* Represents a regression model with one defined independent variable. Provides operations to compute the regression coefficients  
* and evaluate the resulting function at a certain point.  
*  
* We will expand this class in later parts  
*/  
public abstract class RegressionModel {

// The X values of the data set points 
protected double[] xValues;

// he X values of the data set points  
protected double[] yValues;

// Have the unknown parameters been calculated yet? 
protected boolean computed;

/**  
* Construct a new RegressionModel object with the specified data points  
*  
* @param x  
* The X data points  
* @param y  
* The Y data points  
*/  
public RegressionModel(double[] x, double[] y) {  
    this.xValues = x;  
    this.yValues = y;  
    computed = false;  
}

/**  
* Get the X data points  
*  
* @return The X data points  
*/  
public double[] getXValues() {  
    return this.xValues;  
}

/**  
* Get the Y data points  
*  
* @return The Y data points  
*/  
public double[] getYValues() {  
    return this.yValues;  
}

/**  
* Get the computed coefficients from the model that best fit the data set  
*  
* @return The computed coefficients or parameters that have been fitted to the data set  
*/  
public abstract double[] getCoefficients();

/**  
* Find the best fit values of the unknown parameters in this regression model  
*/  
public abstract void compute();

/**  
* Evaluate the computed model at a point x  
*  
* @param x  
* The point to evaluate the model at  
* @return The underlying models computed function evaluated at x  
*/  
public abstract double evaluateAt(double x);  
}  
{% endhighlight %}

That sums up the first tutorial in this series. As I said before there was a lot of theory and not much coding in this one, but there will be more in future tutorials (although there will still be quite a lot of theory).

Check out [Part 2][7] of this tutorial where we get on to implementing a `LinearRegresssionModel`!

 [1]: http://en.wikipedia.org/wiki/Regression_analysis
 [2]: http://i.imgur.com/32ToM9O.jpg
 [3]: http://i.imgur.com/zuGTqzG.jpg
 [4]: http://i.imgur.com/w9Wa8WE.jpg
 [5]: http://i.imgur.com/yssVg8S.jpg
 [6]: http://upload.wikimedia.org/math/8/f/b/8fb0426fb13f5e83ac05e208be4f9dfa.png
 [7]: {{ site.baseurl }}{% post_url 2013-10-07-java-regression-library-linear-model %}