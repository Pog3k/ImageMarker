from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QCursor
from PyQt5.QtCore import *
from image_marker_ui import Ui_MainWindow

import sys

class DraggableBox( QGraphicsItem ):
    """
    A simple QGraphicsItem that can be dragged around the scene.
    Of course, this behavior is easier to achieve if you simply use the default
    event handler implementations in place and call
    QGraphicsItem.setFlags( QGraphicsItem.ItemIsMovable )

    ...but this example shows how to do it by hand, in case you want special behavior
    (e.g. only allowing left-right movement instead of arbitrary movement).
    """

    def __init__(self, rect, parent, *args, **kwargs):
        #super( DraggableBox, self ).__init__( parent, *args, **kwargs )
        super(DraggableBox, self).__init__(parent, *args, **kwargs)
        self.setAcceptHoverEvents(True)
        self.offset = 20
        self._rect = rect
        self.mouse_hover_event = False
        self.setZValue(1000)
        #self.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable)

        self.rect_top_left  = QRectF(self._rect.topLeft().x(), self._rect.topLeft().y(),
                                     self.offset, self.offset)

        self.rect_top_left = self.rect_top_left.normalized()


    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget):
        painter.drawText( QPointF(0,10), "DragableBox" )
        if self.mouse_hover_event:
            painter.drawRect( self.rect_top_left)
        painter.drawRect( self.boundingRect() )

        self.prepareGeometryChange()

    def hoverEnterEvent(self, event):
        cursor = QCursor( Qt.OpenHandCursor )
        QApplication.instance().setOverrideCursor( cursor )
        self.mouse_hover_event = True
        self.prepareGeometryChange()

    def hoverLeaveEvent(self, event):
        self.mouse_hover_event = False
        QApplication.instance().restoreOverrideCursor()
        self.prepareGeometryChange()

    def mouseMoveEvent(self, event):
        # new_pos = event.scenePos()
        # self.setPos( new_pos )

        delta = QPointF(event.scenePos() - self.oldPos)
        self.setPos(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.scenePos()

    # We must override these or else the default implementation prevents
    #  the mouseMoveEvent() override from working.
    def mousePressEvent(self, event):

        self.oldPos = event.scenePos()

    def mouseReleaseEvent(self, event): pass

class BoxResizable(QGraphicsRectItem):
    def __init__(self, rect, parent = None,*args, **kwargs):
        QGraphicsRectItem.__init__(self, rect, parent,*args, **kwargs)

        self.setAcceptHoverEvents(True)


    def paint(self, painter, option, widget):
        painter.drawText( QPointF(0,10), "Hiyaaa" )
       # painter.drawRect( self.boundingRect() )
        super().paint(painter, option, widget)

    # def boundingRect(self):
    #     #return QRectF( -50.0, 50.0, 100.0, -100.0)
    #     print(self.rect())
    #     return self.rect()

    def hoverEnterEvent(self, event):
        cursor = QCursor( Qt.OpenHandCursor )
        QApplication.instance().setOverrideCursor( cursor )

    def hoverLeaveEvent(self, event):
        QApplication.instance().restoreOverrideCursor()

    def mouseMoveEvent(self, event):
        new_pos = event.scenePos()
        self.setPos( new_pos )

    def mouseMoveEvent(self, event):
        new_pos = event.scenePos()
        self.setPos( new_pos )
    # We must override these or else the default implementation prevents
    #  the mouseMoveEvent() override from working.
    def mousePressEvent(self, event): pass
    def mouseReleaseEvent(self, event): pass

class ResizableRubberBand(QtWidgets.QWidget):
    """Wrapper to make QRubberBand mouse-resizable using QSizeGrip

    Source: http://stackoverflow.com/a/19067132/435253
    """
    def __init__(self, parent=None):
        super(ResizableRubberBand, self).__init__(parent)

        self.setWindowFlags(Qt.SubWindow)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.grip1 = QtWidgets.QSizeGrip(self)
        self.grip2 = QtWidgets.QSizeGrip(self)
        self.grip3 = QtWidgets.QSizeGrip(self)
        self.layout.addWidget(self.grip1, 0, Qt.AlignLeft | Qt.AlignTop)
        self.layout.addWidget(self.grip2, 0, Qt.AlignRight | Qt.AlignBottom)
        self.layout.addWidget(self.grip3, 0, Qt.AlignRight | Qt.AlignTop)

        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberband.move(0, 0)
        self.rubberband.show()
        self.show()

    def mousePressEvent(self, event):
        '''
            Mouse is pressed. If selection is visible either set dragging mode (if close to border) or hide selection.
            If selection is not visible make it visible and start at this point.
        '''
        self.oldPos = event.globalPos()
        if event.button() == Qt.LeftButton:
            pass
            #print("hello")

    def mouseMoveEvent(self, event):
        #self.rubberband.move(event.screenPos())
        # orig_cursor_position = event.las  lastPos()
        # updated_cursor_position = event.Pos()

        # orig_position = self.scenePos()

        # updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        # updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        # self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()



    def resizeEvent(self, event):
        self.rubberband.resize(self.size())

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        im = QPixmap("./simple_images/thai_chilli/thai chilli_63.jpeg")
        # self.band = ResizableRubberBand(self.ui.ImageViewer)

        # self.band.move(100, 100)
        # self.band.resize(50, 50)
        # self.band.setMinimumSize(30, 30)
        # self.ui.ImageViewer.setPixmap(im)

        self.image_scene = QGraphicsScene(self.ui.ImageViewer)
        self.ui.ImageViewer.setScene(self.image_scene )

        self.box = BoxResizable( rect=QRectF(0, 0, 50, 50), parent = None)

        self.image_scene.addItem(self.box)
        dragbox = DraggableBox( QRectF( 0, 0, 150, 100),None)
        dragbox.setPos( 10,20 )
        #box.setRotation(45)
        self.image_scene.addItem(dragbox)
        #self.box.move(150, 150)
        #self.box.resize(80, 80)
        #self.box.setMinimumSize(30, 30)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()