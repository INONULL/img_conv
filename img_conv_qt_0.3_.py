#encoding: euc-kr
import os, pillow_heif, sys
from PIL import Image
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QLineEdit, QMessageBox, QProgressBar, QCheckBox, QMenuBar
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QCursor, QFont, QIcon, QAction #, QPixmap

basedir = os.path.dirname(__file__)
class ImageResizer(QWidget):
    def __init__(self):
        super().__init__()
        self.input_folder = ""
        self.output_folder = ""
        self.convert_subfolders = False
        self.extensions = []
        self.export_extensions = []
        self.button_press_count_folder = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(os.path.join(basedir, 'resize.ico')))    
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.Window)
        self.setWindowTitle("IMG_Converter")
        #self.setCursor(QCursor(QPixmap('cursor.png').scaled(300,300)))

        input_folder_button = QPushButton("Select Input Folder", self)
        input_folder_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        input_folder_button.clicked.connect(self.on_select_input_folder)
        self.input_folder_label = QLabel("Input Folder: ", self)

        subfolders_checkbox = QCheckBox("Convert Subfolders", self)
        subfolders_checkbox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        subfolders_checkbox.stateChanged.connect(self.on_subfolders_checkbox_changed)

        output_folder_button = QPushButton("Select Output Folder", self)
        output_folder_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        output_folder_button.clicked.connect(self.on_select_output_folder)
        self.output_folder_label = QLabel("Output Folder: ", self)

        extensions_label = QLabel("Extensions: ", self)
        self.extensions_combobox = QComboBox(self)
        self.extensions_combobox.addItems(["JPG", "JPEG", "PNG", "TIF", "TIFF", "HEIC"])  # Add other supported extensions
        self.extensions_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
      
        export_extensions_label = QLabel("Export Extensions: ", self)
        self.export_extensions_combobox = QComboBox(self)
        self.export_extensions_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.export_extensions_combobox.addItems(["JPG", "JPEG", "PNG", "TIF", "TIFF", "HEIC"])  # Add other supported extensions

        max_size_label = QLabel("Horizontal_Pixel_Size: \n(Ratio Respects to the Origin)", self)

        self.max_size_entry = QLineEdit(self)

        resize_button = QPushButton("Resize Images", self)
        resize_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        resize_button.clicked.connect(self.on_resize_images)

        self.status_label = QLabel("", self)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        menubar = QMenuBar(self)
        help_menu = menubar.addMenu("Help")

        howtouse_action = QAction("How To Use", self)
        howtouse_action.triggered.connect(self.show_howtouse_dialog)
        help_menu.addAction(howtouse_action)

        reference_action = QAction("Library Used", self)
        reference_action.triggered.connect(self.show_reference_dialog)
        help_menu.addAction(reference_action)

        algorithm_action = QAction("Algorithm Used", self)
        algorithm_action.triggered.connect(self.show_algorithm_dialog)
        help_menu.addAction(algorithm_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        vbox = QVBoxLayout()
        vbox.addWidget(input_folder_button)
        vbox.addWidget(self.input_folder_label)
        vbox.addWidget(subfolders_checkbox)
        vbox.addWidget(output_folder_button)
        vbox.addWidget(self.output_folder_label)
        vbox.addWidget(extensions_label)
        vbox.addWidget(self.extensions_combobox)
        vbox.addWidget(export_extensions_label)
        vbox.addWidget(self.export_extensions_combobox)
        vbox.addWidget(max_size_label)
        vbox.addWidget(self.max_size_entry)
        vbox.addWidget(resize_button)
        vbox.addWidget(self.status_label)
        vbox.addWidget(self.progress_bar)
        vbox.setMenuBar(menubar)
        self.setLayout(vbox)
        self.setMinimumSize(500, 500)
        self.adjustSize()
        self.setMaximumSize(1000, 500)
        vbox = QVBoxLayout()

        self.show()

    def show_howtouse_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("How To Use")
        msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setText("Select Input Folder: 변환 대상 파일이 위치한 폴더 선택\nConvert Subfolders: 서브폴더 포함 변환\nSelect Output Folder: 변환 된 파일이 위치 할 폴더 설정\nExtensions: 변환 대상 파일의 확장자 선택\nExport Extensions: 변환 확장자 선택\nHorizontal_Pixel_Size: [가로기준] 해상도 설정 (비율은 원본을 따라감)\nResize Images: 변환 시작 ")
        msg_box.exec()

    def show_about_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About Image Resizer")
        msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setText("This is an image resizing application.\nCoded by JunSungLEE\nContact(Bug_Report): ljs_fr@nate.com")
        msg_box.exec()

    def show_reference_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Library Used")
        msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setText("Python3.11.7, Pillow, Pillow_heif, PyQt6, Pyinstaller")
        msg_box.exec()

    def show_algorithm_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Algorithm Used")
        msg_box.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg_box.setText("Python Libray(Pillow) -> resampling.Lanczos\nNot recommended to use for converting thin graphs.")
        msg_box.exec()

    def on_select_input_folder(self):
        default_folder = os.path.expanduser("~")
        if self.button_press_count_folder == 0:
            folder = QFileDialog.getExistingDirectory(self, "Select Input Folder", default_folder)
        else:
            folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_folder_label.setText(f"Input Folder: {self.input_folder}")
        self.button_press_count_folder = 1

    def on_select_output_folder(self):
        default_folder = os.path.expanduser("~")
        if self.button_press_count_folder == 0:
            folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", default_folder)
        else:
            folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Output Folder: {self.output_folder}")
        self.button_press_count_folder = 1

    def on_subfolders_checkbox_changed(self, state):
        self.convert_subfolders = state == Qt.CheckState.Checked.value

    def on_resize_images(self):
        if not self.input_folder or not self.output_folder:
            QMessageBox.warning(self, "Missing Folders", "Please select input and output folders.")
            return

        max_size_text = self.max_size_entry.text()
        if not max_size_text.isdigit():
            QMessageBox.warning(self, "Invalid Max Size", "Max Size should be a positive integer.")
            return

        self.extensions = [str(self.extensions_combobox.currentText()).lower()]
        self.export_extensions = [str(self.export_extensions_combobox.currentText()).lower()]

        if self.convert_subfolders:
            #self.resize_images_in_folder(self.input_folder, self.output_folder, int(max_size_text))
            self.resize_thread = ResizeThread(self.input_folder, self.output_folder, max_size_text, self.extensions, self.export_extensions)
            self.resize_thread.nofile.connect(self.show_error)
            self.resize_thread.progressChanged.connect(self.update_progress)
            self.resize_thread.finished.connect(self.resize_finished)
            self.resize_thread.start()
        else:
            self.resize_images_in_folder(self.input_folder, self.output_folder, int(max_size_text))
            
            
    def resize_images_in_folder(self, input_folder, output_folder, max_size):
        num_images = 0
        processed_images = 0

        for file_name in os.listdir(input_folder):
            input_path = os.path.join(input_folder, file_name)
            if os.path.isfile(input_path):
                _, extension = os.path.splitext(file_name)
                if extension[1:].lower() in self.extensions:
                    num_images += 1

        if num_images == 0:
            QMessageBox.warning(self, "No Images Found", f"No images with the selected extensions found in the input folder.")
            return

        for file_name in os.listdir(input_folder):
            input_path = os.path.join(input_folder, file_name)
            if os.path.isfile(input_path):
                _, extension = os.path.splitext(file_name)
                if extension[1:].lower() in self.extensions:
                    output_path = os.path.join(output_folder, file_name)
                    self.resize_image(input_path, output_path, max_size)
                    processed_images += 1
                    progress = int((processed_images / num_images) * 100)
                    self.update_progress(progress, processed_images, num_images)
        if self.convert_subfolders:
            return
        else:
            self.resize_finished()

    def resize_image(self, input_path, output_path, max_size):
        try:
            pillow_heif.register_heif_opener()
            image = Image.open(input_path)
            width, height = image.size
            aspect_ratio = width / height

            if width > height:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)

            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Get the selected export extension
            selected_export_extension = self.export_extensions[0]
            file_name, _ = os.path.splitext(os.path.basename(output_path))

            if selected_export_extension == "jpg" or selected_export_extension == "jpeg":
                # Convert the image to RGB mode if the selected export extension is JPEG
                resized_image = resized_image.convert("RGB")

            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"{file_name}.{selected_export_extension}")
            if selected_export_extension == "heic":
                resized_image.save(output_path, format="HEIF")
            else:
                resized_image.save(output_path)
        except Exception as e:
            raise Exception(f"Error resizing image '{input_path}': {str(e)}")

    def update_progress(self, progress, processed_images, num_images):
        self.status_label.setText(str(processed_images) + " / " + str(num_images))
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}%")

    def resize_finished(self):
        self.status_label.setText("Done")
        def showDialog():
            msgBox = QMessageBox()
            msgBox.setWindowIcon(QIcon(os.path.join(basedir, 'resize.ico')))
            msgBox.setText("Image resizing completed\n Click 'OK' to Open Output Folder")
            msgBox.setWindowTitle("Job Finished!")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.StandardButton.Ok:
                path = os.path.realpath(self.output_folder)
                os.startfile(path)
        showDialog()
        self.progress_bar.setValue(0)
        self.input_folder = ""
        self.output_folder = ""
        self.input_folder_label.setText(f"Input Folder: {self.input_folder}")
        self.output_folder_label.setText(f"Output Folder: {self.output_folder}")

    def show_error(self):
        QMessageBox.warning(self, "No Images Found in Subfolders", f"No images with the selected extensions found in Subfolders.")


