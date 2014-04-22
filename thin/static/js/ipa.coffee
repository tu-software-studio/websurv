###
  Created by akeenan on 4/10/14.
###

$ ->
  ipa_controller =
    current_input: null
    set_up_buttons: ->
      console.log "Adding listeners to buttons..."
      button_divs = $ "div.btn-toolbar"
      for button_div in button_divs
        for button in $(button_div).find "button"
          button = $ button
          button.click (e) ->
            if ipa_controller.current_input?
              ipa_controller.current_input.val(ipa_controller.current_input.val() + $.trim(e.target.innerHTML))
              ipa_controller.current_input.focus()
            else
              alert "No input set. Click on an text box to set the input."
    set_up_inputs: ->
      console.log "Adding listeners to inputs..."
      $("body").on "focus","input", (e) ->
        console.log "setting input to: "+ e.target.name
        ipa_controller.current_input = $ e.target
  ipa_controller.set_up_buttons()
  ipa_controller.set_up_inputs()

  $("#ipa-toggle").click (e) ->
    e.preventDefault()
    $("#ipa_buttons").toggle("slide", {direction: "down", duration: 500})
#    $("#ipa_buttons").toggle(500)






