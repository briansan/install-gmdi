#
# @file   gmdi.py
# @author Brian Kim
# @brief  a module that contains methods to access
#         the Google Material Design Icons
#

import pygtk
pygtk.require('2.0')
import gtk, os

def ls_categories():
  return os.listdir('/var/icons')

def ls_icons(cat):
  # check to see if cat is valid
  cats = ls_categories()
  if cat not in cats:
    print 'gmdi: ls_ic: error: invalid category'
    return None
  # get all the icons
  icons = os.listdir('/var/icons/'+cat)
  # dedupe
  y = []
  for icon in icons:
    # get rid of file ext and the leading 'ic'
    icon = icon.split('.')[0].split('_')[1:]
    n = len(icon)
    # grab everything but the last two words
    icon = '_'.join(icon[0:n-2])
    y.append(icon)
  return list(set(y))

def grep_icons(cat,s):
  # get icons
  icons = ls_icons(cat)
  # rval
  y = []
  for icon in icons:
    if s in icon:
      y.append(icon)
  return y

def mk_icon_path(ic,color,sz):
  # check ic
  ic = ic.split('/')
  if not (len(ic) == 2):
    print 'gmdi: get_ic: error: ic arg format "<cat>/<ic>"'
    return None
  # check color
  colors = ['white','black']
  if color not in colors:
    print 'gmdi: get_ic: error: color must be one of ' + str(colors)
    return None
  # check size
  sizes = [18, 24, 36, 48]
  if sz not in sizes:
    print 'gmdi: get_ic: error: size must be one of ' + str(sizes)
    return None
  return '/var/icons/'+ ic[0] + '/' + '_'.join(['ic',ic[1],color,str(sz)+'dp']) + '.png'

def mk_icon(ic,color='white',sz=36):
  # get the path
  y = gtk.Image()
  y.set_from_pixbuf( mk_icon_pixbuf(ic,color,sz) )
  return y

def mk_icon_pixbuf(ic,color='white',sz=36):
  # get the path
  try:
    path = mk_icon_path(ic,color,sz)
    y = gtk.gdk.pixbuf_new_from_file(path)
  except:
    print 'gmdi: mk_icon_pixbuf: path: '+path+' does not exist'
    return None
  return y

class GMDIPicker(gtk.VBox):

  def __init__( self ):
    #
    # model
    #

    # range = curr*256 <> curr*256+255
    # the current low end of the unicode table
    self.q = ''
    self.curr = 'action'
    self.groups = ls_categories()
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
    self.search.set_icon_from_pixbuf( 0, mk_icon_pixbuf( 'action/search', 'black' ) )
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
    model = ls_icons(self.curr)
    model.sort()
    # populate the list
    for icon in model:
      if len(self.q) > 0 and self.q not in icon:
        continue
      ic = mk_icon( '/'.join([self.curr,icon]), 'black', 18 )
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
