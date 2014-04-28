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
      for input in inputs
        currentLetters[inputCounter] = input.value[0]
        inputCounter++
      for span in spans
        span.innerHTML = currentLetters[spanCounter]
        spanCounter++
    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "focus","input", (e) ->
        console.log "setting input to: "+ e.target.name
        comparison_entry_controller.current_input = $ e.target
  comparison_entry_controller.set_up_inputs()
  comparison_entry_controller.loop_through_spans()
  key 'up', -> alert('you pressed up!')