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
