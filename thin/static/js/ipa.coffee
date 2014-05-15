###
  Created by akeenan on 4/10/14.
###

finishIPA = ->
  $("#ipa-keyboard").stop(true, true)

showIPA = ->
  $("#ipa-keyboard").show("slide", {direction: "down", duration: 500})

hideIPA = ->
  $("#ipa-keyboard").hide("slide", {direction: "down", duration: 500})

toggleIPA = ->
  $("#ipa-keyboard").toggle("slide", {direction: "down", duration: 500})

$ ->
  ipa_controller =
    current_input: null
    height: 325
    set_up_buttons: ->
#      console.log "Adding listeners to buttons..."
      button_divs = $ "div.btn-toolbar"
      for button_div in button_divs
        for button in $(button_div).find "button"
          button = $ button
          button.addClass("btn-danger")
          button.click (e) ->
            console.log "input: #{ipa_controller.current_input}"
            if ipa_controller.current_input?
              ipa_controller.current_input.val(ipa_controller.current_input.val() + $.trim(e.target.innerHTML).replace(/&nbsp;/g, ""))
              ipa_controller.current_input.focus()
            else
              alert "No input set. Click on an text box to set the input."
    set_up_inputs: ->
#      console.log "Adding listeners to inputs..."
      $("body").on "focusin", "input:text:not([readonly])", (e) ->
        console.log "setting input to: " + e.target.name
        ipa_controller.current_input = $ e.target
#        finishIPA()
#        showIPA()
#      $("body").on "focusout", "input:text", (e) ->
#        ipa_controller.current_input = null
#        finishIPA()
#        hideIPA()
#      $("body").click (e) ->
#        if e.target == $("body")
#          ipa_controller.current_input = null
#          console.log "setting to null"
    set_up_toggler: ->
      $('#ipa-keyboard').css('height', '30px')
      $('#ipa-keys').css('visibility', 'hidden')
      $('#ipa-toggler').click ->
        if $('#ipa-keys').css('visibility') == 'hidden'
          $('#ipa-keys').css('visibility', '')
          $('#ipa-toggler span.caret').switchClass('rotate-180','rotate-0')
          $('#ipa-keyboard').animate({
            height: ipa_controller.height
          })
        else
          ipa_controller.height = $('#ipa-keyboard').height()
          $('#ipa-toggler span.caret').switchClass('rotate-0','rotate-180')
          $('#ipa-keyboard').animate({
            height: '30px'
          }, 400, 'swing', ->
            $('#ipa-keys').css('visibility', 'hidden')
          )
#        hideIPA()
  if not $("body").attr("no-ipa")
    ipa_controller.set_up_buttons()
    ipa_controller.set_up_toggler()
    ipa_controller.set_up_inputs()
  else
    $('#ipa-keyboard').hide()

  $("#ipa-toggle").click (e) ->
    e.preventDefault()
    toggleIPA()