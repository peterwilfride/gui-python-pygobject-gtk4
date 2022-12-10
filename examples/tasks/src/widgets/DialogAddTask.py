# -*- coding: utf-8 -*-
"""Dialog add task."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gtk

Adw.init()


class DialogAddTask(Adw.MessageDialog):
    last_row_id = int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mainwindow = kwargs.get('transient_for')
        self.database = self.mainwindow.database

        self.set_heading(heading='New task')
        self.set_body(body='Enter task name')

        self.add_response(id='cancel', label=('_Cancel'))
        self.set_response_appearance(
            response='cancel',
            appearance=Adw.ResponseAppearance.DESTRUCTIVE
        )

        self.add_response(id='add', label=('_Add'))
        self.set_response_appearance(
            response='add',
            appearance=Adw.ResponseAppearance.SUGGESTED
        )
        self.connect('response', self.dialog_response)

        self.entry = Gtk.Entry.new()
        self.set_extra_child(child=self.entry)

    def get_entry_text(self):
        return self.entry.get_text()

    def dialog_response(self, dialog, response):
        if response == 'add':
            self.database.create_task(self.entry.get_text())
            self.create_new_task_row()

    def create_new_task_row(self):
        pk = self.database.get_last_row_id()
        print(pk)

        task_row = Adw.ComboRow.new()
        task_row.set_title(
            title=f'Task ID {pk}'
        )
        task_row.set_subtitle(subtitle=self.get_entry_text())
        task_row.set_model(model=self.mainwindow.MODEL)
        task_row.connect(
            'notify::selected',
            self.mainwindow.on_adw_combo_row_selected,
            pk,
        )

        icon = Gtk.Image.new_from_icon_name(
            icon_name='accessories-text-editor-symbolic'
        )
        task_row.add_prefix(widget=icon)

        button_box_horizontal = Gtk.Box.new(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )
        button_box_horizontal.set_margin_start(margin=12)
        task_row.add_suffix(widget=button_box_horizontal)

        button_edit_task = Gtk.Button.new_with_label(label='Editar')
        button_edit_task.set_icon_name(icon_name='document-edit-symbolic')
        button_edit_task.set_valign(align=Gtk.Align.CENTER)
        button_edit_task.connect(
            'clicked',
            self.mainwindow.on_button_edit_task_clicked,
            task_row,
            pk
        )
        button_box_horizontal.append(child=button_edit_task)

        button_delete_task = Gtk.Button.new_with_label(label='Deletar')
        button_delete_task.set_icon_name(icon_name='user-trash-symbolic')
        button_delete_task.set_valign(align=Gtk.Align.CENTER)
        button_delete_task.connect(
            'clicked',
            self.mainwindow.on_button_delete_task_clicked,
            task_row,
            pk
        )
        button_box_horizontal.append(child=button_delete_task)

        self.mainwindow.list_box.append(child=task_row)
