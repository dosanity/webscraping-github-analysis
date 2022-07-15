# Webscraping Analysis on GitHub Repositories

# We will be scraping GitHub repositories and organize the information in a Pandas dataframe.
# After that, we will use linear regressions to gain meaningful insights on the data we collected.

# imports and setup
from bs4 import BeautifulSoup
# you can use either of these libraries to get html from a website
import time
import os

import pandas as pd
import scipy as sc
import numpy as np

import statsmodels.formula.api as sm

import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 6)
# where the data is stored
DATA_PATH = "data"

### Scrape GitHub Repository List using BeautifulSoup

# We will be scraping data from [this repository list](https://github.com/search?o=desc&q=stars%3A%3E1&s=stars&type=Repositories).

# Before we can start to scrape any website we should go through the terms of service and policy documents of the website.
# Almost all websites post conditions to use their data. Here is the terms of [https://github.com/](https://github.com/).
# In our case, we are allowed to scrape the repository, but all use of GitHub data gathered through scraping must comply with
# the GitHub Privacy Statement.

# We avoided any problems with GitHub blocking us from downloading the data by saving all the html files in the data folder.
# The path to data folder is stored in `DATA_PATH` variable. Additionally, the data folder contains highly starred repositories
# saved as `searchPage1.html`,`searchPage2.html`,`searchPage3.html` ... `searchPage10.html`

# We will create a single soup using BeautifulSoups' [append()](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#append) function.

soup = BeautifulSoup(open(DATA_PATH + "/searchPage1.html"), "html.parser")
for i in range(2, 10):
    html = (DATA_PATH + "/searchPage" + str(i) + ".html")
    soup.append(BeautifulSoup(open(html, encoding = "utf8"), "html.parser"))

### Extract Data

# We will now extract the certain data for each repository and create a Pandas Dataframe with a row for each repository and a column for each of these datums.

# The name of the repository
# The primary language (there are multiple or none, if multiple, use the first one, if none, use "none")
# The number of stars
# Number of forks
# Number of commits
# Number of branches
# Number of contributors
# Number of issues
# Length of readme file.

import urllib.request

repo_list = soup.find_all(class_="repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source")

links = []
for repo in repo_list:
    repo_name = repo.find('a').text.split("/")
    name = repo_name[0].strip()
    link = name

    links.append(link)
links

links1 = []
for repo1 in repo_list:
    repo_name1 = repo1.find('a').text.split("/")
    name1 = repo_name1[1].strip()
    link1 = name1

    links1.append(link1)

data = []
for i in range(len(repo_list)):
    soup1 = BeautifulSoup(open(DATA_PATH + "/" + links[i] + "/" + links1[i] + ".html", encoding="utf8"), "html.parser")
    # name
    name = soup1.find(class_='mr-2 flex-self-stretch').text.strip()
    # language
    if soup1.find(class_="d-flex repository-lang-stats-graph") == None:
        language = "None"
    else:
        language = soup1.find(class_="d-flex repository-lang-stats-graph").text.split()[0]
        if language == "Jupyter":
            language1 = soup1.find(class_="d-flex repository-lang-stats-graph").text.split()[0]
            language2 = soup1.find(class_="d-flex repository-lang-stats-graph").text.split()[1]
            language = language1 + ' ' + language2
        else:
            language = soup1.find(class_="d-flex repository-lang-stats-graph").text.split()[0]

    watches, stars, forks = soup1.find_all(class_="social-count")
    # stars
    stars = stars["aria-label"].split()[0]
    stars = int(stars)

    # watches
    watches = watches["aria-label"].split()[0]
    watches = int(watches)

    # forks
    forks = forks["aria-label"].split()[0]
    forks = int(forks)

    # commits
    commits = soup1.find(class_="commits").text.split()[0]
    commits = int(commits.replace(',', ""))

    num_sum = soup1.find_all(class_="text-emphasized")
    # branches
    branches = num_sum[1].text.split()[0]
    branches = int(branches.replace(',', ""))

    # contributors
    contributors = num_sum[4].text.split()[0]
    contributors = contributors.replace('+', "")
    if contributors == '∞':
        contributors = 15600
    else:
        contributors = int(contributors.replace(',', ""))

    counter = soup1.find_all(class_="Counter")

    # issues
    issues = counter[0].text.strip()
    issues = issues.replace("+", "")
    issues = int(issues.replace(',', ""))
    issues

    # length of readme
    readme = len(soup1.select('div.Box-body')[0].get_text())

    data.append(
        {"name": name, "language": language, "stars": stars, "watches": watches, "forks": forks, "commits": commits,
         "branches": branches, "contributors": contributors, "issues": issues, "readme": readme})

