# -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Gtk.ListBox() Adw.ComboRow()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):
    items = ['Item 01', 'Item 02', 'Item 03', 'Item 04', 'Item 05']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            title='Python e GTK 4: PyGObject Gtk.ListBox() Adw.ComboRow()'
        )
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

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        self.listbox = Gtk.ListBox.new()
        self.listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.listbox.get_style_context().add_class(class_name='boxed-list')
        vbox.append(child=self.listbox)

        model = Gtk.StringList.new(strings=self.items)

        for n in range(1, 5):
            icon = Gtk.Image.new_from_icon_name(
                icon_name='accessories-text-editor-symbolic'
            )

            adw_combo_row = Adw.ComboRow.new()
            adw_combo_row.set_title(title=f'Title {n}')
            adw_combo_row.set_subtitle(subtitle='Adw.ComboRow()')
            adw_combo_row.add_prefix(widget=icon)
            adw_combo_row.set_model(model=model)
            adw_combo_row.connect('notify::selected', self.on_adw_combo_row_selected)
            adw_combo_row.connect('notify::selected-item', self.on_adw_combo_row_selected_item)
            self.listbox.append(child=adw_combo_row)

    def on_adw_combo_row_selected(self, comborow, GParamUInt):
        print(f'Posição do item selecionado {comborow.get_selected()}')
        selected_item = comborow.get_selected_item()
        print(f'Texto do item selecionado {selected_item.get_string()}')

    def on_adw_combo_row_selected_item(self, comborow, GParamObject):
        print(f'Posição do item selecionado {comborow.get_selected()}')
        selected_item = comborow.get_selected_item()
        print(f'Texto do item selecionado {selected_item.get_string()}')


class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Ação app.preferences foi ativa.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
