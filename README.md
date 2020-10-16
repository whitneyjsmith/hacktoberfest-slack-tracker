# hacktoberfest-slack-tracker #

Python tool that allows setting up tracking of hacktoberfest PRs with congratulatory messages in slack.


## Supported commands ##
- `/register-hacktoberfest-tracking GITHUB_USERNAME`  register your Github account


## Installing and running locally ##
Out of the box, hacktoberfest-slack-tracker will reference several environment variables that it needs to run. You can add these to your local environment/venv/virtualenv/etc, or you can create a local settings file.

Hacktoberfest-slack-tracker supports `local.py` files in the core/settings folder. There is a provided template called `local.py.template` that you can use to set up your `local.py` file. Just fill in the empty settings and you'll be good to go! (Due to the likely possibility of someone's local settings file being committed to version control and unintentially exposing their credentials, `local.py` has been removed from version control, which is why you won't see it in the repo)
If django is unable to find a local settings file, it will use the settings in `production.py`, which will load all needed items from the environment.

If you would prefer to not use the local settings file, or you are deploying to a production environment, hacktoberfest-slack-tracker requires the following environment variables to run:
- DATABASE_URL
- SECRET_KEY
- GITHUB_USER
- GITHUB_TOKEN