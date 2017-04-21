#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#   Christofer Roibal - ChristoferR <christoferjam@gmail.com>
#   Sugarlabs - CeibalJAM! - Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import sys
import pango
import math

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toolbarbox import ToolbarBox

from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.activity import activity

from gettext import gettext as _

class DrawAreaExample(activity.Activity):

    color = gtk.gdk.color_parse("skyblue")

    def __init__(self, handle):
	activity.Activity.__init__(self, handle)

	toolbar_box = ToolbarBox()

	activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

	separator = gtk.SeparatorToolItem()
	separator.props.draw = False
	separator.set_expand(True)
	toolbar_box.toolbar.insert(separator, -1)
	separator.show()

	change_color_button = ToolButton('toolbar-colors')
	change_color_button.set_tooltip(_('Click here to change the background color'))
	change_color_button.connect('clicked', self.on_change_color_clicked)
	toolbar_box.toolbar.insert(change_color_button, -1)
	change_color_button.show()

	separator = gtk.SeparatorToolItem()
	separator.props.draw = False
	separator.set_expand(True)
	toolbar_box.toolbar.insert(separator, -1)
	separator.show()

	stop_button = StopButton(self)
	stop_button.props.accelerator = '<Ctrl><Shift>Q'
	toolbar_box.toolbar.insert(stop_button, -1)
	stop_button.show()


	button = gtk.Button("Click here to change the background color")
	button.connect('clicked', self.on_change_color_clicked)
	button.set_flags(gtk.CAN_DEFAULT)
	button.grab_default()
	toolbar_box.add(button)
	button.show()

	self.set_toolbar_box(toolbar_box)
	toolbar_box.show()

	canvas = gtk.HBox(False, 0)

	color = gtk.gdk.color_parse("skyblue")

	self.d_area = gtk.DrawingArea()
	self.d_area.connect("expose-event", self.expose)
	self.d_area.modify_bg(gtk.STATE_NORMAL, color)
	

	canvas.add(self.d_area)    
	
	self.set_canvas(canvas)
	self.show_all()

    def expose(self, widget, event):
	self.context = widget.window.cairo_create()

	self.context.rectangle(event.area.x, event.area.y,
		event.area.width, event.area.height)
	self.context.clip()

	self.draw(self.context, event)
	self.queue_draw()
	return False
 
    def draw(self, context, event ):
	rect = self.get_allocation()
	x = rect.x + rect.width / 2
	y = rect.y + rect.height / 2

	radius = min(rect.width / 3, rect.height / 3) - 5

	self.context.arc(x, y, radius, 0  , 2 * math.pi)
	a ,b = self.get_pointer()   
	r2 = a*a + b*b 
	self.context.set_source_rgb(.1 + 100.0 /(a  + .1), .1 + 100.0 /(b + .1) , .1 + 100 /(r2 + .1))
	self.context.fill()

	self.context.set_source

    def expose2(self, widget, event):

	cr = widget.window.cairo_create()

	cr.set_line_width(9)
	cr.set_source_rgb(0.7, 0.2, 0.0)

	w = self.allocation.width
	h = self.allocation.height

	cr.translate(w/2, h/2)
	cr.arc(0, 0, 50, 0, 2*math.pi)
	cr.stroke_preserve()

	cr.set_source_rgb(0.3, 0.4, 0.6)
	cr.fill()

    def on_change_color_clicked(self, button):

	dialog = gtk.ColorSelectionDialog("Changing color")
	dialog.set_transient_for(self)
	colorsel = dialog.colorsel

	colorsel.set_previous_color(self.color)
	colorsel.set_current_color(self.color)
	colorsel.set_has_palette(True)

	response = dialog.run()

	if response == gtk.RESPONSE_OK:
	    self.color = colorsel.get_current_color()
	    self.d_area.modify_bg(gtk.STATE_NORMAL, self.color)

	dialog.destroy()
	return True