project_info = pd.DataFrame(data)
project_info.to_csv('project_info.csv', index=False)
print(project_info)

# Note: There was one repository flagged as having infinite contributers (the Linux kernel).
# We will assume that it has 15600 contributors. This is an estimate based on a google search.
# Further, another repository has "5000+" issues, we will assume it will be just 5000.

## Analyzing the Repository Data

# We will now analyze the data collected using regression tools.
# The goal is to identify properties that make a repository popular.

project_info = pd.read_csv('project_info.csv')
project_info.head()

### Describing the Data

# We will get an overview of the data and compute the correlation matrix.
# Additionally, we will visualize it with a heat map and creating a scatterplot matrix.

print(project_info.describe())

project_corr = project_info.corr()
print(project_corr)

fig, ax = plt.subplots()
heatmap = plt.pcolor(project_corr, cmap=plt.cm.PuBuGn, vmin = -1, vmax = 1)
xy = project_corr.columns.tolist()
plt.xticks(np.arange(0.5, len(xy), 1), xy, rotation = 'vertical')
plt.yticks(np.arange(0.5, len(xy), 1), xy)
plt.title("Correlation Matrix")
plt.colorbar(heatmap)
# plt.show()

import seaborn as sns
rel = sns.pairplot(project_info, diag_kind="kde")

# #move title up
rel.fig.subplots_adjust(top=.95)

#add overall title
rel.fig.suptitle('Scatterplot Matrix', fontsize = 20)

plt.savefig('seaborn.png')

# From these charts, we can see that there is a positive correlation between commits and contributions with the
# correlation being 0.933. Additionally, there is a positive correlation between the number of forks and the number
# of watches with the correlation being 0.71. This number is approximately similar to correlation between the number
# of watches and the number of stars. All other variables don't have much of a correlation with one another.

### Linear Regression

# Now we will use a linear regression to try to predict the number of Stars based on Forks, Contributors, Issues, and README Length.
# We will also use a linear regression to try to predict the number of Stars based on Forks, Contributors, Watches, Commits, and README Length.

uni_mod = sm.ols(formula="stars ~ forks + contributors + issues + readme", data = project_info)
uni_result = uni_mod.fit()
uni_result.save("longley_results.png")
print(uni_result.summary())

uni_mod = sm.ols(formula="stars ~ forks + contributors + watches + commits + readme", data = project_info)
uni_result = uni_mod.fit()
print(uni_result.summary())

# From our regressions, the first model is not a good model because it has a low R-squared of 0.227, the p-values
# for the variables show that they are insignificant, and the prob f-statistic is small. With a low R-squared,
# it indicates that the independent variable is not explaining much in the variation of the dependent variable.
# The variable forks is significant at the 5% level, but all other variables are insignificant. Thus overall, the
# first model is not a good model.  The second model is better because the R-squared is higher than the first at
# 0.598 so around 60% of the variation is explained. Additionally, the prob f-statistic is smaller than the first model.
# Furthermore, commits, watches, and contributors is significant at the 5% level. Overall, the second model is better
# as a result from these differences.