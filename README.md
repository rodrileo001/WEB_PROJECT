My Update
present

•	Signup
o	Error check for each field
o	User Role

•	Login

•	User Home Page
o	Users Task List only
o	Shows Open Task and Closed Tasks for User

•	Boss Page
o	Tasks per User
o	Unassigned Tasks
o	Priority Queue
o	Assigned, Unassigned, and Closed Tasks

•	New Task – Only Boss can do this
o	Increment Task Number by adding 1 to max
o	Check box to assign to self when creating
o	Or pick from user list



•	Task Page
o	Shows Details of Task
o	Some Details Can be Changed
o	Comments listed below
o	Shows Who submitted the comment – 
	Landing Page with all Tasks (only doing this to show user roles)
	This would account for other users making comments on tasks.
o	Add Comment
o	Remove Comment
	Can only be removed by the person that created it
	So, if boss adds comment, user cannot delete it.



•	Bugs
o	Add/Remove Comment post issues, have it directed back to Home for now
o	Modal needs to be rendered at body level in the DOM to center over everything. 




# HERES OUR WEB PROJECT YAY 

Basically we're gonna do these things: 

1) User can login or create an account of a few different types
2) Depending on the user type, it will display a nice looking web page with some sort of pre-defined to-do list that may update some sort of user's to-do list (like it's some sort of company task-management system
3) If user is the big boss, they can create tasks. If the user is lower on the food chain, they can complete tasks and mark them as such. 

As far as the specifics go (i.e. what we display to each type of user, what types of users there should be, what the default tasks should be, etc), we can decide as a group and I'll update this readme with that stuff. 

## TODOS: 

 - Meet up and decide what we're actually gonna do for each user, what sort of stuff we wanna display, if we have better ideas than what are basically to-do lists, etc. 
 - Make all of the pages for each user type 
 - get familiar with git and related whats-its and what-have-yous 

## HERE'S A GUIDE ON GETTING SET UP 

This guide assumes that you're using something other than PyCharm and have Python3 installed. If you're unable to follow this guide, you can ask me how to get set up but this is the real man's way of doing stuff

1) Clone the repo 

- Open up your favorite terminal and sauce up a `git clone https://github.com/cadenforrest/WEB_PROJECT.git`, or `git clone git@github.com:cadenforrest/WEB_PROJECT.git` for the gangsters who already have SSH auth enabled. 

2) Create a virtual environment 
- navigate to the repository `cd WEB_PROJECT`
- run `python3 -m venv venv`
- This will create a folder called `venv` in your directory. 

3) Activate your virtual environment 
- `source venv/bin/activate` <- for MacOS and linux users
- `.\venv\Scripts\activate` <- or something like this for windows nerds, god bless your souls 
- If it worked, your terminal will hang for a second and then you should see `(venv)` next to your prompt in your terminal. 

4) Install the necessary dependencies 
- `pip install -r requirements.txt`

5) Run the app and start developing the stuff 
- `python3 main.py`

## MAKE A BRANCH FOR YOURSELF 
For the love of god, please don't push to the master branch without your code actually working, bc you might mess your teammates up a bit. 
To make a branch for yourself, do the following in your terminal: 

- `git branch your_branch_name_goes_here`
- `git checkout your_branch_name_goes_here`

After that, you can make all the changes you want and go wild. The following will be the general workflow: 

- `git add *` <- this is you telling git to add all of your changes to be staged for commit
- `git status` <- this will show you everything you're about to commit
- `git commit -m "your message goes here go wild"` <- this commits your changes *locally* with a comment
- `git push` <- this pushes all of your commits so far to the repo on the interweb

------------------------------------------------------------------------------------------------------------------------------------------
Using Git and GitHub for PyCharm

Need to have a GitHub account

**Assuming you have git installed**
To set up Git in PyCharm:

1.) Click on VCS on the PyCharm toolbar
2.) Click on ‘Enable Version Control Integration’
3.) Select ‘Git’ then press Ok

To clone repository into PyCharm  
1.) Click on Git on the PyCharm toolbar then click Clone
2.) copy and paste the repository URL into the URL space.
3.) Click Ok and you should have the available project in PyCharm displayed.

**For this particular Project**
In terminal, install the proper packages, including requirements.txt (if not included)
Example: (newer version of Python) pip3 install -r requirements.txt in terminal

Accessing Project repository with multiple contributors

Users will create a personal fork on GitHub for project so that they could edit and Push their changes so that a Pull Request can be submitted into the master branch.
