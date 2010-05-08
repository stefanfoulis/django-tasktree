from django.contrib import admin
from treebeard.admin import TreeAdmin
from tasktree.models import Task

class TaskAdmin(TreeAdmin):
    list_display = ('indented_label','name','effort_estimate','effort_estimate_sum_of_descendants_calculated','effort_estimate_calculated','effort_spent','percent_done','pretty_percent_done','path','numchild','depth',)
    list_editable = ('name','effort_estimate','effort_spent',)
    change_list_template = 'admin/change_list.html'
    
    def indented_label(self, obj):
        return u"%s%s" % ((obj.depth-1)*4*"&nbsp;", obj.name)
    indented_label.allow_tags = True
    
    def pretty_percent_done(self, obj):
        if not obj.percent_done==None:
            if obj.percent_done > 1:
                return u'<div style="border: 1px solid gray;"><div style="background-color: red;width:100%%">&nbsp;%s%%</div></div>' % (int(obj.percent_done*100),)
            return u'<div style="border: 1px solid gray;"><div style="background-color: gray;width:%s%%">&nbsp;</div></div>' % (int(obj.percent_done*100),)
        else:
            return u'<div><div style="width:0%">&nbsp;</div></div>' 
    pretty_percent_done.allow_tags = True
admin.site.register(Task, TaskAdmin)