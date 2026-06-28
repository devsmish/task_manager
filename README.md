# Task Manager

## Overview
Simple Django-based Task Manager application with support for tasks, subtasks, and categories.

## Features
- Task, SubTask, Category models
- Task categorization (Many-to-Many)
- Task status tracking
- Django Admin integration
- **REST API Endpoints (v1) with Django REST Framework** (Tasks & SubTasks CRUD) 🚀
- **Advanced Serializer Validation & Nested Relations** 🛡️
- **Dynamic Task Statistics & Analytics** 📊
- **Query Parameters, Extract Methods & Pagination** 🔍

## Admin Panel
Access `/admin` to manage:
- Tasks
- SubTasks
- Categories

## Releases

Release v0.2.2
### 🔍 Request Query Parameters, Date Component Extraction & Pagination

This release enhances the existing API endpoints by introducing advanced querying, performance-optimized filtering, and data pagination mechanics:

* **SubTask Pagination:** Integrated `PageNumberPagination` to split the subtask data layer, restricting payload responses to a maximum of **5 objects per page**.
* **Strict Chronological Ordering:** Enforced descending database-level sorting (`-created_at`) across subtask listings, ensuring the newest items always appear first.
* **Database Date Components:** Implemented precise task filtering by days of the week by utilizing Django's structural `ExtractWeekDay` method inside an analytical annotated aggregation layer.
* **Combined Query Parameter Filtering:** Developed chained filtering pipelines (logical `AND`) for subtasks, supporting case-insensitive partial parent title matches (`task__title__icontains`) and exact status filters simultaneously.
* **Code Optimization:** Conducted a comprehensive code cleanup by removing redundant, non-optimized endpoint view mappings and reducing database round-trips.

Release v0.2.1
### 🛠️ Advanced Serializers, Validation & SubTask APIViews

This release expands the REST API layer by adopting object-oriented Class-Based Views, complex business logic validation, and deep serialization mapping:

* **SubTask API (Class-Based Views):** Implemented clean, robust CRUD endpoints for subtasks management (`GET` / `POST` under `/api/v1/subtasks/` and `GET` / `PUT` / `DELETE` under `/api/v1/subtasks/<id>/`) using DRF's `APIView`.
* **Nested Serializer Relations:** Upgraded task lookups so that fetching detailed task data dynamically includes all associated subtasks via a nested `subtask_set` configuration.
* **Strict Business Validation:** Added an automated timezone-aware validation hook to reject past deadlines during task creation, and overrode `create`/`update` layers for categories to manually enforce name uniqueness.
* **Data Integrity:** Explicitly isolated core auto-generated fields (such as `created_at`) as `read_only` across serialization entry points to protect timestamps from manual manipulation.

Release v0.2.0
### 🚀 Core REST API Implementation (v1)

The system now includes a fully functional REST API built with Django REST Framework, featuring proper API versioning and secure validation:

* **API Versioning:** All endpoints are strictly versioned and exposed under the `/api/v1/` prefix for maximum compatibility.
* **Task Management Endpoints:** Added secure endpoints for task creation (`POST /api/v1/tasks/create/`) with type validation, fetching all tasks (`GET /api/v1/tasks/`), and retrieving a specific task by ID (`GET /api/v1/tasks/<id>/`) with safe `404 Not Found` error handling.
* **Dynamic Analytics:** Integrated a dedicated aggregation endpoint (`GET /api/v1/tasks/statistics/`) that computes total task counts, breakdown analysis based on model statuses, and real-time overdue metrics using Django's timezone engine.
* **Architecture:** Implemented structured ModelSerializers and decoupled URL routing to separate API concerns from the core Django views.

Release v0.1.1
### 📋 Task & Subtask Management (Admin Panel)

The system includes a customized Django Admin interface tailored for efficient task tracking:

* **Inline Subtask Editing:** Subtasks can be created, updated, or removed directly from the parent Task's editing form without switching pages.
* **Smart Text Truncation:** To keep the Task dashboard clean, task names in the main list view are automatically truncated to 10 characters if they exceed that limit. Full names are strictly preserved in dropdowns and selection menus to avoid ambiguity.
* **Bulk Operations:** Administrators can update multiple subtasks simultaneously. Use the **\"Actions\"** dropdown in the Subtasks list view to instantly mark all selected items as **Done**.

Release v0.1.0
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
pip install djangorestframework
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
