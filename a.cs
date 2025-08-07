using System;
using System.Windows.Forms;

namespace ToDoListApp
{
    public class MainForm : Form
    {
        private TextBox taskInput;
        private Button addButton;
        private Button removeButton;
        private ListBox taskList;

        public MainForm()
        {
            InitializeComponents();
        }

        private void InitializeComponents()
        {
            // Form Settings
            this.Text = "To-Do List";
            this.Size = new System.Drawing.Size(400, 500);

            // Task Input
            taskInput = new TextBox();
            taskInput.Location = new System.Drawing.Point(20, 20);
            taskInput.Width = 250;
            this.Controls.Add(taskInput);

            // Add Button
            addButton = new Button();
            addButton.Text = "Add";
            addButton.Location = new System.Drawing.Point(280, 18);
            addButton.Click += AddButton_Click;
            this.Controls.Add(addButton);

            // Remove Button
            removeButton = new Button();
            removeButton.Text = "Remove";
            removeButton.Location = new System.Drawing.Point(280, 60);
            removeButton.Click += RemoveButton_Click;
            this.Controls.Add(removeButton);

            // Task List
            taskList = new ListBox();
            taskList.Location = new System.Drawing.Point(20, 60);
            taskList.Size = new System.Drawing.Size(250, 350);
            this.Controls.Add(taskList);
        }

        private void AddButton_Click(object sender, EventArgs e)
        {
            string task = taskInput.Text.Trim();

            if (!string.IsNullOrEmpty(task))
            {
                taskList.Items.Add(task);
                taskInput.Clear();
            }
            else
            {
                MessageBox.Show("Please enter a task.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void RemoveButton_Click(object sender, EventArgs e)
        {
            if (taskList.SelectedItem != null)
            {
                taskList.Items.Remove(taskList.SelectedItem);
            }
            else
            {
                MessageBox.Show("Please select a task to remove.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.Run(new MainForm());
        }
    }
}
