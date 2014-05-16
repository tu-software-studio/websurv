# From Django Docs
csrfSafeMethod = (method) ->
    # these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
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
    # Change button to Saving... and disable it
    clicked_button = $(e.target)
    clicked_button.attr('disabled', 'disabled')
    clicked_button.text("Saving...")

    # Send AJAX request to save
    row = clicked_button.parent().parent()
    inputs = row.find('input')
    save_entry(row.attr('id'), inputs)
  $("tr input").change (e) ->
    # Change button back to Save and enable it
    button = $(e.target).parents('tr').find('button')
    button.text("Save")
    button.removeAttr('disabled')

    # Increment necesarry ones after
    input = $(e.target)
    li = input.parent().parent()
    if parseInt(li.next().find("label input").val()) < parseInt(input.val())
      for num in li.nextAll()
        $num = $(num).find("label input")
        if $num.val() == input.val()
          break
        $num.val(+$num.val()+1)
    prev = li.prev().find("label input")
    if parseInt(prev.val()) > parseInt(input.val())
      input.val(prev.val())
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