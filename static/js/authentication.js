/**
 * Created by alexey on 02.04.15.
 */

/**
 * Image preview
 * @param input
 */
function onPreview(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#impPreview').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

//$("#inputPicture").change(function(){
//    readURL(this);
//});