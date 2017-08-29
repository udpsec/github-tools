
![](logo.png)

# Github Star Purge

This is a Python script that will help you remove **all** of the stars from your github profile.

Its use is straightforward:

1. Clone the github_star_purge repo:  ``git clone https://www.github.com/Dowwie/github_star_purge.git``
2. Change to the repo directory:  ``cd github_star_purge``
3. Create a Python3 virtual environment:  ``pyvenv my_venv``
4. Activate your newly created Python virtual environment:  ``source my_venv/bin/activate``
5. Install the github_star_purge package and its Github API dependency:  ``python setup.py install``

The utility installs itself as an executable script from within the activated
virtual environment.  So, at this point you can run it from the command line: 

``github_star_purge <username> <password>``

When you are finished removing your stars, simply type ``deactivate`` to 
exit the virtual environment.
