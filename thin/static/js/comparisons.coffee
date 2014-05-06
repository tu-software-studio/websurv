$ ->
  h1 = Array(10).join('#')
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
        input = $(input)
        currentLetters[inputCounter] = input.val()[0]
        input.id = inputCounter
        inputCounter++
      for span in spans
        span = $(span)
        span.html(currentLetters[spanCounter])
        span.parent().parent().id = spanCounter
        spanCounter++

    set_up_key_listener: ->
      $("body").on "keydown", (e) ->
        if comparison_controller.current_input and e.which in [37..40] # Reordered conditions for short-circuiting
          switch e.which
            when 37
              console.log "#{h1}left#{h1}"
              if comparison_controller.current_input_counter > 0
                console.log "Message"
              else
                comparison_controller.current_input_counter -= 1
            when 38
              console.log "#{h1}up#{h1}"
#              e.preventDefault()
              if comparison_controller.current_input_counter < comparison_controller.current_input.val().length
                inputValue = comparison_controller.current_input.val()
                tableRow = comparison_controller.current_input.parent().parent()
                tableRow.children()[comparison_controller.current_group].firstChild.value += inputValue[comparison_controller.current_input_counter]
                comparison_controller.current_input_counter += 1

            when 39
              console.log "#{h1}right#{h1}"
              console.log "current_input_counter: #{comparison_controller.current_input_counter}"
              console.log "current_input: #{comparison_controller.current_input.val().length}"
              if comparison_controller.current_input_counter < comparison_controller.current_input.val().length
                tableRow = comparison_controller.current_input.parent().parent()
                console.log tableRow.children().eq(comparison_controller.current_group).children()
                span = tableRow.children().eq(comparison_controller.current_group).children()[1]
                console.log "tagname #{span.tagName}"
                if span.tagName is "SPAN"
                  console.log "new group"
                  td = $('<td>')
                  element = $('<input>')
                  console.log "ppooop"
                  element.addClass("form-control")
#                  element.attr('style', "width: inherit; display: inline;")
                  element.attr('id', 'group' + (comparison_controller.current_group + 1))
                  element.attr('disabled', 'disabled')
                  td.append(element)
                  td.insertBefore(tableRow.children().eq(tableRow.children().length - 2))
#                  element.insertBefore(span)
                  tableRow.children().eq(tableRow.children().length - 3).append(span)
                  comparison_controller.current_group += 1
                else
                  comparison_controller.current_input_counter += 1
            when 40
              console.log "#{h1}down#{h1}"
#              e.preventDefault()
              if comparison_controller.current_input_counter > 0
                inputValue = comparison_controller.current_input.val()
                tableRow = comparison_controller.current_input.parent().parent()
                tableRow.children()[comparison_controller.current_group].firstChild.val(tableRow.children()[1].firstChild.val()[...-1])
                comparison_controller.current_input_counter -= 1
            else
            # Do nothing
          console.log "current_input_counter: #{comparison_controller.current_input_counter}"
          comparison_controller.update_current_cell()

    update_current_cell: ->
      console.log "updating cell"
      inputValue = comparison_controller.current_input.val()
      tableRow = comparison_controller.current_input.parent().parent()
#      console.log inputValue[comparison_controller.current_input_counter]
      if inputValue[comparison_controller.current_input_counter] is undefined
        tableRow.children().eq(comparison_controller.current_group).children().eq(1).html("&#x2713;")
      else
#        console.log tableRow.children()[comparison_controller.current_group]
        tableRow.children().eq(comparison_controller.current_group).children().eq(1).html(inputValue[comparison_controller.current_input_counter])

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "focus", "input.trans-form", (e) ->
        console.log "setting input to: " + e.target.name
        comparison_controller.current_input = $(e.target).first()
        comparison_controller.current_input.blur ->
          comparison_controller.current_input_counter = 0
          comparison_controller.current_group = 1
          comparison_controller.current_input = null


  comparison_controller.loop_through_spans()
  comparison_controller.set_up_key_listener()
  comparison_controller.set_up_inputs()