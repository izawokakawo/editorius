import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class TextEditor:
    def __init__(self):
        self.window = Gtk.Window(title="Editorius v3.2.1_01")
        self.window.set_default_size(600, 400)
        self.window.connect("destroy", self.on_destroy)

        self.text_area = Gtk.TextView()
        self.text_area.set_wrap_mode(Gtk.WrapMode.WORD)
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.add(self.text_area)

        self.filename_entry = Gtk.Entry()
        self.filename_entry.set_sensitive(False)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(self.scrolled_window, True, True, 0)
        self.vbox.pack_start(self.filename_entry, False, False, 0)

        self.window.add(self.vbox)

        self.filename = None

        # Настройка горячих клавиш
        self.window.connect("key-press-event", self.on_key_press)

        self.window.show_all()

    def on_key_press(self, widget, event):
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if event.keyval == Gdk.KEY_o:
                self.open_file()
                return True
            elif event.keyval == Gdk.KEY_q:
                self.close_file()
                return True
            elif event.keyval == Gdk.KEY_s:
                self.save_file()
                return True
        return False

    def open_file(self):
        dialog = Gtk.FileChooserDialog("Open File", self.window, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            with open(self.filename, 'r') as file:
                buffer = self.text_area.get_buffer()
                buffer.set_text(file.read())
            self.filename_entry.set_sensitive(True)
            self.filename_entry.set_text(self.filename)
            self.filename_entry.set_sensitive(False)
        dialog.destroy()

    def close_file(self):
        buffer = self.text_area.get_buffer()
        if buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True).strip():
            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.QUESTION,
                                       Gtk.ButtonsType.YES_NO, "Сохранить изменения?")
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                self.save_file()
            dialog.destroy()
        Gtk.main_quit()

    def save_file(self):
        if self.filename:
            with open(self.filename, 'w') as file:
                buffer = self.text_area.get_buffer()
                file.write(buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True))
        else:
            dialog = Gtk.FileChooserDialog("Save File", self.window, Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.filename = dialog.get_filename()
                with open(self.filename, 'w') as file:
                    buffer = self.text_area.get_buffer()
                    file.write(buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True))
                self.filename_entry.set_sensitive(True)
                self.filename_entry.set_text(self.filename)
                self.filename_entry.set_sensitive(False)
            dialog.destroy()

    def on_destroy(self, widget):
        self.close_file()

if __name__ == "__main__":
    editor = TextEditor()
    Gtk.main()
