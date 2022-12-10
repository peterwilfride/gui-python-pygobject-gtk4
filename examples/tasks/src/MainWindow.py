# -*- coding: utf-8 -*-
"""Python e GTK 4: Applications main window."""

import gi

from widgets.DialogAddTask import DialogAddTask
from widgets.DialogDeleteTask import DialogDeleteTask
from widgets.DialogEditTask import DialogEditTask

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

# Adw.init()


class MainWindow(Gtk.ApplicationWindow):
    MODEL = Gtk.StringList.new(strings=['ToDo', 'Complete'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database = kwargs['application'].database

        self.set_title(title='Tasks')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        button_add_task = Gtk.Button.new()
        button_add_task.set_icon_name(icon_name='list-add-symbolic')
        button_add_task.connect('clicked', self.on_button_add_task_clicked)
        headerbar.pack_start(child=button_add_task)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        self.list_box = Gtk.ListBox.new()
        self.list_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.list_box.get_style_context().add_class(class_name='boxed-list')
        vbox.append(child=self.list_box)

        for task in self.database.read_tasks():
            task_row = Adw.ComboRow.new()
            task_row.set_title(title=f'Task ID {task[0]}')
            task_row.set_subtitle(subtitle=task[1])
            task_row.set_model(model=self.MODEL)
            task_row.connect(
                'notify::selected',
                self.on_adw_combo_row_selected,
                task[0],
            )

            status_complete = task[2]
            if status_complete:
                task_row.get_style_context().add_class(class_name='success')
                task_row.set_selected(position=status_complete)

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
                self.on_button_edit_task_clicked,
                task_row,
                task[0]
            )
            button_box_horizontal.append(child=button_edit_task)

            button_delete_task = Gtk.Button.new_with_label(label='Deletar')
            button_delete_task.set_icon_name(icon_name='user-trash-symbolic')
            button_delete_task.set_valign(align=Gtk.Align.CENTER)
            button_delete_task.connect(
                'clicked',
                self.on_button_delete_task_clicked,
                task_row,
                task[0]
            )
            button_box_horizontal.append(child=button_delete_task)

            self.list_box.append(child=task_row)

    def on_button_add_task_clicked(self, button):
        dialog = DialogAddTask(transient_for=self)
        dialog.present()

    def on_button_edit_task_clicked(self, button, task_row, pk):
        dialog = DialogEditTask(
            task_row, pk, transient_for=self)
        dialog.present()

    def on_button_delete_task_clicked(self, button, task_row, pk):
        dialog = DialogDeleteTask(task_row, pk, transient_for=self)
        dialog.present()

    def on_adw_combo_row_selected(self, task_row, GParamUInt, pk):
        status = task_row.get_selected()
        if status:
            self.database.update_task_status(pk, status=status)
            task_row.get_style_context().add_class(class_name='success')
        else:
            self.database.update_task_status(pk, status=status)
            task_row.get_style_context().remove_class(class_name='success')
