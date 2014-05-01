$ ->
comparison_entry_controller =
    current_input: null
    loop_through_spans: ->
      console.log("Grabbing all first letters...")
      inputs = $ "input.trans-form"
      spans = $ "span.current"
      currentLetters = []
      inputCounter = 0
      spanCounter = 0
      inputs[0].autofocus = true
      for input in inputs
        currentLetters[inputCounter] = input.value[0]
        inputCounter++
      for span in spans
        span.innerHTML = currentLetters[spanCounter]
        spanCounter++
    check_keys: ->
      $("body").on "keydown", (e) ->
        if e.which in [37..40] and comparison_entry_controller.current_input
          e.preventDefault()
          switch e.which
            when 37 then console.log "left"
            when 38 then console.log "up"
            when 39 then console.log "right"
            when 40 then console.log "down"

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "focus","input.trans-form", (e) ->
        console.log "setting input to: "+ e.target.name
        comparison_entry_controller.current_input = $ e.target
        comparison_entry_controller.current_input.blur ->
          comparison_entry_controller.current_input = null


comparison_entry_controller.loop_through_spans()
comparison_entry_controller.set_up_inputs()
comparison_entry_controller.check_keys()
