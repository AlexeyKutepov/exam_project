/**
 * Created by alexey on 08.04.15.
 */

$(document).ready(function () {
    var i = 3;

    $("#selectType").change(function () {
        switch ($(this).val()) {
            case "1":
                $("[name='trueAnswer']").prop('type', "checkbox");
                $("#divAnswersType3").hide();
                if (i == 1) {
                    $("#btnDeleteAnswer").toggleClass('disabled', true);
                } else {
                    $("#btnDeleteAnswer").toggleClass('disabled', false);
                }
                break;
            case "2":
                $("[name='trueAnswer']").prop('type', "radio");
                $("#divAnswersType3").hide();
                if (i == 1) {
                    $("#btnDeleteAnswer").toggleClass('disabled', true);
                } else {
                    $("#btnDeleteAnswer").toggleClass('disabled', false);
                }
                break;
        }
    });

    $("#btnAddAnswer").click(function () {
        var type;
        switch ($("#selectType").val()) {
            case "1":
                type = 'checkbox';
                break;
            case "2":
                type = 'radio';
                break;
        }

        $('#divAnswer' + (i + 1)).html(
                "<div class='input-group'><span class='input-group-addon'><input id='isTrueAnswer" + (i + 1) + "' name='trueAnswer' type='" + type + "'></span><input id='inputAnswer" + (i + 1) + "' name='answer" + (i + 1) + "' type='text' class='form-control'></div>"
        );
        i++;
        $('#divCloseAnswers').append("<div id='divAnswer" + (i + 1) + "' class='row'></div>");

        $("#btnDeleteAnswer").toggleClass('disabled', false);
    });

    $("#btnDeleteAnswer").click(function () {
        if (i > 1) {
            $('#divAnswer' + i).html('');
            $('#divAnswer' + (i + 1)).html('');
            i--;
            $('#divCloseAnswers').append("<div id='divAnswer" + (i + 1) + "' class='row'></div>");
        }
        if (i == 1) {
            $(this).toggleClass('disabled', true);
        }
    });

});

/**
 * Image preview
 * @param input
 */
function onPreview(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#impPreview').attr('src', e.target.result).width("auto").height("auto");
        };

        reader.readAsDataURL(input.files[0]);
    }
}