# Book-A-Meal-db

[![Build Status](https://travis-ci.org/gloriaodipo/Book-A-Meal-db.svg?branch=develop)](https://travis-ci.org/gloriaodipo/Book-A-Meal-db) [![Coverage Status](https://coveralls.io/repos/github/gloriaodipo/Book-A-Meal-db/badge.svg?branch=develop)](https://coveralls.io/github/gloriaodipo/Book-A-Meal-db?branch=develop)

Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat.
## Features
- Users can create an account and log in
- Admin (Caterer) should be able to manage (i.e: add, modify and delete) meal options in the application. Examples of meal options are: Beef with rice, Beef with fries etc
- Admin (Caterer) should be able to setup menu for a specific day by selecting from the meal options available on the system.
- Authenticated users (customers) should be able to see the menu for a specific day and select an option out of the menu.
- Authenticated users (customers) should be able to change their meal choice.
- Admin (Caterer) should be able to see the orders made by the user
- Admin should be able to see amount of money made by end of day

## Required technology:
- [PostgreSql](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) (database and ORM)
- [Flask](http://flask.pocoo.org/) (A Python microframework)

## Tools:
- [VirtualEnv](https://virtualenv.pypa.io/en/stable/) (Stores all dependencies used in the project)
- [Pivotal Tracker](www.pivotaltracker.com) (A project management tool)
- [Pytest](https://docs.pytest.org/en/latest/) (Tool for testing)

Getting Started:
Note: Please Ensure you have python3 installed in your machine

To start this app, please follow the instructions below:

On your terminal:

Install pip

sudo apt-get install python-pip

Clone this repository

git clone https://github.com/gloriaodipo/Book-A-Meal-db.git

Get into the root direcory

cd Book-A-Meal-db/

Install virtualenv

pip install virtualenv

Create a virtual environment in the root directory

virtualenv <name of virtualenv>

Activate the virtualenv

source <name of virtualenv>/bin/activate

Install the requirements of the project

pip install -r requirements.txt

Create a file in the root directory called .env and add the two lines below

export FLASK_APP="run.py"

export SECRET="some random string"

Activate the env variables

source .env

Run the application

flask run

Then run tests

pytest tests
