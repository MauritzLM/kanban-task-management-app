# Frontend Mentor - Kanban task management web app solution

This is a solution to the [Kanban task management web app challenge on Frontend Mentor](https://www.frontendmentor.io/challenges/kanban-task-management-web-app-wgQLt-HlbB). Frontend Mentor challenges help you improve your coding skills by building realistic projects. 

## Table of contents

- [Overview](#overview)
  - [The challenge](#the-challenge)
  - [Screenshot](#screenshot)
  - [Links](#links)
- [My process](#my-process)
  - [Built with](#built-with)
  - [Architecture](#Architecture)
  - [Continued development](#continued-development)
  - [Useful resources](#useful-resources)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

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

    2. login 

    3. logout

#### Forms
    
    1. Board form

    2. Delete board form

    3. Column form

    4. Task form 
    
    5. Delete task form

    6. Task view form

    7. Subtask form

  ##### Formsets

    1. Column

    2. Subtask 

    3. Task view

#### Templates

    1. components

    2. forms (add modals functionality)




forms - django has different types of forms you can use: form class, models forms, formsets
views - class views, function views
testing - unit tests
sqlite - development
db queries and speed

setting up venv

also doing cs50 python

It took me a while to understand django forms and getting it to work with the projects' design. I did make some small changes with the form functionality with the column and subtask fields / forms. And the way one deletes them to make it work. Also added a save changes button to the task view form. 

htmx - how to send requests / vs using regular form requests   
     - what to do on form success (include js code)

things i added:
 - authentication
 - loading spinner

looking to add:
 - notifications when updating/creating , deleting 
 - drag and drop 


```html
<h1>Some HTML code I'm proud of</h1>
```
```css
.proud-of-this-css {
  color: papayawhip;
}
```
```js
const proudOfThisFunc = () => {
  console.log('🎉')
}
```



### Continued development

Use this section to outline areas that you want to continue focusing on in future projects. These could be concepts you're still not completely comfortable with or techniques you found useful that you want to refine and perfect.

- django rest framework
- db queries
- 

**Note: Delete this note and the content within this section and replace with your own plans for continued development.**

### Useful resources

- [Example resource 1](https://www.example.com) - This helped me for XYZ reason. I really liked this pattern and will use it going forward.
- [Example resource 2](https://www.example.com) - This is an amazing article which helped me finally understand XYZ. I'd recommend it to anyone still learning this concept.

- formset validation - empty forms added dynamically must not validate 
https://stackoverflow.com/questions/4481366/django-and-empty-formset-are-valid

- 2 htmx / django videos
- MDN Tutorial
- django docs

**Note: Delete this note and replace the list above with resources that helped you during the challenge. These could come in handy for anyone viewing your solution or for yourself when you look back on this project in the future.**

## Author

- Website - [Add your name here](https://www.your-site.com)
- Frontend Mentor - [@yourusername](https://www.frontendmentor.io/profile/yourusername)
- Twitter - [@yourusername](https://www.twitter.com/yourusername)

**Note: Delete this note and add/remove/edit lines above based on what links you'd like to share.**

## Acknowledgments

This is where you can give a hat tip to anyone who helped you out on this project. Perhaps you worked in a team or got some inspiration from someone else's solution. This is the perfect place to give them some credit.

**Note: Delete this note and edit this section's content as necessary. If you completed this challenge by yourself, feel free to delete this section entirely.**

