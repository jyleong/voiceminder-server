# Voiceminder Server
Repository the Voiceminder database and REST API

### Environment Setup
Install python3:
```
> brew upgrade python3
```

Install and configure virtualenv:
```
> pip install virtualenv
> mkdir ~/Python_envs
> cd ~/Python_envs
> virtualenv -p /usr/local/Cellar/python3/3.6.2/bin/python3 voiceminder
```

# Using and Updating the Environment:
Anytime you want to activate this environment:
```
> source ~/Python_envs/voiceminder/bin/activate
```

You will know if you have the environment activated or not from your
command line prompt:
```
(voiceminder) >
```

All the required python packages are defined in the
requirements.txt file. Use the `pip` command to install or
upgrade. Remember you need to do this each time someone adds a required
package to the project.
```
(voiceminder) > pip3 install -r requirements.txt
```

To add a required package to the project, use the `pip freeze` command:
```
(voiceminder) > pip3 freeze > requirements.txt
```

Run instructions
install mysql
make database voiceminder
export environment variables:
```
(voiceminder) > source voiceminder.env
(voiceminder) > python3 src/manage.py db init
(voiceminder) > python3 src/manage.py db migrate
(voiceminder) > python3 src/manage.py db upgrade
(voiceminder) > python3 src/manage.py seed
(voiceminder) > python3 src/run.py
```

install localtunnel via localtunnel.me
launch in terminal
> lt -s voiceminder -p 5000

This launches api as https://voiceminder.localtunnel.me
