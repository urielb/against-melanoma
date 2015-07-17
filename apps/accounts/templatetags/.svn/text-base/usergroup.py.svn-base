from django import template
from django.template import resolve_variable, NodeList
from django.contrib.auth.models import Group

register = template.Library()

@register.tag()
def ifispatient(parser, token):
    nodelist_true = parser.parse(('else', 'endifispatient'))
    token = parser.next_token()
    
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifispatient'))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    
    return UserCheckPermission("patient", nodelist_true, nodelist_false)
    
@register.tag()
def ifisdoctor(parser, token):
    nodelist_true = parser.parse(('else', 'endifisdoctor'))
    token = parser.next_token()
    
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifisdoctor'))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    
    return UserCheckPermission("doctor", nodelist_true, nodelist_false)
    
class UserCheckPermission(template.Node):
    def __init__(self, group, nodelist_true, nodelist_false):
        self.group = group
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        
    def render(self, context):
        user = resolve_variable('user', context)
        
        if not user.is_authenticated():
            return self.nodelist_false.render(context)
            
        try:
            group = self.group
            if group == "doctor" and user.is_doctor() is True:
                return self.nodelist_true.render(context)
            if group == "patient" and user.is_patient() is True:
                return self.nodelist_true.render(context)

        except Group.DoesNotExist:
            return self.nodelist_false.render(context)
            
        
        return self.nodelist_false.render(context)

@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific
    group. Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}, or
           {% ifusergroup Admins|Group1|Group2 %} ... {% endifusergroup %}, or
           {% ifusergroup Admins %} ... {% else %} ... {% endifusergroup %}

    """
    try:
        tag, group = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires 1 argument.")
    
    nodelist_true = parser.parse(('else', 'endifusergroup'))
    token = parser.next_token()
    
    if token.contents == 'else':
        nodelist_false = parser.parse(('endifusergroup',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    
    return GroupCheckNode(group, nodelist_true, nodelist_false)


class GroupCheckNode(template.Node):
    def __init__(self, group, nodelist_true, nodelist_false):
        self.group = group
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
    def render(self, context):
        user = resolve_variable('user', context)
        
        if not user.is_authenticated():
            return self.nodelist_false.render(context)
            
        try:
            for group in self.group.split("|"):
                
                if Group.objects.get(name=group) in user.groups.all():
                    return self.nodelist_true.render(context)

        except Group.DoesNotExist:
            return self.nodelist_false.render(context)
            
        
        return self.nodelist_false.render(context)
