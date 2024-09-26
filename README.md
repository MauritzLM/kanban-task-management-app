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
   - related to  Django User model with foreign key
   - custom save method to return saved object

2. Column
   - related to Board model with foreign key

3. Task
   - related to Column with foreign key
   - custom save method to return saved object

4. Subtask 
   - related to Task with foreign key

#### Views

1. index
   - finds user boards from db if user logged in
   - renders base template

2. get_sidebar
   - finds user boards from db if user logged in
   - renders sidebar component
   
##### Requires login

3. board_detail
   - login required
   - finds users' board using id in url and all columns of the board
   - renders board_detail template

4. board_form
   - on get request creates board form and empty column formset
   - on post request, validates forms
   - if forms are valid, it saves a new board then uses that board's id when saving columns. Then returns a 204 HTTP response.
   - renders board_form component

5. edit_board
   - finds board using url id
   - creates a board form using returned board
   - if forms are valid, it saves the board and updates or deletes (if marked for deletion) columns. Then returns a 204 HTTP response
   - renders edit_board_form component

6. column_form
   - adds a form to the column formset
   - builds a new formset using current_total_formsets from url and build_new_formset helper function
   - passes new_formset and new_total_formsets in context
   - renders column_form component

7. delete_board and delete_task
   - finds object to delete and creates delete form
   - if form is valid, deletes object and redirects to index

8. new_task
   - finds board from id in url
   - on get request creates task form and empty subtask formset
   - on post request, validates forms
   - changes the column queryset of the task_form to contain only columns from current board
   - if forms are valid, it saves a new task then uses that task's id when saving subtasks. Then returns a 204 HTTP response.
   - renders task_form component

9. edit_task
   - finds task and board from id and t_id in url           
   - creates a task form using returned task
   - changes the column queryset of the task_form to contain only columns from current board
   - if forms are valid, it saves the task and updates or deletes (if marked for deletion) subtasks. Then returns a 204 HTTP response
   - renders edit_task_form component

10. task_view
   - finds task and board from id and t_id in url
   - on get request, creates task form using returned task. Creates taskview formset (as subtask_formset) filtering by returned task and ordering by is_completed (completed items are first).
   - changes the column queryset of the task_form to contain only columns from current board
   - on post request, forms are validated and any column changes and subtask is_completed changes are saved. Then returns a 204 HTTP response     
   - renders task_view component

11. subtask_form
   - adds a form to the subtask formset
   - builds a new formset using current_total_formsets from url and build_new_formset helper function
   - passes new_formset and new_total_formsets in context
   - renders subtask_form component

#### Auth Views

1. signup
   - Uses UserCreationForm from django
   - logs user in on if form is valid

2. login
   - uses custom login form 

3. logout
   - logs user out when submitted

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
   - can delete set to true

2. Subtask formset
   - Uses modelformsetfactory and subtask form
   - No extra forms
   - can delete set to true
   - placeholder widget for sub_name
       
3. Task view formset
   - Uses modelformsetfactory and subtask model
   - Excludes task field
   - No extra forms
   - Read only widget on sub_name

#### Templates

1. components
   - the sidebar-wrapper in the base template makes a request to the sidebar url when the page loads

2. forms
   - Htmx swaps the requested form into the form wrapper in the base.html template
   - forms are rendered manually as needed
   - the add subtask/column button appends a new form to the formset, this button is disabled when there are 5 forms
   - forms make htmx post requests otherwise the modal won't work correctly
   - when a form is submitted successfully it either redirect to a url or reload the currect location:

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

- django rest framework
- learn more about doing effective and efficient db queries
- 

### Useful resources / Acknowledgments

- [Django and htmx example 1](https://www.youtube.com/watch?v=3dyQigrEj8A&list=LL&index=17) - Great video tutorial and a blog that got me started 
- [Django and htmx example 2](https://www.youtube.com/watch?v=L1VC-KpSoBk&list=LL&index=16) - Another great video tutorial that helped me understand I have to send htmx post requests in my forms.
- [Dynamic formsets](https://stackoverflow.com/questions/74757197/the-right-way-to-dynamically-add-django-formset-instances-and-post-usign-htmx) - Very helpful post with answers about how to add formsets dynamically.
- [formset validation](https://stackoverflow.com/questions/4481366/django-and-empty-formset-are-valid) - formset validation - empty forms added dynamically must not validate
- [MDN Django Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) - Building a library application using django from start to finish. I used this as a reference throughout the project.
- [Django documentation](https://www.djangoproject.com/) - Official documentation

## Author

- Frontend Mentor - [MauritLM](https://www.frontendmentor.io/profile/MauritLM)