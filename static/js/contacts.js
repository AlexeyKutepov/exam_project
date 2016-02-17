/**
 * Created by Alexey Kutepov on 12.05.15.
 */

// The pattern for check e-mail
var pattern = /^([a-z0-9_\.-])+@[a-z0-9-]+\.([a-z]{2,4}\.)?[a-z]{2,4}$/i;

/**
 * Checks the email
 * @param input
 */
function checkEmail(input){
    if ($(input).val() == "") {
        $("#divEmail").removeClass("has-error").removeClass("has-success");
        $("#labelErrorEmail").hide();
        $("#btnSend").prop('disabled', false);
    } else if (pattern.test($(input).val())) {
        $("#divEmail").removeClass("has-error").addClass("has-success");
        $("#labelErrorEmail").hide();
        $("#btnSend").prop('disabled', false);
    } else {
        $("#divEmail").addClass("has-error").removeClass("has-success");
        $("#labelErrorEmail").show();
        $("#btnSend").prop('disabled', true);
    }
}

