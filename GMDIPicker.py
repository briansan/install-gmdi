##
# @file UnicodePickerView

# @brief a view that allows a user to pick a unicode value
#

import pygtk
pygtk.require('2.0')
import gtk, gmdi

class GMDIPicker(gtk.VBox):

  def __init__( self ):
    #
    # model
    #
    
    # range = curr*256 <> curr*256+255
    # the current low end of the unicode table
    self.q = ''
    self.curr = 'action'
    self.groups = gmdi.ls_categories()
    self.groups.sort()
    self.combobox_model = gtk.ListStore(str)
    for x in self.groups:
      self.combobox_model.append([x])

    #
    # ui
    #

    # 
    # layout: combobox, table of unicode, control
    gtk.VBox.__init__( self )
   
    # top: selects a popular unicode range
    self.combobox = gtk.ComboBox()
    cell = gtk.CellRendererText()
    self.combobox.pack_start(cell)
    self.combobox.add_attribute(cell, 'text', 0)
    self.combobox.set_model( self.combobox_model )
    self.combobox.connect( 'changed', self.cb_changed )

    # middle: scroll window w list inside it
    self.scroll = gtk.ScrolledWindow()
    self.lv = gtk.List()
    
    self.scroll.add_with_viewport(self.lv)
 
    # bottom: search bar
    self.search = gtk.Entry()
    self.search.set_icon_from_pixbuf( 0, gmdi.mk_icon_pixbuf( 'action/search', 'black' ) )
    self.search.connect( 'activate', self.activate )

    # add components to vbox
    self.pack_start( self.combobox, False)
    self.pack_start( self.scroll, True)
    self.pack_start( self.search, False)
  
  def cb_changed( self, cb ):
    # get index
    i = cb.get_active()
    # get the curr
    self.curr = self.groups[i] if i > -1 else self.curr
    # update
    self.update()

  def activate( self, v ):
    self.q = self.search.get_text()
    self.update()

  def clear( self ):
    for child in self.lv.get_children():
      self.lv.remove(child)

  def start( self ):
    self.show_all()
    self.combobox.set_active(0)

  def update( self ):
    self.clear()
    # get the icons
    model = gmdi.ls_icons(self.curr)
    model.sort()
    # populate the list
    for icon in model:
      if len(self.q) > 0 and self.q not in icon:
        continue
      ic = gmdi.mk_icon( '/'.join([self.curr,icon]), 'black', 18 )
      label = gtk.Label(icon)
      hbox = gtk.HBox(False,10)
      hbox.pack_start(ic, False)
      hbox.pack_start(label, True)
      align = gtk.Alignment()
      align.set_padding(10,10,10,10)
      align.add(hbox)
      item = gtk.ListItem()
      item.add(align)
      self.lv.add( item )
    self.lv.show_all()
  
if __name__ == "__main__":
  w = gtk.Window()
  w.set_default_size( 320, 480 )
  w.add( GMDIPicker() )
  w.show_all()
  gtk.main()
