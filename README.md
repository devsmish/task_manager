# Task Manager

## Overview
Simple Django-based Task Manager application with support for tasks, subtasks, and categories.

## Features
- Task, SubTask, Category models
- Task categorization (Many-to-Many)
- Task status tracking
- Django Admin integration

## Admin Panel
Access /admin to manage:
Tasks
SubTasks
Categories

## Setup

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
