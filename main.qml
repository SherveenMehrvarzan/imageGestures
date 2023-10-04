import QtQuick
import QtQuick.Window 
import QtMultimedia
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs




Window {
    visible: true
    width: 600
    height: 500
    title: "WebCam"


    Image {
        id: feedImage
        width: parent.width
        height: parent.height - 50
        fillMode: Image.PreserveAspectFit
        cache: false
        source: "image://MyImageProvider/img"
        property bool counter: false

        function reloadImage() {
            counter = !counter
            source = "image://MyImageProvider/img?id=" + counter
        }
    }

    RowLayout {
        anchors.top: feedImage.bottom
        anchors.horizontalCenter: feedImage.horizontalCenter

        Button {
            id: btnStartCamera
            text: "Start Camera"
            onClicked: {
                myImageProvider.start()
            }
        }
        
        Button {
            id: btnStopCamera
            text: "Stop Camera"
            onClicked: {
                myImageProvider.killThread()
             }
        }


    }

    
    Connections{
        target: myImageProvider

        function onImageChanged(image) {
            console.log("emit")
            feedImage.reloadImage()
        }
            
    }

}