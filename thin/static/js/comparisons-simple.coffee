csrfSafeMethod = (method) ->
    # these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
#sameOrigin = (url) ->
#    # test that a given url is a same-origin URL
#    # url could be relative or scheme relative or absolute
#    host = document.location.host; # host + port
#    protocol = document.location.protocol;
#    sr_origin = '//' + host;
#    origin = protocol + sr_origin;
#    # Allow absolute or scheme relative URLs to same origin
#    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
#        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
#        #or any other URL that isn't scheme relative or absolute i.e relative.
#        !(/^(\/\/|http:|https:).*/.test(url))
clicked_button = null
$ ->
  $.ajaxSetup({
    crossDomain: false
    beforeSend: (xhr, settings) ->
      if !csrfSafeMethod(settings.type)
        # Send the token to same-origin, relative URLs only.
        # Send the token only if the method warrants CSRF protection
        # Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
  })
  $("button[type='submit']").click (e) ->
    clicked_button = $(e.target)
    clicked_button.attr('disabled', 'disabled')
    clicked_button.text("Saving...")
    row = clicked_button.parent().parent()
    inputs = row.find('input')
    save_entry(row.attr('id'), inputs)
  $("tr input").change (e) ->
    button = $(e.target).parents('tr').find('button')
    button.text("Save")
    button.removeAttr('disabled')
  csrftoken = $.cookie('csrftoken')

save_entry = (trans_id, inputs) ->
  console.log "saving entry..."
  data = inputs.serialize()
  data += "&trans_id=" + trans_id
  $.ajax({
      #url: ""
      data: data
      dataType: "json"
      type: "POST"
      success: (data, jqXHR) ->
        clicked_button.text('Saved')
        clicked_button = null
        return true
      error: (response) ->
        clicked_button = null
        console.log("ERROR RESPONSE: " + response.responseText)
        x = JSON.parse(response.responseText)
        $("#messages").append("<div class='alert alert-danger alert-dismissable'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>Error!</div>")
        return false;
  })