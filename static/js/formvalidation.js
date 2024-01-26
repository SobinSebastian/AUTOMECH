



//#################### FORM VALIDATION FOR MODEL VARIANT #############################
document.addEventListener('DOMContentLoaded', function () {
    var myForm = document.querySelector('#myForm');
    var variantNameInput = document.querySelector('#id_variant_name');
    var modelSelect = document.querySelector('#id_model');
    var fuelTypeSelect = document.querySelector('#id_fuel_type');
    var torqueInput = document.querySelector('#id_torque');
    var bhpInput = document.querySelector('#id_bhp');
    var engineInput = document.querySelector('#id_engine');
    var transmissionInput = document.querySelector('#id_transmission');
    var tyreSizeInput = document.querySelector('#id_tyre_size');

    // Add input event listeners for real-time validation
    variantNameInput.addEventListener('input', function () {
        validateVariantName(variantNameInput);
    });

    modelSelect.addEventListener('input', function () {
        validateModel(modelSelect);
    });

    fuelTypeSelect.addEventListener('input', function () {
        validateFuelType(fuelTypeSelect);
    });

    torqueInput.addEventListener('input', function () {
        validateTorque(torqueInput);
    });

    bhpInput.addEventListener('input', function () {
        validateBhp(bhpInput);
    });

    engineInput.addEventListener('input', function () {
        validateEngine(engineInput);
    });

    transmissionInput.addEventListener('input', function () {
        validateTransmission(transmissionInput);
    });

    tyreSizeInput.addEventListener('input', function () {
        validateTyreSize(tyreSizeInput);
    });

    myForm.addEventListener('submit', function (event) {
        // Validate Variant_Name
        if (!validateVariantName(variantNameInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate Model
        if (!validateModel(modelSelect)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate Fuel_Type
        if (!validateFuelType(fuelTypeSelect)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate Torque
        if (!validateTorque(torqueInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate BHP
        if (!validateBhp(bhpInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate Engine
        if (!validateEngine(engineInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate Transmission
        if (!validateTransmission(transmissionInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        // Validate Tyre_Size
        if (!validateTyreSize(tyreSizeInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        myForm.classList.add('was-validated');
    });

    function validateVariantName(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('variant_nameError');

        // Check if the value is empty or doesn't match the pattern
        if (value === '' || !/^[a-zA-Z0-9-]+$/.test(value)) {
            errorContainer.textContent = "Variant Name can only contain letters, numbers, and hyphens.";
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }
    }

    function validateModel(select) {
        var value = select.options[select.selectedIndex].value;
        var errorContainer = document.getElementById('modelError');

        // Check if the value is empty
        if (value === '') {
            errorContainer.textContent = "Please select a Model.";
            select.classList.remove('is-valid');
            select.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            select.classList.remove('is-invalid');
            select.classList.add('is-valid');
            return true;
        }
    }
    

    function validateTorque(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('torqueError');

        // Check if the value is empty or doesn't match the pattern
        if (value === '' || !/^\d+Nm$/.test(value)) {
            errorContainer.textContent = "Torque should be a number ending with 'Nm'.";
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }
    }
    function validateTyreSize(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('tyre_sizeError');
    
        // Check if the value is empty or doesn't match the pattern
        if (value === '' || !/\d{2,3}\/\d{2,3} R\d{1,2}/.test(value)) {
            errorContainer.textContent = "Provide Correct format e.g.: 145/70 R12";
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }
    }
    
    function validateBhp(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('bhpError');
    
        // Check if the value is empty or doesn't match the pattern
        if (value === '' || !/(\d*\.\d+|\d+) Bhp/.test(value)) {
            errorContainer.textContent = "Provide Correct format e.g.: '125 Bhp', '125.5 Bhp'";
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }
    }
    
    function validateEngine(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('engineError');
    
        // Check if the value is empty or doesn't match the pattern
        if (value === '' || !/^\d+(\.\d+)?cc$/.test(value)) {
            errorContainer.textContent = "Engine should be a number or a decimal number ending with 'cc'.";
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            return true;
        }
    }
    function validateTransmission(select) {
        var value = select.options[select.selectedIndex].value;
        var errorContainer = document.getElementById('transmissionError');
    
        // Check if the value is empty
        if (value === '') {
            errorContainer.textContent = "Please select a Transmission.";
            select.classList.remove('is-valid');
            select.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            select.classList.remove('is-invalid');
            select.classList.add('is-valid');
            return true;
        }
    }
    
    function validateFuelType(select) {
        var value = select.options[select.selectedIndex].value;
        var errorContainer = document.getElementById('fuleTypeError');
        // Check if the value is empty
        if (value === '') {
            errorContainer.textContent = "Please select a Fuel Type.";
            select.classList.remove('is-valid');
            select.classList.add('is-invalid');
            return false;
        } else {
            errorContainer.textContent = "";
            select.classList.remove('is-invalid');
            select.classList.add('is-valid');
            return true;
        }
    }
});


