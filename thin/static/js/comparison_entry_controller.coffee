$ ->
comparison_entry_controller =
    current_input: null
    current_input_counter: 0
    align_form_counter: 0
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
          switch e.which
            when 37
              console.log "left"
              if comparison_entry_controller.current_input_counter > 0
                comparison_entry_controller.current_input_counter -= 1
            when 38
              console.log "up"
              e.preventDefault()
            when 39
              console.log "right"
              if comparison_entry_controller.current_input_counter < comparison_entry_controller.current_input[0].value.length - 1
                comparison_entry_controller.current_input_counter += 1
            when 40
              console.log "down"
              e.preventDefault()
          console.log comparison_entry_controller.current_input_counter
          comparison_entry_controller.update_current_cell()

    update_current_cell: ->
      console.log "updating cell"
      inputValue = comparison_entry_controller.current_input[0].value
      tableRow = comparison_entry_controller.current_input[0].parentNode.parentNode
      tableRow.children[1].firstChild.innerHTML = inputValue[comparison_entry_controller.current_input_counter]

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "focus","input.trans-form", (e) ->
        console.log "setting input to: "+ e.target.name
        comparison_entry_controller.current_input = $ e.target
        comparison_entry_controller.current_input.blur ->
          comparison_entry_controller.current_input_counter = 0
          comparison_entry_controller.current_input = null


comparison_entry_controller.loop_through_spans()
comparison_entry_controller.check_keys()
comparison_entry_controller.set_up_inputs()