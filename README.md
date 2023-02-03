# studentManagementSystem
Project for Python and SQL

1. Urls

Used for routing. Specifies which python code to run for each url.

2. Views/StudentViews/TeacherViews

Contains most of the logic. Receives the request, uses models, populates context parameter(later used in template) and returns the template.

3. Models

Defines object. Also used for creating the database in code-first approach. (see migrations file for table creation/alteration operations)

4. Templates

Html codes for UI

