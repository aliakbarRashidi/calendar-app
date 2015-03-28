/*
 * Copyright (C) 2012-2015 Canonical, Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 3.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.0
import Ubuntu.Components 1.1

Item {
   id: root

   property string iconSource
   property alias labelText: name.text
   property bool expandIcon: false
   property bool showContents: true

   signal clicked()

   anchors {
       left: parent.left
       right: parent.right
   }
   height: visible ? units.gu(8) : 0

   Rectangle {
       anchors.fill: parent
       color: Theme.palette.selected.background
       opacity: addNewCalendarButtonArea.pressed ?  1.0 : 0.0
   }

   UbuntuShape {
       id: uShape

       anchors {
           left: parent.left
           top: parent.top
           bottom: parent.bottom
           margins: units.gu(1)
       }
       width: height
       radius: "medium"
       color: Theme.palette.normal.overlay
       image: Image {
           source: root.expandIcon ? root.iconSource : ""
       }
       Image {
           anchors.centerIn: parent
           source: root.expandIcon ? "" : root.iconSource
           visible: !root.expandIcon
           width: units.gu(2)
           height: units.gu(2)
       }
       visible: root.showContents
   }

   Label {
       id: name

       anchors {
           left: uShape.right
           leftMargin: units.gu(2)
           verticalCenter: parent.verticalCenter
           right: parent.right
           rightMargin: units.gu(2)
       }
       color: UbuntuColors.lightAubergine
       elide: Text.ElideRight
       visible: root.showContents
   }

   MouseArea {
       id: addNewCalendarButtonArea

       anchors.fill: parent
       onClicked: root.clicked()
       visible: root.showContents
   }
}
