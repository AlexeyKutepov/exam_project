/**
 * Created by alexey on 08.04.15.
 */

$(document).ready(function(){
      var type1=3;
      var type2=3;

     $("#selectType").change(function(){
         switch ($(this).val()) {
             case "1":
                 $("[name='trueAnswer']").prop('type', "checkbox");
                 $("#divAnswersType1").show();
                 $("#divAnswersType2").hide();
                 $("#divAnswersType3").hide();
                 if (type1 == 1) {
                     $("#btnDeleteAnswer").toggleClass('disabled', true);
                 } else {
                     $("#btnDeleteAnswer").toggleClass('disabled', false);
                 }
                 break;
             case "2":
                 $("[name='trueAnswer']").prop('type', "radio");
                 $("#divAnswersType1").hide();
                 $("#divAnswersType2").show();
                 $("#divAnswersType3").hide();
                 if (type2 == 1) {
                     $("#btnDeleteAnswer").toggleClass('disabled', true);
                 } else {
                     $("#btnDeleteAnswer").toggleClass('disabled', false);
                 }
                 break;
         }
     });

     $("#btnAddAnswer").click(function(){
         switch ($("#selectType").val()) {
             case "1":
                 $('#divAnswer'+(type1+1)+'Type1').html(
                      "<div class='input-group'><span class='input-group-addon'><input id='checkboxAnswer" + (type1+1) + "' name='checkboxAnswer" + (type1+1) + "' type='checkbox'></span><input id='inputAnswer" + (type1+1) + "Type1' name='answer" + (type1+1) + "type1' type='text' class='form-control'></div>"
                  );
                 type1++;
                 $('#divAnswersType1').append("<div id='divAnswer" + (type1+1) + "Type1' class='row'></div>");
                 break;
             case "2":
                 $('#divAnswer'+(type2+1)+'Type2').html(
                      "<div class='input-group'><span class='input-group-addon'><input id='radioAnswer" + (type2+1) + "' name='radioAnswer' type='radio'></span><input id='inputAnswer" + (type2+1) + "Type2' name='answer" + (type2+1) + "type2' type='text' class='form-control'></div>"
                  );
                 type2++;
                 $('#divAnswersType2').append("<div id='divAnswer" + (type2+1) + "Type2' class='row'></div>");
                 break;
         }

        $("#btnDeleteAnswer").toggleClass('disabled', false);
     });

     $("#btnDeleteAnswer").click(function(){
         switch ($("#selectType").val()) {
             case "1":
                 if (type1 > 1) {
                     $('#divAnswer' + (type1) + 'Type1').html('');
                     $('#divAnswer' + (type1 + 1) + 'Type1').html('');
                     type1--;
                     $('#divAnswersType1').append("<div id='divAnswer" + (type1 + 1) + "Type1' class='row'></div>");
                 }
                 if (type1 == 1) {
                     $(this).toggleClass('disabled', true);
                 }
                 break;
             case "2":
                 if (type2 > 1) {
                     $('#divAnswer' + (type2) + 'Type2').html('');
                     $('#divAnswer' + (type2 + 1) + 'Type2').html('');
                     type2--;
                     $('#divAnswersType2').append("<div id='divAnswer" + (type2 + 1) + "Type2' class='row'></div>");
                 }
                 if (type2 == 1) {
                     $(this).toggleClass('disabled', true);
                 }
                 break;
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