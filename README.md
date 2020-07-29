[![Tests](https://github.com/ckoerber/strops/workflows/Tests/badge.svg?branch=master)
](https://github.com/ckoerber/strops/actions/)

# Strops

Data interface for connection interactions of the strong force and beyond to experiments.

![Demo image](https://raw.githubusercontent.com/ckoerber/strops/master/strops/static/img/demo.png)


## Details

Interested in the physics? [Take a look at the about page](https://strops-dev.ckoerber.com/about/).

This project aims at providing an open-source module for the systematic mapping of BSM-quark-gluon interactions over BSM-nuclear interactions to experimental observables.
The primary BSM candidate for the module is mapping DM structures&mdash;though different processes like searches for 0𝜈ββ decays are of interested as well.
The module is intended to allow setting parameters at the SM-BSM scale to obtain all relevant operators (combined chiral and BSM parameter expansion) in the desired basis to be used in many-nucleon computations.
Furthermore, it is intended to collect and connect existing computations to implemented operators.
This module is expected to benefit the experimental community in translating measurements to fundamental constraints and helps the high-energy theory community provide input for many-nucleon computations.
Systematic improvements in intermediate results, like improvements in the computation of related SM parameters, are intended to be incorporated in a database such that continuous progress will be shared.

## Disclaimer

This project is work in progress (early alpha).
While interest, feedback, and help in any form are appreciated, we emphasize that details may change and advise you not to base your computations on the current state, yet.

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
And change the `NAME` value to an absolute path (it does not matter where; the absolute path is crucial if you want to run the CLI from any folder.)

For more advanced options, see also the [EspressoDB manual](https://espressodb.readthedocs.io/en/latest/Usage.html#configure-your-project).

Once done, you install tables in the DB by running
```bash
strops migrate
```

###### Version notes

To account for changing data structures, this module makes uses of `JSONFields` which are enabled through Django's ORM with version 3.1 (currently alpha).
If you want to use a SQLite database as a backend, make sure it has [enabled the JSON1 extension](https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.JSONField).

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

## Contributing

Thanks for your interest in contributing!
There are many ways to contribute to this project.
For now, helping by providing data is of particular interest.
In case you want to know more, [get started here](CONTRIBUTING.md).


## License

BSD 3-Clause License. See also the [LICENSE](LICENSE.md) file.
