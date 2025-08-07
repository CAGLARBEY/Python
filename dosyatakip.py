import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QWidget, QLineEdit, QHBoxLayout, QTimeEdit, QCheckBox
)
from PyQt5.QtCore import QThread, pyqtSignal, QTime, QTimer
from PyQt5.QtGui import QColor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderWatcherHandler(FileSystemEventHandler):
    """Custom event handler for folder watching."""
    def __init__(self, log_signal, file_filter, stats_signal):
        super().__init__()
        self.log_signal = log_signal
        self.file_filter = file_filter
        self.stats_signal = stats_signal
        self.event_count = 0

    def filter_event(self, path):
        """Check if the event matches the file filter."""
        if self.file_filter:
            return path.endswith(self.file_filter)
        return True

    def log_event(self, event_type, path, dest_path=None):
        """Log an event and update stats."""
        self.event_count += 1
        self.stats_signal.emit(self.event_count)
        if dest_path:
            self.log_signal.emit(f"{event_type}: {path} -> {dest_path}")
        else:
            self.log_signal.emit(f"{event_type}: {path}")

    def on_modified(self, event):
        if self.filter_event(event.src_path):
            self.log_event("Modified", event.src_path)

    def on_created(self, event):
        if self.filter_event(event.src_path):
            self.log_event("Created", event.src_path)

    def on_deleted(self, event):
        if self.filter_event(event.src_path):
            self.log_event("Deleted", event.src_path)

    def on_moved(self, event):
        if self.filter_event(event.src_path):
            self.log_event("Moved", event.src_path, event.dest_path)

class FolderWatcherThread(QThread):
    log_signal = pyqtSignal(str)
    stats_signal = pyqtSignal(int)

    def __init__(self, folder_path, file_filter):
        super().__init__()
        self.folder_path = folder_path
        self.file_filter = file_filter
        self.observer = None

    def run(self):
        self.observer = Observer()
        event_handler = FolderWatcherHandler(self.log_signal, self.file_filter, self.stats_signal)
        self.observer.schedule(event_handler, self.folder_path, recursive=True)
        self.observer.start()
        self.exec_()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()

class FolderWatcherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Watcher")
        self.setGeometry(200, 200, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.central_widget.setStyleSheet("background-color: black; color: white;")

        self.status_label = QLabel("Select a folder to start watching.")
        self.status_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.status_label)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: black; color: white;")
        self.layout.addWidget(self.log_output)

        self.stats_label = QLabel("Events Count: 0")
        self.stats_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.stats_label)

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Select Folder and Start Watching")
        self.start_button.clicked.connect(self.select_folder)
        self.start_button.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Watching")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_watching)
        self.stop_button.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(self.stop_button)

        self.save_log_button = QPushButton("Save Log to File")
        self.save_log_button.clicked.connect(self.save_log)
        self.save_log_button.setStyleSheet("background-color: gray; color: white;")
        button_layout.addWidget(self.save_log_button)

        self.layout.addLayout(button_layout)

        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter file extension filter (e.g., .txt)")
        self.filter_input.setStyleSheet("background-color: gray; color: white;")
        filter_layout.addWidget(self.filter_input)
        self.layout.addLayout(filter_layout)

        timing_layout = QHBoxLayout()
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime.currentTime())
        self.start_time_edit.setStyleSheet("background-color: gray; color: white;")
        timing_layout.addWidget(self.start_time_edit)

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime(23, 59))
        self.end_time_edit.setStyleSheet("background-color: gray; color: white;")
        timing_layout.addWidget(self.end_time_edit)

        self.time_check = QCheckBox("Enable Timing")
        self.time_check.setStyleSheet("color: white;")
        timing_layout.addWidget(self.time_check)

        self.layout.addLayout(timing_layout)

        self.folder_path = None
        self.watcher_thread = None
        self.event_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_timing)

    def select_folder(self):
        """Open a dialog to select a folder and start watching it."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Watch")
        if folder:
            self.folder_path = folder
            self.status_label.setText(f"Watching folder: {self.folder_path}")
            self.start_watching()

    def start_watching(self):
        """Start the folder watching thread."""
        if self.folder_path:
            file_filter = self.filter_input.text().strip()
            self.watcher_thread = FolderWatcherThread(self.folder_path, file_filter)
            self.watcher_thread.log_signal.connect(self.log_event)
            self.watcher_thread.stats_signal.connect(self.update_stats)
            self.watcher_thread.start()
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.timer.start(1000)  # Check timing every second

    def stop_watching(self):
        """Stop the folder watching thread."""
        if self.watcher_thread:
            self.watcher_thread.stop()
            self.watcher_thread = None
            self.timer.stop()
            self.status_label.setText("Stopped watching.")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def log_event(self, message):
        """Log events to the text output."""
        self.log_output.append(message)

    def update_stats(self, count):
        """Update the stats label."""
        self.stats_label.setText(f"Events Count: {count}")

    def save_log(self):
        """Save the log output to a file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log File", "log.txt", "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.log_output.toPlainText())
                self.status_label.setText(f"Log saved to {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error saving log: {e}")

    def check_timing(self):
        """Enable or disable watching based on timing."""
        if self.time_check.isChecked():
            current_time = QTime.currentTime()
            if not (self.start_time_edit.time() <= current_time <= self.end_time_edit.time()):
                self.stop_watching()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderWatcherApp()
    window.show()
    sys.exit(app.exec_())
