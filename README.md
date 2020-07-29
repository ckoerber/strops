![![Tests](https://github.com/ckoerber/strops/workflows/Tests/badge.svg?branch=master)
](https://github.com/ckoerber/strops/actions/)

# Strops

## Install

This module is pip installable.
```bash
pip install [--user] -e .
```
The `-e` option symlinks the install against this folder and is relevant for now.

This installs the `strops` command line interface into your Python bin.

## Init strops for the first time

#### Specify to which database you want to connect
The fastest route is copying
```bash
cp app/db-config-example.yaml app/db-config.yaml
```
And change the `NAME` value to an absolute path (it does not matter where; the absolute path is important if you want to run the CLI from any folder.)

For more advanced options, see also the [EspressoDB manual](https://espressodb.readthedocs.io/en/latest/Usage.html#configure-your-project).

Once done, you install tables in the DB by running
```bash
strops migrate
```

#### Inserting first trial data

To inspect the data in the admin interface, you first need to create a superuser
```bash
strops createsuperuser
```
This information is stored in the DB you have specified above.

Initial data is load-in by running
```bash
strops init-data
```
And that's it.

#### Running a server locally

You can launch a server locally by running
```bash
strops runserver
```
