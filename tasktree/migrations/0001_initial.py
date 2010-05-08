# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Task'
        db.create_table('tasktree_task', (
            ('effort_estimate_sum_of_descendants_calculated', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('effort_spent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('effort_estimate_calculated', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('effort_estimate', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('tasktree', ['Task'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Task'
        db.delete_table('tasktree_task')
    
    
    models = {
        'tasktree.task': {
            'Meta': {'object_name': 'Task'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effort_estimate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'effort_estimate_calculated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'effort_estimate_sum_of_descendants_calculated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'effort_spent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }
    
    complete_apps = ['tasktree']
