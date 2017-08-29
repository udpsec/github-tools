import sys
import getpass
import github


def login():
    a = raw_input("Account: ")
    p = getpass.getpass("Password: ")
    g = github.Github(a, p)
    u = g.get_user()

    try:
        logged_in = u.login
    except github.BadCredentialsException, e:
        print "\nCouldn't log in. Again? (y)"

        if raw_input() == "y":
            return login()
        else:
            sys.exit(1)

    return u


def delete_starred_repos():
    print "\nAttempting to delete."

    for repo in u.get_starred():
        u.remove_from_starred(repo)
        global deleted
        deleted += 1

    if deleted == 0:
        print "\nYes! No more starred repositories!"
        print "Have a good day!"
    else:
        return delete_starred_repos()


def act(answer):
    if answer == "y":
        delete_starred_repos()
    else:
        sys.exit(1)


def inform():
    print "\nYou will be deleting all the starred repositories from your GitHub account ({}).".format(u.login)
    print "Do you want to continue? (y)"


deleted = 0

u = login()
inform()
act(raw_input())
