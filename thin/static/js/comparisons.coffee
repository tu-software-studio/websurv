$ ->
  comparison_controller =
    current_input: null
    current_input_counter: 0
    current_group: 1
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
        input.id = inputCounter
        inputCounter++
      for span in spans
        span.innerHTML = currentLetters[spanCounter]
        span.parentNode.parentNode.id = spanCounter
        spanCounter++

    set_up_key_listener: ->
      $("body").on "keydown", (e) ->
        if e.which in [37..40] and comparison_controller.current_input
          switch e.which
            when 37
              console.log "left"
              if comparison_controller.current_input_counter > 0
                console.log "Message"
              else
                comparison_controller.current_input_counter -= 1
            when 38
              console.log "up"
              e.preventDefault()
              if comparison_controller.current_input_counter < comparison_controller.current_input[0].value.length
                inputValue = comparison_controller.current_input[0].value
                tableRow = comparison_controller.current_input[0].parentNode.parentNode
                tableRow.children[comparison_controller.current_group].firstChild.value += inputValue[comparison_controller.current_input_counter]
                comparison_controller.current_input_counter += 1

            when 39
              console.log "right"
              if comparison_controller.current_input_counter < comparison_controller.current_input[0].value.length - 1
                tableRow = comparison_controller.current_input[0].parentNode.parentNode
                console.log tableRow.children[comparison_controller.current_group].children
                span = tableRow.children[comparison_controller.current_group].children[1]
                if span.tagName is "SPAN"
                  console.log "new group"
                  td = document.createElement("td")
                  element = document.createElement("input")
                  element.className = "form-control"
                  element.id = "group" + (comparison_controller.current_group + 1)
                  element.disabled = "true"
                  td.appendChild(element)
                  console.log tableRow
                  console.log tableRow.children.length
                  tableRow.insertBefore(td, tableRow.children[tableRow.children.length - 2])
                  tableRow.children[tableRow.children.length - 3].appendChild(span)
                  comparison_controller.current_group += 1
                else
                  comparison_controller.current_input_counter += 1
            when 40
              console.log "down"
              e.preventDefault()
              if comparison_controller.current_input_counter > 0
                inputValue = comparison_controller.current_input[0].value
                tableRow = comparison_controller.current_input[0].parentNode.parentNode
                tableRow.children[comparison_controller.current_group].firstChild.value = tableRow.children[1].firstChild.value[...-1]
                comparison_controller.current_input_counter -= 1
            else
              # Do nothing
          console.log comparison_controller.current_input_counter
          comparison_controller.update_current_cell()

    update_current_cell: ->
      console.log "updating cell"
      inputValue = comparison_controller.current_input[0].value
      tableRow = comparison_controller.current_input[0].parentNode.parentNode
      console.log inputValue[comparison_controller.current_input_counter]
      if inputValue[comparison_controller.current_input_counter] is undefined
        tableRow.children[comparison_controller.current_group].children[1].innerHTML = "&#x2713;"
      else
        tableRow.children[comparison_controller.current_group].children[1].innerHTML = inputValue[comparison_controller.current_input_counter]

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "focus","input.trans-form", (e) ->
        console.log "setting input to: "+ e.target.name
        comparison_controller.current_input = $ e.target
        comparison_controller.current_input.blur ->
          comparison_controller.current_input_counter = 0
          comparison_controller.current_group = 1
          comparison_controller.current_input = null


  comparison_controller.loop_through_spans()
  comparison_controller.set_up_key_listener()
  comparison_controller.set_up_inputs()