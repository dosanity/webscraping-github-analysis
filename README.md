# Webscraping Analysis on GitHub Repositories

## Overview of Project

### Purpose
There are many GitHub repositories and some are more popular than others. A Git repository tracks and saves the history of all changes made to the files in a Git project. It saves this data in a directory called . git, also known as the repository folder. Git uses a version control system to track all changes made to the project and save them in the repository. In this project, we will be scraping GitHub repositories and organizing the information in a Pandas data frame. After that, we will use linear regressions to gain meaningful insights into the data we collected. Our goal is to identify properties that make a repository popular which will give insights into future uses of repositories.

## Webscraping Process

### Scrape GitHub Repository List using BeautifulSoup

We will be scraping data from [this repository list](https://github.com/search?o=desc&q=stars%3A%3E1&s=stars&type=Repositories).

Before we can start to scrape any website we should go through the terms of service and policy documents of the website. Almost all websites post conditions to use their data. Here are the terms of [https://github.com/](https://github.com/). In our case, we are allowed to scrape the repository, but all use of GitHub data gathered through scraping must comply with the GitHub Privacy Statement.

We avoided any problems with GitHub blocking us from downloading the data by saving all the HTML files in the data folder. The path to the data folder is stored in the `DATA_PATH` variable. Additionally, the data folder contains highly starred repositories saved as:

 `searchPage1.html`, `searchPage2.html`, `searchPage3.html` ... `searchPage10.html`

### Extract Data

We extracted the following data:

+ The name of the repository
+ The primary language
+ The number of watches
+ The number of stars
+ Number of forks
+ Number of commits
+ Number of branches
+ Number of contributors
+ Number of issues
+ Length of readme file.

## Analyzing the Repository Data

### Describing the Data

We will get an overview of the data and compute the correlation matrix.

![Correlation-Matrix](https://user-images.githubusercontent.com/29410712/179305275-7e920928-9b40-4255-9cf7-23c51cba7181.png)

Additionally, we will visualize it with a heat map and create a scatterplot matrix.

![seaborn](https://user-images.githubusercontent.com/29410712/179307109-0614e5ce-c5cc-4add-9ec7-345fdf7eb59a.png)

From these charts, we can see that there is a positive correlation between commits and contributions with the correlation being 0.933. Additionally, there is a positive correlation between the number of forks and the number of watches with the correlation being 0.71. This number is approximately similar to the correlation between the number of watches and the number of stars. All other variables don't have much of a correlation with one another.

### Linear Regression Models

Now we will use linear regression to try to predict the number of Stars based on Forks, Contributors, Issues, and README Length.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  stars   R-squared:                       0.227
Model:                            OLS   Adj. R-squared:                  0.191
Method:                 Least Squares   F-statistic:                     6.244
Date:                Fri, 15 Jul 2022   Prob (F-statistic):           0.000187
Time:                        14:41:51   Log-Likelihood:                -1071.6
No. Observations:                  90   AIC:                             2153.
Df Residuals:                      85   BIC:                             2166.
Df Model:                           4                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept     4.738e+04   7345.923      6.449      0.000    3.28e+04     6.2e+04
forks            1.4623      0.326      4.491      0.000       0.815       2.110
contributors     1.8914      2.310      0.819      0.415      -2.701       6.483
issues          -1.6891      3.223     -0.524      0.602      -8.097       4.719
readme          -0.0058      0.134     -0.043      0.965      -0.272       0.260
================================================================================
Omnibus:                      104.465   Durbin-Watson:                   0.442
Prob(Omnibus):                  0.000   Jarque-Bera (JB):             1509.964
Skew:                           3.814   Prob(JB):                         0.00
Kurtosis:                      21.560   Cond. No.                     6.49e+04
================================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 6.49e+04. This might indicate that there are
strong multicollinearity or other numerical problems.
```
We will also use linear regression to try to predict the number of Stars based on Forks, Contributors, Watches, Commits, and README Length.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  stars   R-squared:                       0.598
Model:                            OLS   Adj. R-squared:                  0.574
Method:                 Least Squares   F-statistic:                     24.94
Date:                Fri, 15 Jul 2022   Prob (F-statistic):           2.54e-15
Time:                        14:00:23   Log-Likelihood:                -1042.3
No. Observations:                  90   AIC:                             2097.
Df Residuals:                      84   BIC:                             2112.
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
Intercept     2.285e+04   5718.815      3.996      0.000    1.15e+04    3.42e+04
forks           -0.5362      0.332     -1.616      0.110      -1.196       0.124
contributors    15.9343      4.764      3.345      0.001       6.461      25.407
watches         17.7592      2.275      7.805      0.000      13.234      22.284
commits         -0.3285      0.085     -3.848      0.000      -0.498      -0.159
readme          -0.1416      0.098     -1.448      0.151      -0.336       0.053
==============================================================================
Omnibus:                       72.640   Durbin-Watson:                   1.149
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              634.454
Skew:                           2.397   Prob(JB):                    1.70e-138
Kurtosis:                      15.092   Cond. No.                     1.98e+05
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.98e+05. This might indicate that there are
strong multicollinearity or other numerical problems.
```
From our regressions, the first model is not a good model because it has a low R-squared of 0.227, the p-values for the variables show that they are insignificant, and the prob f-statistic is small. A low R-squared indicates that the independent variable is not explaining much of the variation of the dependent variable. The variable forks are significant at the 5% level, but all other variables are insignificant. Thus overall, the first model is not a good model.  The second model is better because the R-squared is higher than the first at 0.598 so around 60% of the variation is explained. Additionally, the prob f-statistic is smaller than the first model. Furthermore, commits, watches, and contributors are significant at the 5% level. Overall, the second model is better as a result of these differences.

### Challenges and Difficulties Encountered
The data from the GitHub repository is always changing and we did not program to actively take in data. Instead, we saved the HTML files to access the data at a certain point in time. Although this is a good enough sample for this analysis, it could potentially be more accurate if there was a program taking in live data from the GitHub repository. It was also difficult and time-consuming to navigate through the HTML files to scrape the data. We overcame this through for loops to salvage the code.

## Results
- As stated above, our goal was to identify properties that make a repository popular which will give insights into future uses of repositories. In our findings, we can conclude that commits, watches, and contributors in repositories are statistically significant. In other words, as the number of commits increases by 1, the number of stars decreases by 0.33 percentage points. Moreover, as the number of watches increases by 1, the number of stars increases by 17.76 percentage points. Finally, as the number of contributors increases by 1, the number of stars increases by 15.93 percentage points. Forks and README Length are both statistically insignificant. 


