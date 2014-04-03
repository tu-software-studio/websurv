var count = 1

$( "#add" ).click(function() {
    $( "#form1").clone().attr('id', 'form'+(++count) ).insertAfter("#form1")
    $("#form2").find("tr")[0] = count;
    $("#form2").find("th").remove();
    submitForm("#form1");
});

function submitForm( $form_id ){
    var $form = $( $form_id );
    $.ajax({
        url: window.glossUrl,
        data: $form.serialize(), 
        dataType: "json",
        type: "POST",
        success: function(data, jqXHR){
            alert("success");
	},
	error: function(response) {
	    alert("Error");
	}
    });
}
