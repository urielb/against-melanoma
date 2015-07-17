# -*- coding: utf-8 -*-

from django import template
from django.template import resolve_variable, NodeList
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.middleware.csrf import get_token

register = template.Library()

@register.tag()
def notifications_as_table(parser, token):
    return NotificationsTableNode()
    
class NotificationsTableNode(template.Node):
    def __init__(self):
        pass
    def render(self, context):
        user = resolve_variable('user', context)
        script = u"""<script type='text/javascript'> $(function () {
        $(".hide_notification").live('click', function(e) {
            $(e.currentTarget).parent().parent().remove();
            submit_hide_notification($(e.currentTarget).parent().parent().attr('id'));
            if ($("#notifications tr").length == 1)
                $("#notifications").append("<tr><td colspan='3' class='alert-success'>Sem novas notificações</td></tr>")
        });
        
        var submit_hide_notification = function (id) {
            data = {
                'notification_id': id,
                'csrfmiddlewaretoken': '%s'
            }
            $.post("%s", data).success(function (data) {
                //alert(data.message)
           }).error(function (xhr, status, error) {
               data = xhr.responseText
               data = $.parseJSON(data)
               //4alert(data.message)
           });;
        }
        })</script>""" % (context['csrf_token'], reverse('hide_notification'))
        table = """<table id='notifications' class='table table-striped'><tr><th>Mensagem</th><th>Data</th><th>Ocultar</th></tr>%s</table>%s""" % ("%s", script)
        
        trs = ""
        tr = "<tr id='%s' class='%s'><td>%s</td><td>%s</td><td><a class='hide_notification pointer'>Ocultar</a></td></tr>"
        
        if len(user.notifications.filter(hidden=False)) > 0:
            for i in user.notifications.filter(hidden=False).order_by("-id"):
                trs += tr % (i.id, i.style, i.message, i.datetime)
        else:
            trs += u"<tr><td colspan='3' class='alert-success'>Sem novas notificações</td></tr>"
            
        
        return table % trs
        
@register.tag()
def notifications_as_div(parser, token):
    try:
        tag, style = token.split_contents()
        return NotificationsDivNode(style.replace("\"", ""))
    except ValueError:
        return NotificationsDivNode()
        
class NotificationsDivNode(template.Node):
    def __init__(self):
        self.style = ""
    def __init__(self, style):
        self.style = style
        
    def render(self, context):
        user = resolve_variable('user', context)
        html = "<div class='%s'><h4>Avisos</h4>%s</div>" % (self.style, "%s")
        
        ps = ""
        p = "<p class='%s'>%s (%s)</p>"
        
        if len(user.notifications.filter(hidden=False)) > 0:
            for i in user.notifications.filter(hidden=False).order_by("-id"):
                ps += p % (i.style, i.message, i.datetime)
        else:
            ps += "<div class='alert alert-success'>%s</div>" % _(u"Sem novas notificações").__unicode__()
        
        return html % ps
