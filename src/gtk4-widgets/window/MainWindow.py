# -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Gtk.Window()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class NewWindow(Gtk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_modal(modal=True)
        self.set_title(title='Python e GTK 4: PyGObject Gtk.Window()')
        self.set_default_size(width=int(1366 / 3), height=int(768 / 3))
        self.set_size_request(width=int(1366 / 3), height=int(768 / 3))

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        vbox.set_valign(Gtk.Align.CENTER)
        self.set_child(child=vbox)

        # Widgets.
        button = Gtk.Button.new_with_label('Fechar janela')
        button.connect('clicked', self.on_window_button_close_clicked)
        vbox.append(child=button)

        self.show()

    def on_window_button_close_clicked(self, widget):
        self.destroy()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK 4: PyGObject Gtk.ApplicationWindow()')
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

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        vbox.set_valign(Gtk.Align.CENTER)
        self.set_child(child=vbox)

        # Widgets.
        button = Gtk.Button.new_with_label('Abrir janela')
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, widget):
        # window = Gtk.Window.new()
        # window.set_transient_for(parent=self)
        # window.set_modal(modal=True)
        # window.set_title(title='Python e GTK 4: PyGObject Gtk.Window()')
        # window.set_default_size(width=int(1366 / 3), height=int(768 / 3))
        # window.set_size_request(width=int(1366 / 3), height=int(768 / 3))
        # window.show()

        # Usando uma classe (recomendado).
        NewWindow(transient_for=self)


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
