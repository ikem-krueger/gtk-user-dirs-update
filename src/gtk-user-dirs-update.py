#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess

class GtkUserDir(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("gtk-user-dirs-update.ui")

        self.window = builder.get_object("dialog1")
        self.window.set_title("Update User Directories")
        self.window.connect("destroy", self.quit)

        self.vbox1 = Gtk.Box()
        self.vbox1.set_orientation(Gtk.Orientation.VERTICAL)

        self.dialog_vbox1 = builder.get_object("dialog-vbox1")
        self.dialog_vbox1.pack_end(self.vbox1, True, True, 0)

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

            self.vbox1.pack_start(hbox, True, True, 0)

        self.button_reset = builder.get_object("button_reset")
        self.button_reset.connect("clicked", self.reset_xdg_dirs)

        #self.button_apply = builder.get_object("button_apply")
        #self.button_apply.connect("clicked", self.apply)

        self.window.show_all()

    def update_entries(self):
        print("TODO: implement update_entries()")

    def find_xdg_dir(self, name):
        return subprocess.check_output(['xdg-user-dir', name]).decode().rstrip('\n')

    def set_xdg_dir(self, name, path):
        # there need to be a check here..
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

    def reset_xdg_dirs(self, widget):
        subprocess.Popen(['xdg-user-dirs-update', '--force'])

        self.update_entries()

    def quit(self, *args):
        Gtk.main_quit()

if __name__ == "__main__":
    app = GtkUserDir()
    Gtk.main()

