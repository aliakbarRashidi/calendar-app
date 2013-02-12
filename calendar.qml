import QtQuick 2.0
import Ubuntu.Components 0.1

/*!
    \brief MainView with Tabs element.
           First Tab has a single Label and
           second Tab has a single ToolbarAction.
*/

MainView {
    // objectName for functional testing purposes (autopilot-qt5)
    objectName: "calendar"
    
    width: units.gu(50)
    height: units.gu(75)
    
    Tabs {
        id: tabs
        anchors.fill: parent
        
        // First tab begins here
        Tab {
            objectName: "Tab1"
            
            title: i18n.tr("Calendar")
            
            // Tab content begins here
            page: Page {
                Column {
                    anchors.centerIn: parent
                    Label {
                        text: i18n.tr("Swipe from right to left to change tab.")
                    }
                }
            }
        }
        
        // Second tab begins here
        Tab {
            objectName: "Tab2"
            
            title: i18n.tr("Optional Screen")
            page: Page {
                anchors.margins: units.gu(2)
                
                tools: ToolbarActions {
                    Action {
                        objectName: "action"
                        
                        iconSource: Qt.resolvedUrl("avatar.png")
                        text: i18n.tr("Tap me!")
                        
                        onTriggered: {
                            label.text = i18n.tr("Toolbar tapped")
                        }
                    }
                }
                
                Column {
                    anchors.centerIn: parent
                    Label {
                        id: label
                        objectName: "label"
                        
                        text: i18n.tr("Swipe from bottom to up to reveal the toolbar.")
                    }
                }
            }
        }
    }
}
