<script>
    function validateMakeName(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('makeNameError');

        // Check if the value is empty
        if (value === '') {
            errorContainer.textContent = "Make Name cannot be empty";
        } else if (!/^[a-zA-Z]+$/.test(value)) {
            // Check if the value contains only characters
            errorContainer.textContent = "Make Name should only contain alphabetic characters";
        } else {
            // Reset the error message if the validation passes
            errorContainer.textContent = "";
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var makeNameInput = document.querySelector('#id_Make_Name');
        makeNameInput.addEventListener('input', function () {
            validateMakeName(makeNameInput);
        });

        // Add event listener for submit button click
        var submitButton = document.querySelector('#makeForm button[type="submit"]');
        submitButton.addEventListener('click', function (event) {
            // Validate the input before submitting the form
            validateMakeName(makeNameInput);

            // Prevent form submission if there are validation errors
            if (makeNameInput.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }

            makeNameInput.classList.add('was-validated');
        });
    });
</script>