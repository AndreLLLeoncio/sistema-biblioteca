$(document).ready(function() {
    // Function to handle click on delete link
    $(document).on('click', '.confirm-delete', function (e) {
      e.preventDefault(); // Prevent the default action
      var deleteUrl = $(this).attr("href"); // Get the delete URL
      $("#confirmDeleteModal").modal('show'); // Show the modal
      $("#confirmDeleteButtonModal").attr("href", deleteUrl); // Set the delete URL as the href of the delete button in the modal
    });
    
    // Function to handle click on confirm delete button in the modal
    $(document).on('click', '#confirmDeleteButtonModal', function () {
      var deleteUrl = $(this).attr("href"); // Get the delete URL from the delete button
      window.location = deleteUrl; // Redirect to the delete URL
    });
  });