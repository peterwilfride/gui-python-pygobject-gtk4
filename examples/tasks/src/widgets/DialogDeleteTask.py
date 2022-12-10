# -*- coding: utf-8 -*-
"""Dialog delete task."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw

Adw.init()


class DialogDeleteTask(Adw.MessageDialog):
    def __init__(self, adw_combo_row, pk, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = kwargs.get('transient_for')
        self.adw_combo_row = adw_combo_row
        self.pk = pk

        self.set_heading(heading='Delete task')
        self.set_body(body='Are you sure you want to remove the task?')
        self.add_response(id='cancel', label=('_Cancel'))
        self.add_response(id='delete', label=('_Delete'))
        self.set_response_appearance(
            response='delete',
            appearance=Adw.ResponseAppearance.DESTRUCTIVE
        )
        self.connect('response', self.dialog_response)

    def dialog_response(self, dialog, response):
        if response == 'delete':
            self.mainwindow.database.delete_task(pk=self.pk)
            self.mainwindow.list_box.remove(child=self.adw_combo_row)
