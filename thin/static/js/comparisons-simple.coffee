$ ->
  $("button[type='submit']").click (e) ->
    $(e.target).attr('disabled', 'disabled')
    $(e.target).text("Saving...")
    row = $(e.target).parent().parent()
    inputs = row.find('input')
    save_entry(row.attr('id'), inputs)
  $("tr input").change (e) ->
    button = $(e.target).parents('tr').find('button')
    button.text("Save")
    button.removeAttr('disabled')

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
        $(e.target).parents('tr').find('button').text('Saved')
        return true
      error: (response) ->
        console.log(response.responseText)
        x = JSON.parse(response.responseText)
        $("#messages").append("<div class='alert alert-danger alert-dismissable'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>Error!</div>")
        return false;
  })