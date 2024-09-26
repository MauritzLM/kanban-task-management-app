# Frontend Mentor - Kanban task management web app solution

This is a solution to the [Kanban task management web app challenge on Frontend Mentor](https://www.frontendmentor.io/challenges/kanban-task-management-web-app-wgQLt-HlbB). Frontend Mentor challenges help you improve your coding skills by building realistic projects. 

## Table of contents

- [Overview](#overview)
  - [The challenge](#the-challenge)
  - [Links](#links)
- [My process](#my-process)
  - [Built with](#built-with)
  - [Architecture](#Architecture)
  - [Continued development](#continued-development)
  - [Useful resources](#useful-resources)
- [Author](#author)

## Overview

### The challenge

Users should be able to:

- View the optimal layout for the app depending on their device's screen size
- See hover states for all interactive elements on the page
- Create, read, update, and delete boards and tasks
- Receive form validations when trying to create/edit boards and tasks
- Mark subtasks as complete and move tasks between columns
- Hide/show the board sidebar
- Toggle the theme between light/dark modes
- **Bonus**: Allow users to drag and drop tasks to change their status and re-order them in a column
- **Bonus**: Keep track of any changes, even after refreshing the browser (`localStorage` could be used for this if you're not building out a full-stack app)
- **Bonus**: Build this project as a full-stack application


### Links

- Solution URL: [Add solution URL here]()
- Live Site URL: [Add live site URL here](https://web-production-b1cb.up.railway.app/taskmanager/)

## My process

### Built with

- Semantic HTML5 markup
- SASS
- Flexbox
- CSS Grid
- Mobile-first workflow
- [Django](https://www.djangoproject.com/) - Python framework
- [HTMX](https://htmx.org/) - Library to access modern browser features
- [Hyperscript](https://hyperscript.org/) - Front-end scripting language
- [Postgresql](https://www.postgresql.org/) - Relational database

### Architecture

#### Models

1. Board 
   - Related to Django User model with foreign key
   - Custom save method to return saved object

2. Column
   - Related to Board model with foreign key

3. Task
   - Related to Column with foreign key
   - Custom save method to return saved object

4. Subtask 
   - Related to Task with foreign key

#### Views

1. index
   - Finds user boards from db if user logged in
   - Renders base template

2. get_sidebar
   - Finds user boards from db if user logged in
   - Renders sidebar component
   
##### Requires login

3. board_detail
   - Finds user's board using id in url and all columns of the board
   - Renders board_detail template

4. board_form
   - On get request creates board form and empty column formset
   - On post request, validates forms
   - If forms are valid, it saves a new board then uses that board's id when saving columns. Then returns a 204 HTTP response.
   - Renders board_form component

5. edit_board
   - Finds board using url id
   - Creates a board form using returned board
   - If forms are valid, it saves the board and updates or deletes (if marked for deletion) columns. Then returns a 204 HTTP response
   - Renders edit_board_form component

6. column_form
   - Adds a form to the column formset
   - Builds a new formset using current_total_formsets from url and build_new_formset helper function
   - Passes new_formset and new_total_formsets in context
   - Renders column_form component

7. delete_board and delete_task
   - Finds object to delete and creates delete form
   - If form is valid, deletes object and redirects to index

8. new_task
   - Finds board from id in url
   - On get request creates task form and empty subtask formset
   - On post request, validates forms
   - Changes the column queryset of the task_form to contain only columns from the current board
   - If forms are valid, it saves a new task then uses that task's id when saving subtasks. Then returns a 204 HTTP response.
   - Renders task_form component

9. edit_task
   - Finds task and board from id and t_id in url           
   - Creates a task form using returned task
   - Changes the column queryset of the task_form to contain only columns from the current board
   - If forms are valid, it saves the task and updates or deletes (if marked for deletion) subtasks. Then returns a 204 HTTP response
   - Renders edit_task_form component

10. task_view
   - Finds task and board from id and t_id in url
   - On get request, creates task form using returned task. Creates taskview formset (as subtask_formset) filtering by returned task and ordering by is_completed (completed items are first).
   - Changes the column queryset of the task_form to contain only columns from the current board
   - On post request, forms are validated and any column changes and subtask is_completed changes are saved. Then returns a 204 HTTP response     
   - Renders task_view component

11. subtask_form
   - Adds a form to the subtask formset
   - Builds a new formset using current_total_formsets from url and build_new_formset helper function
   - Passes new_formset and new_total_formsets in context
   - Renders subtask_form component

#### Auth Views

1. signup
   - Uses UserCreationForm from django
   - Logs user in if form is valid

2. login
   - Uses custom login form 

3. logout
   - Logs user out when submitted

#### Forms
    
1. Board form
   - Model form
   - Only includes name field with placeholder widget and custom error message
   
2. Board and Task delete forms
   - Model forms with no fields
      
3. Column form
   - Model form
   - Only includes col_name field with empty label, placeholder widget and custom error message

4. Task form 
   - Model form
   - Includes title, description and column fields
   - Custom label for column - 'Status'
   - Placeholder widget for title and description
   - Custom error messages for title and column
    
5. Task view form
   - Model form
   - Only includes column field with 'Status' label

6. Subtask form
   - Model Form
   - Only includes sub_name field with placeholder widget and custom error message

##### Formsets

1. Column formset
   - Uses modelformsetfactory and column form
   - No extra forms
   - Can delete set to true

2. Subtask formset
   - Uses modelformsetfactory and subtask form
   - No extra forms
   - Can delete set to true
   - Placeholder widget for sub_name
       
3. Task view formset
   - Uses modelformsetfactory and subtask model
   - Excludes task field
   - No extra forms
   - Read only widget on sub_name

#### Templates

1. Components
   - The sidebar-wrapper in the base template makes a request to the sidebar url when the page loads

2. Forms
   - Htmx swaps the requested form into the form wrapper in the base.html template
   - Forms are rendered manually as needed
   - The add subtask/column button appends a new form to the formset, this button is disabled when there are 5 forms
   - Forms make htmx post requests otherwise the modal won't work correctly
   - When a form is submitted successfully it either redirects to a url or reloads the currect location:

   ```js
   document.addEventListener('htmx:beforeSwap', (e) => {
    if (e.detail.target.id == 'form-wrapper' && !e.detail.xhr.response) {
        location.reload()
    }
   });
   ```
3. Template tags
   - Custom template tag to get the number of subtasks completed   

### Continued development

- Django rest framework
- Learn more about doing effective and efficient db queries

### Useful resources / Acknowledgments

- [Django and htmx example 1](https://www.youtube.com/watch?v=3dyQigrEj8A&list=LL&index=17) - Great video tutorial and a blog that got me started 
- [Django and htmx example 2](https://www.youtube.com/watch?v=L1VC-KpSoBk&list=LL&index=16) - Another great video tutorial that helped me understand I have to send htmx post requests in my forms.
- [Dynamic formsets](https://stackoverflow.com/questions/74757197/the-right-way-to-dynamically-add-django-formset-instances-and-post-usign-htmx) - Very helpful post with answers about how to add formsets dynamically.
- [formset validation](https://stackoverflow.com/questions/4481366/django-and-empty-formset-are-valid) - Formset validation - empty forms added dynamically must not validate
- [MDN Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) - Building a library application using django from start to finish. I used this as a reference throughout the project.
- [Django documentation](https://www.djangoproject.com/) - Official documentation

## Author

- Frontend Mentor - [MauritLM](https://www.frontendmentor.io/profile/MauritLM)