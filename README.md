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

Releases

Release v 0.1.1
### 📋 Task & Subtask Management (Admin Panel)

The system includes a customized Django Admin interface tailored for efficient task tracking:

* **Inline Subtask Editing:** Subtasks can be created, updated, or removed directly from the parent Task's editing form 
* without switching pages.
* **Smart Text Truncation:** To keep the Task dashboard clean, task names in the main list view are automatically 
* truncated to 10 characters if they exceed that limit. Full names are strictly preserved in dropdowns and selection 
* menus to avoid ambiguity.
* **Bulk Operations:** Administrators can update multiple subtasks simultaneously. Use the **"Actions"** dropdown in the 
* Subtasks list view to instantly mark all selected items as **Done**.

Release v 0.1.0
### Core Models
- Category model for task grouping
- Task model with status tracking and deadlines
- SubTask model linked to Task

### Relationships
- Task ↔ Category (Many-to-Many)
- SubTask → Task (ForeignKey)

### Django Admin
- All models registered in admin panel
- Basic admin configuration for data management

### Data Layer
- Database migrations created and applied
- Initial test data added via Django Admin

## Setup

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
