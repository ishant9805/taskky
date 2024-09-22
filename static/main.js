// JavaScript to handle opening the modal and setting up the initial task name
document.getElementById('addButton').addEventListener('click', function() {
    var taskName = document.getElementById('taskName').value.trim();

    if (taskName == '') {
        // If the task name is empty, alert the user
        alert('Please enter a task name.');
        document.getElementById('taskName').focus();
    } else {
        // Set the task name in the modal's input field
        document.getElementById('modalTaskName').value = taskName;

        // Show the modal manually using Bootstrap's JavaScript
        var taskModal = new bootstrap.Modal(document.getElementById('taskModal'));
        taskModal.show();
    }
});

// JavaScript to handle saving the task when the 'Save Task' button is clicked
document.getElementById('saveTask').addEventListener('click', function() {
    var taskDescription = document.getElementById('taskDescription').value;
    var taskDueDate = document.getElementById('taskDueDate').value;

    // Close the modal after saving
    var taskModal = bootstrap.Modal.getInstance(document.getElementById('taskModal'));
    taskModal.hide();
});

document.querySelector('.btn-close').addEventListener('click', function() {
    var taskModal = bootstrap.Modal.getInstance(document.getElementById('taskModal'));
    taskModal.hide();
});
document.querySelector('.btn-closer').addEventListener('click', function() {
    var taskModal = bootstrap.Modal.getInstance(document.getElementById('taskModal'));
    taskModal.hide();
});

// Add event listeners to all edit buttons
document.querySelectorAll('.editTask').forEach(button => {
    button.addEventListener('click', () => {
        var taskId = button.getAttribute('data-task-id');
        var taskname = document.getElementById("taskName" + taskId).innerText;;
        var desc = document.getElementById("taskDesc" + taskId).innerText;
        var due = document.getElementById("taskDue" + taskId).innerText;
        // Set the task name in the modal's input field
        document.getElementById('modalTaskName').value = taskname;
        // Set the task desc in the modal's input field
        document.getElementById('taskDescription').value = desc;
        // Set the task due date time in the modal's input field
        document.getElementById('taskDueDate').value = due;
        // Change saveTask text to update Task
        document.getElementById('saveTask').innerText = "Update";

        // Get the form element and update its action attribute
        document.getElementById('taskForm').action = "/edit_task/" + taskId;

        // Show the modal manually using Bootstrap's JavaScript
        var taskModal = new bootstrap.Modal(document.getElementById('taskModal'));
        taskModal.show();
    });
});