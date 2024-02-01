 
 document.addEventListener('DOMContentLoaded', function () {
    var categoryForm = document.querySelector('#categoryForm');
    var categoryNameInput = document.querySelector('#id_category_name');

    categoryForm.addEventListener('submit', function (event) {
        // Validate Category Name
        if (!validateCategoryName(categoryNameInput)) {
            event.preventDefault();
            event.stopPropagation();
        }

        categoryForm.classList.add('was-validated');
    });

    function validateCategoryName(input) {
        var value = input.value.trim();
        var errorContainer = document.getElementById('category_nameError');

        // Check if the value is empty or doesn't match the pattern
        if (value.length <= 3 || !/^[a-zA-Z\s]+$/.test(value)) {
            errorContainer.textContent = "Category name should be alphabetic and have a length greater than 3.";
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
});


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

//server category add form////////////////////////////////////////////////////////////////////////////

var serviceForm = document.querySelector('#serviceForm');
        var serviceNameInput = document.querySelector('#id_service_name');
        var serviceCategorySelect = document.querySelector('#id_service_category');
        var descriptionInput = document.querySelector('#id_description');
        var serviceImageInput = document.querySelector('#id_service_Image');

        serviceForm.addEventListener('submit', function (event) {
            // Validate Service Name
            if (!validateServiceName(serviceNameInput)) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Service Category
            if (!validateServiceCategory(serviceCategorySelect)) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Description
            if (!validateDescription(descriptionInput)) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Service Image
            if (!validateServiceImage(serviceImageInput)) {
                event.preventDefault();
                event.stopPropagation();
            }

            serviceForm.classList.add('was-validated');
        });

        function validateServiceName(input) {
            var value = input.value.trim();
            var errorContainer = document.getElementById('service_nameError');

            // Check if the value is empty
            if (value === '') {
                errorContainer.textContent = "Service name is required.";
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

        function validateServiceCategory(select) {
            var value = select.options[select.selectedIndex].value;
            var errorContainer = document.getElementById('service_categoryError');

            // Check if the value is empty
            if (value === '') {
                errorContainer.textContent = "Please select a service category.";
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

        function validateDescription(input) {
            // You can add validation for the description if needed.
            // This function is currently empty as an example.
            return true;
        }

        function validateServiceImage(input) {
            var value = input.value.trim();
            var errorContainer = document.getElementById('service_ImageError');

            // Check if the value is empty
            if (value === '') {
                errorContainer.textContent = "Please select a service image.";
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

        /// ####################### Service Center Add Form #############################
        var locationForm = document.querySelector('#locationForm');
        var placeInput = document.querySelector('#id_place');
        var cityInput = document.querySelector('#id_city');
        var pincodeInput = document.querySelector('#id_pincode');
        var phoneNumberInput = document.querySelector('#id_phone_number');
        var latitudeInput = document.querySelector('#id_latitude');
        var longitudeInput = document.querySelector('#id_longitude');

        // Add input event listeners for real-time validation
        placeInput.addEventListener('input', function () {
            validateText(placeInput, 'Place');
        });

        cityInput.addEventListener('input', function () {
            validateText(cityInput, 'City');
        });

        pincodeInput.addEventListener('input', function () {
            validatePincode(pincodeInput);
        });

        phoneNumberInput.addEventListener('input', function () {
            validatePhoneNumber(phoneNumberInput);
        });

        latitudeInput.addEventListener('input', function () {
            validateDecimal(latitudeInput, 'Latitude');
        });

        longitudeInput.addEventListener('input', function () {
            validateDecimal(longitudeInput, 'Longitude');
        });

        locationForm.addEventListener('submit', function (event) {
            // Validate Place
            if (!validateText(placeInput, 'Place')) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate City
            if (!validateText(cityInput, 'City')) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Pincode
            if (!validatePincode(pincodeInput)) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Phone Number
            if (!validatePhoneNumber(phoneNumberInput)) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Latitude
            if (!validateDecimal(latitudeInput, 'Latitude')) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Validate Longitude
            if (!validateDecimal(longitudeInput, 'Longitude')) {
                event.preventDefault();
                event.stopPropagation();
            }

            // Perform any additional form submission logic here

            locationForm.classList.add('was-validated');
        });

        function validateText(input, fieldName) {
            var value = input.value.trim();
            var errorContainer = document.getElementById(input.id + 'Error');

            // Check if the value is empty or contains non-alphabetic characters
            if (value === '' || !/^[a-zA-Z\s]+$/.test(value)) {
                errorContainer.textContent = fieldName + ' should contain only alphabetic characters.';
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

        function validatePincode(input) {
            var value = input.value.trim();
            var errorContainer = document.getElementById('pincodeError');

            // Check if the value is empty or not a 6-digit number
            if (value === '' || !/^\d{6}$/.test(value)) {
                errorContainer.textContent = "Pincode should be a 6-digit number.";
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

        function validatePhoneNumber(input) {
            var value = input.value.trim();
            var errorContainer = document.getElementById('phoneNumberError');

            // Check if the value is empty or not a 10-digit number
            if (value === '' || !/^\d{10}$/.test(value)) {
                errorContainer.textContent = "Phone number should be a 10-digit number.";
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

        function validateDecimal(input, fieldName) {
            var value = input.value.trim();
            var errorContainer = document.getElementById(input.id + 'Error');

            // Check if the value is empty or a valid decimal number
            if (value === '' || !/^\d+(\.\d+)?$/.test(value)) {
                errorContainer.textContent = fieldName + ' should be a decimal number.';
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
    });




