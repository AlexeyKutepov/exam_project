/**
 * Created by alexey on 08.04.15.
 */

$(document).ready(function () {

    /**
     * Create test page begin
     */

    var i = 3;

    $("#selectType").change(function () {
        switch ($(this).val()) {
            case "1":
                $("[name='trueAnswer']").prop('type', "checkbox");
                $("#isTrueAnswer1").prop( "required", false )
                $('#divCloseAnswer').show();
                $("#divOpenAnswer").hide();
                $("#inputOpenAnswer").prop('required', false);
                $("#inputAnswer1").prop('required', true);
                $("#inputAnswer2").prop('required', true);
                $("#divAddDel").show();
                if (i == 2) {
                    $("#btnDeleteAnswer").toggleClass('disabled', true);
                } else {
                    $("#btnDeleteAnswer").toggleClass('disabled', false);
                }
                break;
            case "2":
                $("[name='trueAnswer']").prop('type', "radio");
                $("#isTrueAnswer1").prop( "required", true );
                $('#divCloseAnswer').show();
                $("#divOpenAnswer").hide();
                $("#inputOpenAnswer").prop('required',false);
                $("#inputAnswer1").prop('required', true);
                $("#inputAnswer2").prop('required', true);
                $("#divAddDel").show();
                if (i == 2) {
                    $("#btnDeleteAnswer").toggleClass('disabled', true);
                } else {
                    $("#btnDeleteAnswer").toggleClass('disabled', false);
                }
                break;
            case "3":
                $("#isTrueAnswer1").prop( "required", false )
                $('#divCloseAnswer').hide();
                $("#divOpenAnswer").show();
                $("#inputOpenAnswer").prop('required',true);
                $("#inputAnswer1").prop('required', false);
                $("#inputAnswer2").prop('required', false);
                $("#divAddDel").hide();
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
                "<div class='input-group'><span class='input-group-addon'><input id='isTrueAnswer" + (i + 1) + "' name='trueAnswer' value='" + (i + 1) + "' type='" + type + "'></span><input id='inputAnswer" + (i + 1) + "' name='answer" + (i + 1) + "' type='text' class='form-control'></div>"
        );
        i++;
        $('#divCloseAnswer').append("<div id='divAnswer" + (i + 1) + "' class='row'></div>");

        $("#btnDeleteAnswer").toggleClass('disabled', false);
    });

    $("#btnDeleteAnswer").click(function () {
        if (i > 2) {
            $('#divAnswer' + i).html('');
            $('#divAnswer' + (i + 1)).html('');
            i--;
            $('#divCloseAnswer').append("<div id='divAnswer" + (i + 1) + "' class='row'></div>");
        }
        if (i == 2) {
            $(this).toggleClass('disabled', true);
        }
    });

    /**
     * Create test page end
     */
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