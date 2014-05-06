$ ->
  h1 = Array(10).join('#')
  comparison_controller =
    current_input: null
    current_input_counter: 0
    current_group: 1
    current_row: null
    align_form_counter: 0
    loop_through_spans: ->
      console.log("Grabbing all first letters...")
      inputs = $ "div.trans-form"
      spans = $ "span.current"
      currentLetters = []
      inputCounter = 1
      spanCounter = 1
      inputs[0].autofocus = true
      for input in inputs
        input = $(input)
        currentLetters[inputCounter] = input.html()[0]
        input.attr('id', inputCounter)
        inputCounter++
      for span in spans
        span = $(span)
        span.html(currentLetters[spanCounter])
        span.parent().parent().attr('id', spanCounter)
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
              if comparison_controller.current_input_counter < comparison_controller.current_input.html().length
                inputValue = comparison_controller.current_input.html()
                tableRow = comparison_controller.current_input.parent().parent()
#                tableRow.children()[comparison_controller.current_group].firstChild.value += inputValue[comparison_controller.current_input_counter]
                console.log "row_children:"
                console.log tableRow.children().eq(1).children()[comparison_controller.current_group]
                console.log comparison_controller.current_group
#                tableRow.children().eq(1).children()[comparison_controller.current_group-1].value += inputValue[comparison_controller.current_input_counter]
                $("#group#{comparison_controller.current_group}")[0].value += inputValue[comparison_controller.current_input_counter]
                comparison_controller.current_input_counter += 1

            when 39
              console.log "#{h1}right#{h1}"
              console.log "current_input_counter: #{comparison_controller.current_input_counter}"
              console.log "current_input: #{comparison_controller.current_input.html().length}"
              console.log "current_group: #{comparison_controller.current_group}"
              if comparison_controller.current_input_counter < comparison_controller.current_input.html().length
                tableRow = comparison_controller.current_input.parent().parent()
                console.log tableRow.children().eq(1).children()[comparison_controller.current_group]
                console.log
                span = tableRow.children().eq(1).children()[comparison_controller.current_group]
                console.log "tagname: #{span.tagName}"
                if span.tagName is "SPAN"
                  console.log "new group"
                  td = $('<td>')
                  element = $('<input>')
                  element.addClass("form-control")
                  element.attr('style', "width: inherit; display: inline-block;")
                  element.attr('id', 'group' + (comparison_controller.current_group + 1))
                  element.attr('disabled', 'disabled')
#                  td.append(element)
#                  td.insertBefore(tableRow.children().eq(tableRow.children().length - 2))
                  element.insertBefore(span)
                  tableRow.children().eq(tableRow.children().length - 3).append(span)
                  comparison_controller.current_group += 1
                else
                  comparison_controller.current_input_counter += 1
            when 40
              console.log "#{h1}down#{h1}"
#              e.preventDefault()
              if comparison_controller.current_input_counter > 0
                inputValue = comparison_controller.current_input.html()
                tableRow = comparison_controller.current_input.parent().parent()
                tableRow.children()[comparison_controller.current_group].firstChild.val(tableRow.children()[1].firstChild.val()[...-1])
                comparison_controller.current_input_counter -= 1
            else
            # Do nothing
          console.log "current_input_counter: #{comparison_controller.current_input_counter}"
          comparison_controller.update_current_cell()

    update_current_cell: ->
      console.log "updating cell"
      inputValue = comparison_controller.current_input.html()
      tableRow = comparison_controller.current_input.parent().parent()
#      console.log inputValue[comparison_controller.current_input_counter]
      if inputValue[comparison_controller.current_input_counter] is undefined
        tableRow.children().eq(1).children().eq(comparison_controller.current_group).html("&#x2713;")
      else
#        console.log tableRow.children()[comparison_controller.current_group]
#        tableRow.children().eq(1).children.eq(comparison_controller.current_group).html(inputValue[comparison_controller.current_input_counter])
        $("##{comparison_controller.current_row}.current").html(inputValue[comparison_controller.current_input_counter])

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "click", "tr.trans-form", (e) ->
        console.log "setting input to: " + e.target.id
        comparison_controller.current_input = $(e.target).first()
        comparison_controller.current_row = comparison_controller.current_input.attr('id')
        $("table tr td").attr('style', 'background-color: #86C67C;')
        comparison_controller.current_input.blur ->
          comparison_controller.current_input_counter = 0
          comparison_controller.current_group = 1
          comparison_controller.current_row = null
          comparison_controller.current_input.unbind('blur')
          comparison_controller.current_input = null


  comparison_controller.loop_through_spans()
  comparison_controller.set_up_key_listener()
  comparison_controller.set_up_inputs()