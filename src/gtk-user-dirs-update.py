#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess

class Dialog(Gtk.Dialog):
    def __init__(self):
        Gtk.Dialog.__init__(self)

        self.set_title("Update User Directories")
        self.set_resizable(False)

        reset_button = self.add_button("gtk-revert-to-saved", Gtk.ResponseType.CANCEL)
        apply_button = self.add_button("gtk-apply", Gtk.ResponseType.OK)

        self.connect("response", self.on_response)

        icons = {
            "DESKTOP":"user-desktop",
            "DOCUMENTS":"folder-documents",
            "DOWNLOAD":"folder-download",
            "MUSIC":"folder-music",
            "PICTURES":"folder-pictures",
            "PUBLICSHARE":"folder-publicshare",
            "TEMPLATES":"folder-templates",
            "VIDEOS":"folder-videos"
        }

        self.vbox.set_spacing(4)

        for icon_name in sorted(icons.keys()):
            image = Gtk.Image()
            image.set_from_icon_name(icons[icon_name], Gtk.IconSize.LARGE_TOOLBAR)

            label = Gtk.Label()
            label.set_label(icon_name.capitalize() + ":")

            entry = Gtk.Entry()
            entry.set_text(self.find_xdg_dir(icon_name))
            entry.connect("button-press-event", self.select_button_xdg_dir, entry, icon_name)

            hbox = Gtk.Box()

            hbox.pack_start(image, False, True, 2)
            hbox.pack_start(label, False, True, 0)
            hbox.pack_start(entry, True, True, 6)

            self.vbox.add(hbox)

        self.set_focus(apply_button)
        self.show_all()

    def on_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.apply()
        elif response == Gtk.ResponseType.CANCEL:
            self.reset_xdg_dirs()
        else:
            self.quit()

    def apply(self):
        print("TODO: implement apply()")

    def update_entries(self):
        print("TODO: implement update_entries()")

    def find_xdg_dir(self, name):
        return subprocess.check_output(['xdg-user-dir', name]).decode().rstrip('\n')

    def set_xdg_dir(self, name, path):
        # TODO: there need to be a check here...
        subprocess.Popen(['xdg-user-dirs-update', '--set', name, path])

    def select_entry_xdg_dir(self, widget, entry, name):
        path = entry.get_text()

        self.set_xdg_dir(name, path)

    def select_button_xdg_dir(self, widget, other, entry, name):
        dialog = Gtk.FileChooserDialog("Select a directory", None,
                                        Gtk.FileChooserAction.SELECT_FOLDER, 
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.set_current_folder(entry.get_text())

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()

            self.set_xdg_dir(name, path)

            # update_entry
            entry.set_text(self.find_xdg_dir(name))

        dialog.destroy()

    def reset_xdg_dirs(self):
        subprocess.Popen(['xdg-user-dirs-update', '--force'])

        self.update_entries()

    def quit(self, *args):
        Gtk.main_quit()

if __name__ == "__main__":
    app = Dialog()
    Gtk.main()
