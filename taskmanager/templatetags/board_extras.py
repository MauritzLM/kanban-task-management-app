from django import template

register = template.Library()

def count_subtasks_completed(subtasks):
    return subtasks.filter(is_completed=True).count()

register.filter('count_subtasks_completed', count_subtasks_completed)

