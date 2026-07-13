# Task Manager

## Overview
Simple Django-based Task Manager application with support for tasks, subtasks, and categories.
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

Release v0.7.0
### ⚡ Automated Task Lifecycle Signals, Owner Email Notifications & Idempotency Guards

This milestone introduces an automated notification subsystem powered by Django event signals, enabling real-time email 
alerts for task state modifications while establishing strict delta validation to eliminate duplicate communication 
channels:

* **Task Lifecycle Signals (Closes #74):** Engineered a `pre_save` signal layer bound to the core `Task` model to 
* dynamically intercept task updates, state transitions, and absolute closures.
* **Owner Email Notification Routing (Closes #74):** Integrated an automated notification routine that compiles and 
* dispatches formatted text alerts directly to the assigned task `owner` email whenever a valid status change is 
* detected.
* **Idempotency & Anti-Spam Verification (Closes #74):** Implemented pre-save database delta checks to compare incoming 
* status values against existing database records, strictly suppressing notification triggers during consecutive saves 
* with unchanged statuses.
* **Console Email Engine Integration (Closes #74):** Configured a local development email ecosystem inside `settings.py` 
* using Django's console email backend to safely stream outbound email payloads directly to the server terminal for 
* debugging.

Release v0.6.0
### 🍪 Secure Cookie-Based Authentication, Automated Token Refresh & Token Blacklisting

This milestone hardens the authentication layer by transitioning session storage to client-side secure cookies, 
automating token lifecycles, and implementing a database-backed blacklist ecosystem to fully eliminate token replay 
vulnerabilities:

* **Secure Account Registration (Closes #65):** Established a strict account creation pipeline featuring deep field 
* validation, automated password hashing via Django's core validators, and ironclad uniqueness constraints on both 
* usernames and emails.
* **HTTP-Only Cookie Encapsulation (Closes #66):** Neutralized XSS injection threats by intercepting standard JWT 
* responses and embedding short-lived Access and long-lived Refresh tokens into cryptographic `httpOnly`, `Secure`, 
* and `SameSite=Lax` browser cookies.
* **Custom Cookie-Aware Auth Backend (Closes #67):** Engineered a specialized `JWTCookieAuthentication` provider that 
* transparently extracts and decodes access keys from incoming HTTP request cookies while maintaining structural 
* fallback compatibility for traditional Bearer tokens.
* **Server-Side Token Blacklisting & Session Purge (Closes #68):** Integrated an explicit database-backed 
* `token_blacklist` routine to permanently invalidate active refresh tokens upon logout, complemented by automated 
* client-side cookie deletion blocks to ensure comprehensive session termination.

Release v0.5.0
### 🛡️ User Ownership Isolation, Custom Object-Level Security & OpenAPI 3.0 Documentation

This milestone completes the security and documentation ecosystem by introducing multi-tenant data isolation, strict 
object-level access controls, and fully automated OpenAPI 3.0 interactive schemas:

* **Contextual User Extraction & Ownership:** Added an `owner` ForeignKey relation linked to the Django User model 
* across both Task and SubTask records. Overrode `perform_create()` view hooks to seamlessly bind the authenticated 
* `request.user` to newly created objects while protecting the database via read-only serializer controls.
* **Isolated Queryset Multi-Tenancy:** Restructured the `get_queryset()` pipelines on list endpoints, establishing 
* automatic database-level filtering so that users can strictly interact with data they own.
* **Granular Object permissions:** Engineered a custom `IsOwner` permission validator inside `permissions.py` to protect 
* specific resource IDs. Malicious or unauthorized attempts to alter or delete foreign rows now trigger an explicit 
* `403 Forbidden` termination block.
* **OpenAPI 3.0 Specs via drf-spectacular:** Deployed `drf-spectacular` to serve as the unified API blueprint engine. 
* Exposed secure paths for raw schema delivery (`/api/v1/schema/`), 
* responsive Swagger UI components (`/api/v1/schema/swagger-ui/`), 
* and clean ReDoc documentation interfaces (`/api/v1/schema/redoc/`).
* **Interactive JWT Interceptor:** Structured global configuration properties inside `settings.py` to embed native 
* JWT Bearer authentication locks into the Swagger interface, enabling seamless sandbox manual endpoint testing.

Release v0.4.0
### 🔐 Enterprise JWT Hardening, Global Protection Perimeter & Pagination Tuning

This milestone focuses on securing the API infrastructure against unauthorized access by deploying a stateless token 
authentication mechanism, sealing all endpoints behind a global security guardrail, and tuning delivery thresholds:

* **Stateless JWT Infrastructure:** Integrated `djangorestframework-simplejwt` to handle user sessions without 
* server-side state. Configured token lifecycles with a strict **60-minute** expiration window for Access tokens and 
* a **7-day** window for Refresh tokens to ensure high rotation security.
* **Exposed Token Rotation Endpoints:** Formulated public routing paths at `/token/` and `/token/refresh/` allowing 
* clients to seamlessly generate new keys and exchange expired tokens.
* **Global Security Perimeter:** Swapped open endpoints for a mandatory `IsAuthenticated` global permission rule inside 
* `settings.py`. Every active route (`/tasks/`, `/subtasks/`, `/categories/`) now implicitly drops anonymous connections 
* with a `401 Unauthorized` response block.
* **Optimized Pagination Limits:** Tuned the global REST framework `PAGE_SIZE` configuration along with the кастомный 
* `CustomCursorPagination` module, dropping the layout density from 6 to exactly **5 items per page** across all 
* resource models.

Release v0.3.0
### 🔐 Secure Global Cursor Pagination & Isolated Multi-Channel Logging Engine

This release focuses heavily on production infrastructure, application security, and advanced telemetry, hardening the 
API layer against data scraping and establishing granular observability:

* **Cryptographic Cursor Pagination:** Migrated from vulnerable page-index offsets to global `CursorPagination` wrapped 
* inside a custom framework layer. All list endpoints now mask page states behind secure token hashes (`?cursor=...`) 
* with a strict envelope size of **6 objects per page**.
* **Unified cross-model Sorting:** Standardized the underlying cursor pointer sorting around the unique `id` field, 
* completely neutralizing internal breaks on abstract models (like `Category`) that do not share timestamps.
* **Isolated Multi-Stream Logging:** Created a split-channel runtime logging grid that separates standard console 
* outputs from environment events, dumping incoming HTTP lifecycles into `logs/http_logs.log` and raw ORM-generated SQL 
* statements into `logs/db_logs.log`.
* **Self-Building Directories & Version Guardrails:** Introduced automated system setup scripts using `pathlib` to 
* generate required storage folders out-of-the-box, while reinforcing `.gitignore` parameters to prevent logging files 
* from spilling into open Git trees.

Release v0.2.4
### 🗂️ Category ViewSet, Custom Aggregations & Reusable Soft Deletion System

This release introduces a complete Category management system via unified viewsets, along with an enterprise-grade, 
highly reusable Soft Deletion architecture to preserve relational data integrity across the platform:

* **ModelViewSet Integration:** Exposed comprehensive CRUD capabilities for the `Category` model using a streamlined 
* `ModelViewSet`, wired automatically via DRF's `DefaultRouter`.
* **Dynamic Task Aggregation:** Added a custom `@action` detail endpoint (`count_tasks`) to compute and return total 
* active tasks associated with any given category.
* **Reusable Soft Deletion Engine:** Designed an abstract `SoftDeleteModel` and a custom `SoftDeleteManager` that 
* overrides default querysets to seamlessly filter out soft-deleted records from standard API responses.
* **Database Schema Synchronization:** Generated and applied required database migrations to introduce `is_deleted` and 
* `deleted_at` tracking layers without physical data loss.

Release v0.2.3
### 🛠️ DRF Generic Views Migration, Advanced Filtering & Full-Text Search

This release completely refactors the core view layer by replacing manual function-based views and boilerplate `APIView`
classes with Django REST Framework's robust **Generic Views**, while incorporating standardized filtering and data 
controls:

* **Generic Views Migration:** Refactored entire view pipelines for both Tasks and SubTasks models into optimized 
* `ListCreateAPIView` and `RetrieveUpdateDestroyAPIView` architectures.
* **Declarative Filter Backends:** Integrated `DjangoFilterBackend`, `SearchFilter`, and `OrderingFilter` to establish 
* uniform, enterprise-grade data query controls.
* **Multi-Field Case-Insensitive Search:** Enabled full-text search parameters (`?search=...`) evaluated dynamically 
* against both `title` and `description` model fields.
* **Precise Model Filtering:** Introduced query-driven filter pipelines for exact matching on `status` and `deadline` 
* variables across all entity indices.
* **Dynamic Serializer Class Routing:** Overrode `get_serializer_class()` layers to dynamically switch between 
* specialized schemas (e.g., applying strict input validation during writes and nested relational mappings for reads).
* **Unified Pagination Support:** Standardized data layer payloads by mapping custom pagination 
* parameters (`page_size = 5`) uniformly across all task and subtask resource pools.

Release v0.2.2
### 🔍 Request Query Parameters, Date Component Extraction & Pagination

This release enhances the existing API endpoints by introducing advanced querying, performance-optimized filtering, and 
data pagination mechanics:

* **SubTask Pagination:** Integrated `PageNumberPagination` to split the subtask data layer, restricting payload 
* responses to a maximum of **5 objects per page**.
* **Strict Chronological Ordering:** Enforced descending database-level sorting (`-created_at`) across subtask listings,
* ensuring the newest items always appear first.
* **Database Date Components:** Implemented precise task filtering by days of the week by utilizing Django's structural 
* `ExtractWeekDay` method inside an analytical annotated aggregation layer.
* **Combined Query Parameter Filtering:** Developed chained filtering pipelines (logical `AND`) for subtasks, supporting 
* case-insensitive partial parent title matches (`task__title__icontains`) and exact status filters simultaneously.
* **Code Optimization:** Conducted a comprehensive code cleanup by removing redundant, non-optimized endpoint view 
* mappings and reducing database round-trips.

Release v0.2.1
### 🛠️ Advanced Serializers, Validation & SubTask APIViews

This release expands the REST API layer by adopting object-oriented Class-Based Views, complex business logic validation, 
and deep serialization mapping:

* **SubTask API (Class-Based Views):** Implemented clean, robust CRUD endpoints for subtasks management (`GET` / `POST` 
* under `/api/v1/subtasks/` and `GET` / `PUT` / `DELETE` under `/api/v1/subtasks/<id>/`) using DRF's `APIView`.
* **Nested Serializer Relations:** Upgraded task lookups so that fetching detailed task data dynamically includes all 
* associated subtasks via a nested `subtask_set` configuration.
* **Strict Business Validation:** Added an automated timezone-aware validation hook to reject past deadlines during task 
* creation, and overrode `create`/`update` layers for categories to manually enforce name uniqueness.
* **Data Integrity:** Explicitly isolated core auto-generated fields (such as `created_at`) as `read_only` across 
* serialization entry points to protect timestamps from manual manipulation.

Release v0.2.0
### 🚀 Core REST API Implementation (v1)

The system now includes a fully functional REST API built with Django REST Framework, featuring proper API versioning 
and secure validation:

* **API Versioning:** All endpoints are strictly versioned and exposed under the `/api/v1/` prefix for maximum 
* compatibility.
* **Task Management Endpoints:** Added secure endpoints for task creation (`POST /api/v1/tasks/create/`) with type 
* validation, fetching all tasks (`GET /api/v1/tasks/`), and retrieving a specific task by ID (`GET /api/v1/tasks/<id>/`) 
* with safe `404 Not Found` error handling.
* **Dynamic Analytics:** Integrated a dedicated aggregation endpoint (`GET /api/v1/tasks/statistics/`) that computes 
* total task counts, breakdown analysis based on model statuses, and real-time overdue metrics using Django's timezone 
* engine.
* **Architecture:** Implemented structured ModelSerializers and decoupled URL routing to separate API concerns from the 
* core Django views.

Release v0.1.1
### 📋 Task & Subtask Management (Admin Panel)

The system includes a customized Django Admin interface tailored for efficient task tracking:

* **Inline Subtask Editing:** Subtasks can be created, updated, or removed directly from the parent Task's editing form 
* without switching pages.
* **Smart Text Truncation:** To keep the Task dashboard clean, task names in the main list view are automatically 
* truncated to 10 characters if they exceed that limit. Full names are strictly preserved in dropdowns and selection 
* menus to avoid ambiguity.
* **Bulk Operations:** Administrators can update multiple subtasks simultaneously. Use the **\"Actions\"** dropdown in 
* the Subtasks list view to instantly mark all selected items as **Done**.

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
pip install django-filter
pip install djangorestframework djangorestframework-simplejwt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
