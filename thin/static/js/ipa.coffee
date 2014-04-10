###
  Created by akeenan on 4/10/14.
###

$ ->
  input_box = $("#ipa_input").eq(0)
  console.log "Adding listeners to buttons..."
  button_divs = $("div.buttons")
  for button_div in button_divs
    for button in $(button_div).find("button")
      button = $(button)
      button.click (e) ->
        input_box.val(input_box.val() + $.trim(e.target.innerHTML))
        input_box.focus()