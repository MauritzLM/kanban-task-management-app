from django.utils.safestring import mark_safe

# Helper to build the needed formset
def build_new_formset(formset, new_total_formsets):
    html = ""

    for form in formset.empty_form:
        html += form.label_tag().replace('__prefix__', str(new_total_formsets))
        html += str(form).replace('__prefix__', str(new_total_formsets))
    
    return mark_safe(html)