class ResizeThread(QThread):
    progressChanged = Signal(int, int, int)
    finished = Signal()
    nofile = Signal()

    def __init__(self, input_folder, output_folder, max_size, extensions, export_extensions):
        super().__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.max_size = int(max_size)
        self.extensions = extensions
        self.export_extensions = export_extensions

    def run(self):
        num_images = 0
        processed_images = 0

        for root, dirs, files in os.walk(self.input_folder):
            for file_name in files:
                _, extension = os.path.splitext(file_name)
                if extension[1:].lower() in self.extensions:
                    num_images += 1

        if num_images == 0:
            self.nofile.emit()
            return

        for root, dirs, files in os.walk(self.input_folder):
            for file_name in files:
                input_path = os.path.join(root, file_name)
                _, extension = os.path.splitext(file_name)
                if extension[1:].lower() in self.extensions:
                    output_path = self.get_output_path(input_path)
                    self.resize_image(input_path, output_path)
                    processed_images += 1
                    progress = int((processed_images / num_images) * 100)
                    self.progressChanged.emit(progress, processed_images, num_images)
        self.finished.emit()

    def get_output_path(self, input_path):
        relative_path = os.path.relpath(input_path, self.input_folder)
        output_path = os.path.join(self.output_folder, relative_path)
        return output_path

    def resize_image(self, input_path, output_path):
        try:
            pillow_heif.register_heif_opener()
            image = Image.open(input_path)
            width, height = image.size
            aspect_ratio = width / height
            if width > height:
                new_width = self.max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = self.max_size
                new_width = int(new_height * aspect_ratio)
            
            # Get the selected export extension
            selected_export_extension = self.export_extensions[0]
            file_name, _ = os.path.splitext(os.path.basename(output_path))

            if selected_export_extension == "jpg" or selected_export_extension == "jpeg":
                # Convert the image to RGB mode if the selected export extension is JPEG
                resized_image = resized_image.convert("RGB")
        
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"{file_name}.{selected_export_extension}")
            if selected_export_extension == "heic":
                resized_image.save(output_path, format="HEIF")
            else:
                resized_image.save(output_path)
        except Exception as e:
            raise Exception(f"Error resizing image '{input_path}': {str(e)}")


class HighDpiFix:
    def __init__(self):
        if sys.platform == 'win32':
            if hasattr(Qt, 'AA_EnableHighDpiScaling'):
                QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

            # Enable DPI awareness on Windows Vista (6.0) and later
            if sys.getwindowsversion().major >= 6:
                try:
                    from ctypes import windll
                    windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                except ImportError:
                    pass

if __name__ == "__main__":
    high_dpi_fix = HighDpiFix()
    app = QApplication([])
    app.setFont(QFont('Serif', 10, QFont.Weight.Light))
    image_resizer = ImageResizer()
    app.exec()