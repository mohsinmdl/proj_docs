# Git Guide 101
***
## Commit
The "commit" command is used to save your changes to the local repository.
***




### Initialized a repository

```commandline
git init
```

### Add a file to the staging area

```commandline
git add --all

```

### Commiting files
```commandline
git commit -m "message"
git commit -am "message with adding file to the staging area "
```
### Repository log
```commandline
git log
```
### Repository status
```commandline
git status 
```

### Unstaging files
``` sh
git reset --hard


git diff <1stVer commit hash> <LastVer commit hash> ::	difference btw changes made 

```
## Branch
In Git, branches are a part of your everyday development process. Git branches are effectively a pointer to a snapshot of your changes. When you want to add a new feature or fix a bug—no matter how big or how small—you spawn a new branch to encapsulate your changes. This makes it harder for unstable code to get merged into the main code base, and it gives you the chance to clean up your future's history before merging it into the main branch.
***



### Create a branch
```commandline
git branch <branch-name>
git checkout -b <branch-name>
```
### Merging a branch
```commandline
git merge <source-branch-name>
```
### Listing branches 
```commandline
git branch 
git brach --list
```
### Removing a branch
```commandline
git brach -d
```
### Create a tag
```commandline
git tag <tag-name>
```
### Replace a tag
```commandline
git tag -f <new-tag-name>
```
### Listing tags
```commandline
git tag -l
git tag
```
### Removing a tag
```commandline
git tag -d <tag-name>
```

## Fixing Common issues
***

### 
```commandline
git log --oneline
```

### Ammend wiht previous commits
```commandline

git status
git add --all
git commit ammend
git log --oneline
```
!!! warning "Be carefull!"
    When you `ammend` a commit, this will remove the tag from the commit if it has already

### Add tag to the latest ammend
```commandline
git tag
git log --online
git tag -f <update-tag>
```


### Show all changes
```commandline
git reflog

```
### Checkout differert state in the repository
```commandline
git reset HEAD@{5}
```
`Changes sitting there`

#### older version of this file
```commandline
git reset --hard


or

git reset HEAD@{3} --hard
```

### Reset Back to previous commits. 
```commandline
git log --oneline
git reset HEAD~2 --hard

```

### Last Commit gone but changes sitting there
```commandline
git reset HEAD~ --soft
```
### Stash -- file no need to put into stage
```commandline
git stash
```
### Taking stash file to the staging folder
```commandline
git stash pop
git add --all
git commit -m "<message>"
```




### Switch between branches A/B B/A 
```commandline
git checkout - 

``` 


# push an existing repository from the command line
```commandline
git remote add origin https://github.com/mohsinmdl/GTIN-Prediction-System.git
git push -u origin master

```












