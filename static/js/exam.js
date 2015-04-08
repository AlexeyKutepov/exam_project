/**
 * Created by alexey on 08.04.15.
 */

$(document).ready(function(){
      var i=3;
     $("#btnAddAnswer").click(function(){
      $('#divAnswer'+(i+1)).html(
          "<div class='input-group'><span class='input-group-addon'><input id='checkboxAnswe" + (i+1) + "' name='isAnswer" + (i+1) + "' type='checkbox'></span><input id='inputAnswer" + (i+1) + "' name='answer" + (i+1) + "' type='text' class='form-control'></div>"
      );
      i++;
      $('#divAnswers').append("<div id='divAnswer" + (i+1) + "' class='row'></div>");
      $("#btnDeleteAnswer").toggleClass('disabled', false);
  });

     $("#btnDeleteAnswer").click(function(){
    	 if(i>1){
             $("#divAnswer"+(i)).html('');
             $("#divAnswer"+(i+1)).html('');
             i--;
             $('#divAnswers').append("<div id='divAnswer" + (i+1) + "' class='row'></div>");
		 }
         if (i == 1) {
             var $this = $(this);
             $this.toggleClass('disabled', true);
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