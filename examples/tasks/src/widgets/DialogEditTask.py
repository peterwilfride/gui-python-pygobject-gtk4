# -*- coding: utf-8 -*-
"""Dialog delete task."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

Adw.init()


class DialogEditTask(Adw.MessageDialog):
    def __init__(self, adw_combo_row, pk, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = kwargs.get('transient_for')
        self.adw_combo_row = adw_combo_row
        self.pk = pk

        self.set_heading(heading='Edit task')
        self.set_body(body='Enter a new value')
        
        self.add_response(id='cancel', label=('_Cancel'))
        self.set_response_appearance(
            response='cancel',
            appearance=Adw.ResponseAppearance.DESTRUCTIVE
        )
        
        self.add_response(id='update', label=('_Update'))
        self.set_response_appearance(
            response='update',
            appearance=Adw.ResponseAppearance.SUGGESTED
        )
        self.connect('response', self.dialog_response)

        self.entry = Gtk.Entry.new()
        self.entry.set_text(text=adw_combo_row.get_subtitle())
        self.set_extra_child(child=self.entry)

    def get_entry_text(self):
        return self.entry.get_text()
    
    def dialog_response(self, dialog, response):
        if response == 'update':
            task = self.get_entry_text()
            self.mainwindow.database.update_task(pk=self.pk, task=task)
            self.adw_combo_row.set_subtitle(subtitle=task)
