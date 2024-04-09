# Advanced Python Final Project: Trivia Application

A final project for my Advanced Programing: Python class. It's a containerized trivia web app built using Flask and PyMongo, styled with flake8, and tested with unittest. To provide trivia questions, the app makes requests to the OpenTrivia API endpoint.

## Outcomes

This project gave me a working understanding of the Flask and unittest frameworks, bash scripting, containerized applications, API requests, CI pipelines and GitHub hooks.

## Requirements
- Appropriate Atlas PEM certificate in the top level directory of the app.

## How to use
Run the container and execute with Python to start the Flask app:

```
./run.sh
python src/app.py
```

## Self-grade
I would give this assignment full points:
- Worked in a team of 4
- Public GitHub project used
- Public GitHub repo used
- Uses a public REST API, MongoDB and Flask
- GitHub project used to manage team and issue creation, assignment
- Docker container used, git best practices
- At least one issue was assigned to each team member
- At least one branch for each issue created
- Uses flake8, mypy, unittest as provided
- Makefile automates all test runs
- [Screenshots of tests](https://github.com/syncorex/advpy-web-app/tree/main/screenshots)
- CI/CD checks passed when pushing to main in container
