# studentManagementSystem
Project for Python and SQL

0. manage.py

Django boiler-point for operations such as stating local server/db operations.

1. urls.py

Used for routing. Specifies which python code to run for each url.

2. Views/StudentViews/TeacherViews .py

Contains most of the logic. Receives the request, uses models, populates context parameter(later used in template) and returns the template.

3. Models

Defines objects. Also used for creating the database in code-first approach. (see migrations file for table creation/alteration operations)

4. Templates

Html codes for UI

