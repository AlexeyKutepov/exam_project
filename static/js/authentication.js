/**
 * Created by Kutepov Alexey on 02.04.15.
 */

var isEmail=false, isPass1=false, isPass2=false, isLastName=false, isFirstName=false, isDateOfBirth=false;

// The pattern for check e-mail
var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;


window.onload = function() {
    if (pattern.test($("#inputEmail").val())) {
        isEmail = true;
    }
    if (!$("#inputPassword1").prop("required")) {
        isPass1 = true;
    }
    if (!$("#inputPassword2").prop("required")) {
        isPass2 = true;
    }
    if ($("#inputLastName").val() != "") {
        isLastName = true;
    }
    if ($("#inputFirstName").val() != "") {
        isFirstName = true;
    }
     if ($("#inputDateOfBirth").val() != "") {
        isDateOfBirth = true;
    }

    checkSubmit();
};

/**
 * Image preview
 * @param input
 */
function onPreview(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#impPreview')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

/**
 * Checks the email
 * @param input
 */
function checkEmail(input){
    if (pattern.test($(input).val())) {
        $("#divEmail").removeClass("has-error").addClass("has-success");
        $("#labelErrorEmail").hide();
        isEmail=true;
    } else {
        $("#divEmail").addClass("has-error").removeClass("has-success");
        $("#labelErrorEmail").show();
        isEmail=false;
    }
    checkSubmit();
}

/**
 * Checks the password1
 * @param input
 */
function checkPassword1(input) {
    if (input.value.length < 6) {
        $("#divPassword1").addClass("has-error").removeClass("has-success");
        $("#labelErrorPassword1").show();
        isPass1=false;
    } else {
        $("#divPassword1").removeClass("has-error");
        $("#labelErrorPassword1").hide();
        isPass1=true;
    }
    checkSubmit();
}

/**
 * Checks the password2
 * @param input
 */
function checkPassword2(input) {
    if (input.value != $("#inputPassword1").val()) {
        $("#divPassword2").addClass("has-error").removeClass("has-success");
        $("#labelErrorPassword2").show();
        isPass2=false;
    } else {
        if (input.value.length < 6) {
            $("#divPassword2").addClass("has-error").removeClass("has-success");
            $("#labelErrorPassword2").hide();
            isPass2=false;
        } else {
            $("#divPassword2").removeClass("has-error").addClass("has-success");
            $("#divPassword1").addClass("has-success").removeClass("has-error");
            $("#labelErrorPassword2").hide();
            isPass2 = true;
        }
    }
    checkSubmit();
}

/**
 * Checks the last name
 * @param input
 */
function checkLastName(input) {
    if (input.value == "") {
        $("#divLastName").addClass("has-error").removeClass("has-success");
        isLastName=false;
    } else {
        $("#divLastName").removeClass("has-error").addClass("has-success");
        isLastName=true;
    }
    checkSubmit();
}

/**
 * Checks the first name
 * @param input
 */
function checkFirstName(input) {
    if (input.value == "") {
        $("#divFirstName").addClass("has-error").removeClass("has-success");
        isFirstName=false;
    } else {
        $("#divFirstName").removeClass("has-error").addClass("has-success");
        isFirstName=true;
    }
    checkSubmit();
}

/**
 * Checks the date of birth
 * @param input
 */
function checkDateOfBirth(input) {
    if (input.value == "") {
        $("#divDateOfBirth").addClass("has-error").removeClass("has-success");
        isDateOfBirth=false;
    } else {
        $("#divDateOfBirth").removeClass("has-error").addClass("has-success");
        isDateOfBirth=true;
    }
    checkSubmit();
}


function onChangePasswordClick(input) {
    if (input.value == 0) {
        input.value = 1;
        $("#inputPassword1").prop('required', true);
        $("#inputPassword2").prop('required', true);
        isPass1 = false;
        isPass2 = false;
        input.innerHTML = "Отмена"
    } else {
        input.value = 0;
        $("#inputPassword1").prop('required', false).val('');
        $("#inputPassword2").prop('required', false).val('');
        $("#divPassword1").removeClass("has-error").removeClass("has-success");
        $("#divPassword2").removeClass("has-error").removeClass("has-success");
        $("#labelErrorPassword1").hide();
        $("#labelErrorPassword2").hide();
        isPass1 = true;
        isPass2 = true;
        input.innerHTML = "Изменить пароль"
    }
    checkSubmit();
}


function checkSubmit() {
    if (isEmail && isPass1 && isPass2 && isLastName && isFirstName && isDateOfBirth) {
        $("#btnSubmit").prop('disabled', false);
    } else {
        $("#btnSubmit").prop('disabled', true);
    }
}