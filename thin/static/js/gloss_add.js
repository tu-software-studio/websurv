var count = 1

$("#add").click(function () {
    x = submitForm($("#form" + (count)));
});

function submitForm($form_id) {
    $.ajax({
        url: window.glossUrl,
        data: $form_id.serialize(),
        dataType: "json",
        type: "POST",
        success: function (data, jqXHR) {
            newForm();
            textify($("#form" + (count - 1)));
            return true;
        },
        error: function (response) {
            console.log(response.responseText);
            x = JSON.parse(response.responseText);
            if (x.primary) {
                $("#messages").append("<div class='alert alert-danger alert-dismissable' ><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button> Primary field cannot be empty!</div>")
            }
            if (x.part_of_speech) {
                $("#messages").append("<div class='alert alert-danger alert-dismissable' ><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button> Part of speech field cannot be empty!</div>")
            }
            return false;
        }
    });
}

function newForm() {
    $("#formrow" + count).clone().attr('id', 'formrow' + (++count)).insertAfter("#formrow" + (count - 1));
    frow = $("#formrow" + count);
    frow.find("#rownum").html(count);
    frow.find("input")[1].value = "";
    frow.find("input")[2].value = "";
    frow.find("form").attr('id', "form" + count);
};

function textify($form) {
    var form = document.getElementById("form" + (count - 1)).children;
    console.log(form);
    for (var i = 1; i < form.length; i++) {
        var element = $(form[i].childNodes[1]);
        console.log(element);
        element[0].style.outline = "none";
        element[0].readOnly = true;
        element[0].disabled = "disabled";

    }

};

window.onunload = function () {
    submitForm($("#form" + (count)));
}


