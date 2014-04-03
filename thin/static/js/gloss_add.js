var count = 1

$( "#add" ).click(function() {
    $("#formrow"+count).clone().attr('id', 'formrow'+(++count)).insertAfter("#formrow"+(count-1))
    $( "#formrow"+count ).find("td")[0].innerHTML=count
    $( "#formrow"+count ).find("form").attr('id', "form"+count)
    submitForm( $("#form"+(count-1)));
});

function submitForm( $form_id ){
    //var $form = $( $form_id );
    alert($form_id)
    $.ajax({
        url: window.glossUrl,
        data: $form_id.serialize(),
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

function textify( $form ){
    var form = document.getElementById("form1").children;
    console.log(form);
    for(var i=1;i<form.length;i++)
    {
	var element = $(form[i]);
	console.log(element[0].value);
	element.replaceWith( $("<div class='form-control'>"+element[0].value+'</div>') );

    }

};

//element.replaceWith($('<lmn id="'+element.attr('id')+'">'+element.html()+'</lmn>'));
