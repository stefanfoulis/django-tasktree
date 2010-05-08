from django.db import models
from django.db.models import Q
from django.db.models import F
from django.db.models.signals import post_delete, pre_delete, pre_save, post_save
from treebeard.mp_tree import MP_Node

class Task(MP_Node):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', null=True, blank=True)
    
    effort_estimate = models.IntegerField('estimate [min]', null=True, blank=True)
    effort_estimate_sum_of_descendants_calculated = models.IntegerField('sum [min]', default=0)
    effort_estimate_calculated = models.IntegerField('estimate calculated [min]', default=0)
    
    effort_spent = models.IntegerField('time spent [min]', null=True, blank=True)
    
    @property
    def percent_done(self):
        if self.effort_estimate and self.effort_spent:
            return float(self.effort_spent) / float(self.effort_estimate)
        else:
            return None
    
    def __unicode__(self):
        return u"%s" % (self.name,)
    class Meta:
        ordering = ['path']

def task_change_handler(sender, **kwargs):
    obj = kwargs.get('instance')
    try:
        current = Task.objects.get(id=obj.id)
        current_estimate = current.effort_estimate or 0
        current_sum = current.effort_estimate_sum_of_descendants_calculated or 0
        effort_estimate_calculated = current.effort_estimate_calculated or 0
    except Task.DoesNotExist:
        current_estimate = 0
        current_sum = 0
        effort_estimate_calculated = 0
        
    mytotal = obj.effort_estimate or 0
    mytotal += current_sum
    obj.effort_estimate_calculated = mytotal
    obj.effort_estimate_sum_of_descendants_calculated = current_sum
    mydiff = (obj.effort_estimate or 0)-current_estimate
    print "Task save diff:%s own:%s/%s sum:%s/%s total:%s/%s" % (mydiff,current_estimate,obj.effort_estimate, 
                                                            current_sum,obj.effort_estimate_sum_of_descendants_calculated, 
                                                            effort_estimate_calculated,obj.effort_estimate_calculated,)
    if not mydiff == 0:
        obj.get_ancestors().update(effort_estimate_calculated=F('effort_estimate_calculated')+mydiff,
                                    effort_estimate_sum_of_descendants_calculated=F('effort_estimate_sum_of_descendants_calculated')+mydiff)
pre_save.connect(task_change_handler, sender=Task)

def task_deleted_handler(sender, **kwargs):
    deleted_instance = kwargs.get('instance')
    print "task is being deleted %s (%s)" % (deleted_instance.id,deleted_instance.name,)
    # re-fetch the object becuase the data could be stale
    # we use effort estimate, because we don't care about the children... they will be deleted
    # individually
    diff = Task.objects.get(pk=deleted_instance.pk).effort_estimate or 0
    if diff:
        deleted_instance.get_ancestors().update(
            effort_estimate_calculated=F('effort_estimate_calculated')-diff,
            effort_estimate_sum_of_descendants_calculated=F('effort_estimate_sum_of_descendants_calculated')-diff
        )
    print "Task delete diff:%s" % (diff,)
pre_delete.connect(task_deleted_handler, sender=Task)

def testdata():
    roots = ['Superproject 1','Superproject 1']
    for r in roots:
        p = Task.add_root(name=r)
        for m in range(5):
            mt = p.add_child(name=u'Modul %s' % m)
            for t in range(6):
                tt = mt.add_child(name=u'Task %s' % t)
            
        
