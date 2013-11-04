#!/usr/bin/env python


'''
zephyros API docs:
https://github.com/sdegutis/zephyros/blob/master/Docs/Python.md


TODO:
* make sure we can store unique window ids
* Proper showbox buffer
* Storing multiple groups


Features:
* Moded editing
  * Help Mode
* Commands
  * Add
  * Focus
  * Remove
  * List Windows
  * Save Layout

Data Model
---
groups
  group['name']
  group['windows']

buffer
  history
'''

import sys
sys.path.insert(0, '/Applications/_Utilities/Zephyros.app/Contents/Resources/libs/')
import zephyros


# Global Variables
active = 0
moded_bindings = ( 
                   ('ESCAPE', [], 'exit_active'),
                   ('h', [], 'show_help'),
                   ('a', [], 'add_to_group'),
                   ('f', [], 'focus_group'),
                 )
# Ugly hack for finding nested functions
functions = None

# Temporary single group buffer
group = []


@zephyros.zephyros
def myscript():
  ### Helpers
  def _bind():
    global moded_binding
    global functions

    for b in moded_bindings:
      f = functions.get(b[2])
      zephyros.api.bind(b[0], b[1], f)


  def _unbind():
    global moded_bindings
    for b in moded_bindings:
      zephyros.api.unbind(b[0], b[1])


  ### MODED COMMANDS
  # ESCAPE
  def exit_active():
    zephyros.api.log('exit')
    active = 0
    zephyros.api.hide_box()
    _unbind()


  # h
  def show_help():
    zephyros.api.show_box('help, blah blah blah')

  # a
  def add_to_group():
    global group
    zephyros.api.show_box('added %s : %s' % (zephyros.api.focused_window().app().title(), zephyros.api.focused_window().title()))
    zephyros.api.log('%r' % zephyros.api.focused_window().app())
    # zephyros.api.log('%r' % zephyros.api.focused_window())
    # zephyros.api.log('%r' % zephyros.api.focused_window())
    group.append(zephyros.api.focused_window().id)

  # f
  def focus_group():
    # zephyros.api.log('%r' % zephyros.api.focused_window())

    for w in zephyros.api.all_windows():
      # Unminimize in Group
      if w.id in group:
        if w.minimized():
          w.un_minimize()

      # Minimize everything else
      else:
        w.minimize()




  ### GLOBAL COMMANDS
  def toggle_mode():
    global active
    if active:
      zephyros.api.log('toggling off...')
      active = 0
      zephyros.api.hide_box()
      _unbind()
    else:
      zephyros.api.log('toggling on...')
      zephyros.api.show_box('grouper\n\n(h for help)')
      active = 1
      _bind()
    # zephyros.api.log('test')
    # zephyros.api.log(zephyros.api.clipboard_contents())
    # zephyros.api.alert(zephyros.api.focused_window().title())

  ### DEBUG

  def window_id():
      win = zephyros.api.focused_window()
      zephyros.api.log('%r' % zephyros.api.focused_window().id)
      zephyros.api.log('%r' % zephyros.api.focused_window().id)
      zephyros.api.log('%r' % zephyros.api.focused_window().id)

  def test_trapping():
    zephyros.api.show_bot('test trapping h')
    zephyros.api.log('test trapping h')



  ### BINDING

  # ugly hack
  global functions
  functions = globals().copy()
  functions.update(locals())

  zephyros.api.bind('ESCAPE', ['Cmd'], toggle_mode)

  ### DEBUG
  # zephyros.api.bind('ESCAPE', ['Cmd'], window_id)
  # zephyros.api.bind('H', [], toggle_mode)
  # zephyros.api.bind('H', None, test_trapping)
  # zephyros.api.bind('F', ['Cmd', 'Shift'], nudge_window)
