import os

from PyQt6.QtCore import QSize, pyqtSignal, QEvent, Qt, QPoint
from PyQt6.QtGui import QPixmap, QColor, QCursor, QMouseEvent, QIcon, QPalette
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, \
    QFileDialog, QStackedWidget, QColorDialog, QGraphicsView, QDial, QSpinBox, QFontDialog, QRadioButton, QDialog, \
    QDialogButtonBox, QMessageBox, QStyleFactory, QStatusBar
from PyQt6 import uic
import sys
import matplotlib.font_manager as font_search
from PIL import Image,ImageFont, ImageDraw
import webbrowser
import shutil

class MainPage(QMainWindow):
    def __init__(self):
      shutil.rmtree("Output")
      os.mkdir("Output")
      self.icon=QIcon("Core/favicon.ico")
      super(MainPage,self).__init__()
      uic.loadUi("Core/form.ui",self)

      self.pressing = False

      self.status_bar=QStatusBar()
      self.status_bar.setSizeGripEnabled(False)
      self.setStatusBar(self.status_bar)
      self.setFixedSize(1190, 742)
      self.cursor=QCursor()
      self.number_of_rows=self.findChild(QSpinBox,"num_of_rows")

      self.get_result=self.findChild(QPushButton,"get_result")
      self.get_result.clicked.connect(self.deliver_result)

      self.custom_font_size_box=self.findChild(QSpinBox,"custom_font_size")
      self.custom_font_size_box.setMaximum(2000)
      self.custom_font_size_box.setValue(100)

      self.watermark_rotation=self.findChild(QSpinBox,"watermark_rotation")

      self.radio_sys_font=self.findChild(QRadioButton,"radio_sys_font")
      self.radio_sys_font.setChecked(True)
      self.radio_custom_font=self.findChild(QRadioButton,"radio_custom_font")

      self.button = self.findChild(QPushButton,"Button1_2")
      self.color_btn = self.findChild(QPushButton, "color_btn")
      self.stacked_widget=self.findChild(QStackedWidget,"stackedWidget")
      self.back_btn = self.findChild(QPushButton, "pushButton_2")

      self.number_of_watermarks=self.findChild(QSpinBox,"num_of_watermarks")


      self.picture_frame = self.findChild(QLabel, "label")
      self.render_button=self.findChild(QPushButton,"Renderbutton")
      self.render_button.clicked.connect(self.draw)


      self.color_wind = self.findChild(QGraphicsView, "graphicsView")

      self.font_dlg=QFontDialog()
      self.font_btn=self.findChild(QPushButton,"font_button")
      self.font_btn.clicked.connect(self.select_font)

      self.label_text=self.findChild(QLineEdit,"lineEdit")

      self.commit_btn=self.findChild(QPushButton,"commit_btn")
      self.commit_btn.clicked.connect(self.commit)

      self.opacity_box = self.findChild(QSpinBox, "opacity_box")
      self.opacity_box.setMaximum(100)
      self.opacity_box.setValue(50)

      self.dial=self.findChild(QDial,"dial")
      self.dial.setValue(50)
      self.dial.setRange(0, 100)
      self.dial.setSingleStep(1)
      self.dial.setNotchesVisible(True)
      self.dial.valueChanged.connect(self.opacity_box.setValue)

      self.opacity_box.valueChanged.connect(self.dial.setValue)

      self.custom_font_dlg=QFileDialog()
      self.custom_font_dlg.setNameFilters(["Fonts (*.ttf *.otf)"])
      self.custom_font_dlg.selectNameFilter("True type fonts (*.ttf)")
      self.custom_font_btn=self.findChild(QPushButton,"Custom_font_btn")
      self.custom_font_btn.clicked.connect(self.select_custom_font)


      self.button.clicked.connect(self.button_clicked)
      self.dlg=QFileDialog()
      self.dlg.setNameFilters(["Images (*.png *.jpg *.jpeg)"])
      self.dlg.selectNameFilter("Images (*.png *.jpg)")
      self.color_dlg=QColorDialog()
      self.color_btn.clicked.connect(self.select_color)
      self.back_btn.clicked.connect(self.go_back)

      self.color=QColor(0,0,0)




    def deliver_result(self):
        self.im.save(f"Output/output_img.{self.file_ext}")
        webbrowser.open("Output")

    def button_clicked(self):
        self.dlg.exec()
        self.filenames = self.dlg.selectedFiles()
        if self.filenames:
            picture_name=self.filenames[0]
            self.picture_frame.setPixmap(QPixmap(self.filenames[0]))
            self.file_ext=self.filenames[0].split(".")[1]
            self.picture_frame.setScaledContents( True )
            self.stacked_widget.setCurrentIndex(1)
            self.im = Image.open(self.filenames[0])
            shutil.rmtree("Processing")
            os.mkdir("Processing")

            self.im.save(f"Processing/processed_image.{self.file_ext}")

            self.im = Image.open(f"Processing/processed_image.{self.file_ext}")



    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)

    def select_color(self):
        self.color_dlg.exec()
        if self.color_dlg.selectedColor():
            self.color=self.color_dlg.selectedColor()

            self.color_wind.setStyleSheet(f'background-color:{self.color.name()}')


    def commit(self):
        self.im=Image.open(f"Processing/buffer_img.{self.file_ext}")
        self.im.save(f"Processing/processed_image.{self.file_ext}")
        self.im=Image.open(f"Processing/processed_image.{self.file_ext}")

    def draw(self):
        self.im = Image.open(f"Processing/processed_image.{self.file_ext}")
        self.im.save(f"Processing/buffer_img.{self.file_ext}")
        if self.radio_sys_font.isChecked():
            if type(self.font) == str:

                font = ImageFont.truetype(self.font, self.font_size)
            else:
                return QMessageBox.warning(self, "Error", "Please, select a system font to proceed")

        elif self.radio_custom_font.isChecked():
            if self.custom_font_dlg.selectedFiles():
                font = ImageFont.truetype(self.custom_font, self.custom_font_size_box.value())
            else:
                return QMessageBox.warning(self, "Error", "Please, select a custom font to proceed")


        if self.number_of_rows.value()>self.number_of_watermarks.value():
            return QMessageBox.warning(self, "Error", "Number of rows cannot exceed number of watermarks")

        ascent, descent = font.getmetrics()
        text_width = font.getmask(self.label_text.text()).getbbox()[2]
        text_height = font.getmask(self.label_text.text()).getbbox()[3] + descent


        x=0
        y=0


        ready_image=self.im.convert("RGBA")
        items_in_row_max=self.number_of_watermarks.value()//self.number_of_rows.value()

        for row in range(self.number_of_rows.value()):

            y = ((self.im.height//self.number_of_rows.value()//2) + (self.im.height//self.number_of_rows.value())*row)

            x=0
            for item in range(items_in_row_max):
                text_layer = Image.new("RGBA", (self.im.width, self.im.height), (0, 0, 0, 0))
                x = ((self.im.width // items_in_row_max // 2) + (
                            self.im.width // items_in_row_max) * item)
                text_box = Image.new("RGBA", (text_width, text_height), (0,0,0,0))




                ImageDraw.Draw(text_box).text((0,0),
                       self.label_text.text(), fill=(self.color.red(), self.color.green(), self.color.blue(),
                                                     self.dial.value() * 255 // 100), font=font)

                text_box=text_box.rotate(self.watermark_rotation.value(), expand = 1)
                text_layer.paste(text_box,box=(x-text_box.width//2,y-text_box.height//2))

                ready_image=Image.alpha_composite(ready_image,text_layer)

        x = 0
        y = 0

        if self.file_ext=="jpeg" or self.file_ext=="jpg":
            ready_image=ready_image.convert("RGB")

        ready_image.save(f"Processing/buffer_img.{self.file_ext}")

        self.picture_frame.setPixmap(QPixmap(f"Processing/buffer_img.{self.file_ext}"))

        return self.picture_frame.setScaledContents(True)




    def select_font(self):
        self.font_dlg.exec()
        if self.font_dlg.selectedFont():
            self.font=self.font_dlg.selectedFont()
            self.font_size=int(self.font.key().split(',')[1])
            font_props=font_search.FontProperties(family=self.font.family())
            self.font=font_search.findfont(prop=font_props,fallback_to_default=True)
            if self.font.split("\\")[-1]=="DejaVuSans.ttf":
                return QMessageBox.warning(self, "Error", "Failed to locate selected font, defaulting to DejaVu Sans")


    def select_custom_font(self):
        self.custom_font_dlg.exec()
        if self.custom_font_dlg.selectedFiles():
            self.custom_font=self.custom_font_dlg.selectedFiles()[0]


app = QApplication(sys.argv)

darkPalette = QPalette()
darkPalette.setColor(QPalette.ColorRole.PlaceholderText,Qt.GlobalColor .gray)
darkPalette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor .white)
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole .WindowText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66,66))
darkPalette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor .white)
darkPalette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor .white)
darkPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole .Text, QColor(127, 127, 127))
darkPalette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
darkPalette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
darkPalette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor .white)
192
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole .ButtonText, QColor(127, 127, 127))
darkPalette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor. red)
darkPalette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130,
218))
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole .Highlight, QColor(80, 80, 80))
darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt .GlobalColor.white)
darkPalette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole .HighlightedText, QColor(127, 127, 127))


app.setPalette(darkPalette)

window = MainPage()
window.setWindowTitle("Watermarker")
window.setWindowIcon(window.icon)


window.show()
styles=QStyleFactory()

app.setStyle('Fusion')

app.exec()




