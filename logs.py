import sys
import psutil
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt

class ProcessMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Process Monitor Tool")
        self.setGeometry(200, 200, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Theme Selector
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Light Theme", "Dark Theme"])
        self.theme_selector.currentIndexChanged.connect(self.change_theme)
        self.layout.addWidget(self.theme_selector)

        # Process Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "RAM (MB)", "User"])
        self.layout.addWidget(self.table)

        # Buttons and Kill Input
        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh Processes")
        self.refresh_button.clicked.connect(self.refresh_processes)
        button_layout.addWidget(self.refresh_button)

        self.save_button = QPushButton("Save Report")
        self.save_button.clicked.connect(self.save_report)
        button_layout.addWidget(self.save_button)

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Enter PID to kill")
        button_layout.addWidget(self.pid_input)

        self.kill_button = QPushButton("Kill Process")
        self.kill_button.clicked.connect(self.kill_process)
        button_layout.addWidget(self.kill_button)

        self.layout.addLayout(button_layout)

        # Status Label
        self.status_label = QLabel()
        self.layout.addWidget(self.status_label)

        # Initial Load
        self.refresh_processes()

    def refresh_processes(self):
        """Fetch and display the processes in the table."""
        self.table.setRowCount(0)  # Clear the table

        try:
            # Refresh CPU usage for all processes
            psutil.cpu_percent(interval=0.1, percpu=False)

            processes = []
            for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
                try:
                    proc_info = {
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.cpu_percent(interval=0.1),
                        "memory_mb": proc.memory_info().rss / 1024 / 1024,
                        "username": proc.info['username'] or "N/A"
                    }
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            # Populate the table
            for row, proc in enumerate(processes):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(proc['pid'])))
                self.table.setItem(row, 1, QTableWidgetItem(proc['name']))
                self.table.setItem(row, 2, QTableWidgetItem(f"{proc['cpu_percent']:.2f}"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{proc['memory_mb']:.2f}"))
                self.table.setItem(row, 4, QTableWidgetItem(proc['username']))

            self.status_label.setText(f"Loaded {len(processes)} processes.")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def save_report(self):
        """Save the process list as a JSON file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "process_report.json", "JSON Files (*.json)", options=options)

        if file_path:
            try:
                processes = []
                for row in range(self.table.rowCount()):
                    process = {
                        "PID": self.table.item(row, 0).text(),
                        "Name": self.table.item(row, 1).text(),
                        "CPU %": self.table.item(row, 2).text(),
                        "RAM (MB)": self.table.item(row, 3).text(),
                        "User": self.table.item(row, 4).text()
                    }
                    processes.append(process)

                with open(file_path, 'w') as f:
                    json.dump(processes, f, indent=4)

                self.status_label.setText(f"Report saved to {file_path}")
            except Exception as e:
                self.status_label.setText(f"Error saving report: {e}")

    def kill_process(self):
        """Kill a process by PID."""
        pid_text = self.pid_input.text()
        if not pid_text.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid PID.")
            return

        pid = int(pid_text)
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            QMessageBox.information(self, "Success", f"Process {pid} terminated successfully.")
            self.refresh_processes()
        except psutil.NoSuchProcess:
            QMessageBox.warning(self, "Error", f"No process found with PID {pid}.")
        except psutil.AccessDenied:
            QMessageBox.critical(self, "Error", f"Access denied to terminate process {pid}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to terminate process {pid}: {e}")

    def change_theme(self):
        """Change the application theme."""
        theme = self.theme_selector.currentText()
        if theme == "Light Theme":
            self.central_widget.setStyleSheet("background-color: white; color: black;")
            self.table.setStyleSheet("QTableWidget { background-color: white; color: black; }")
        elif theme == "Dark Theme":
            self.central_widget.setStyleSheet("background-color: black; color: white;")
            self.table.setStyleSheet("QTableWidget { background-color: black; color: white; }")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProcessMonitor()
    window.show()
    sys.exit(app.exec_())
