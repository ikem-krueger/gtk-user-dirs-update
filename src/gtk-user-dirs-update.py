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
		self.window.show()

		self.entry_desktop = builder.get_object("entry_desktop")
		self.entry_desktop.connect("button-press-event", self.select_button_xdg_dir, self.entry_desktop, "DESKTOP")

		self.entry_documents = builder.get_object("entry_documents")
		self.entry_documents.connect("button-press-event", self.select_button_xdg_dir, self.entry_documents, "DOCUMENTS")

		self.entry_download = builder.get_object("entry_download")
		self.entry_download.connect("button-press-event", self.select_button_xdg_dir, self.entry_download, "DOWNLOAD")

		self.entry_music = builder.get_object("entry_music")
		self.entry_music.connect("button-press-event", self.select_button_xdg_dir, self.entry_music, "MUSIC")

		self.entry_pictures = builder.get_object("entry_pictures")
		self.entry_pictures.connect("button-press-event", self.select_button_xdg_dir, self.entry_pictures, "PICTURES")

		self.entry_publicshare = builder.get_object("entry_publicshare")
		self.entry_publicshare.connect("button-press-event", self.select_button_xdg_dir, self.entry_publicshare, "PUBLICSHARE")

		self.entry_templates = builder.get_object("entry_templates")
		self.entry_templates.connect("button-press-event", self.select_button_xdg_dir, self.entry_templates, "TEMPLATES")

		self.entry_videos = builder.get_object("entry_videos")
		self.entry_videos.connect("button-press-event", self.select_button_xdg_dir, self.entry_videos, "VIDEOS")

		self.button_reset = builder.get_object("button_reset")
		self.button_reset.connect("clicked", self.reset_xdg_dirs)

		#self.button_apply = builder.get_object("button_apply")
		#self.button_apply.connect("clicked", self.apply)

		self.update_entries()

	def update_entries(self):
		self.entry_desktop.set_text(self.find_xdg_dir("DESKTOP"))
		self.entry_documents.set_text(self.find_xdg_dir("DOCUMENTS"))
		self.entry_download.set_text(self.find_xdg_dir("DOWNLOAD"))
		self.entry_music.set_text(self.find_xdg_dir("MUSIC"))
		self.entry_pictures.set_text(self.find_xdg_dir("PICTURES"))
		self.entry_publicshare.set_text(self.find_xdg_dir("PUBLICSHARE"))
		self.entry_templates.set_text(self.find_xdg_dir("TEMPLATES"))
		self.entry_videos.set_text(self.find_xdg_dir("VIDEOS"))

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

