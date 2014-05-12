$ ->
  h1 = Array(10).join('#')
  comparison_controller =
    current_input_counter: 0
    current_group: 0
    current_row: null
    current_label: []
    
    id_counter: 0
    align_form_counter: 0

    set_up_key_listener: ->
      $("body").on "keydown", (e) ->
        if e.which in [37..40] # Reordered conditions for short-circuiting
          switch e.which
            when 37
              console.log "#{h1}left#{h1}"
              rowId = comparison_controller.current_row.id
              if comparison_controller.within_bounds(rowId, 0, parseInt(comparison_controller.current_label[rowId][0])-1)
                comparison_controller.labelify_span(rowId, 0, parseInt(comparison_controller.current_label[rowId][0])-1)
                comparison_controller.current_label[rowId][0]-= 1                
            when 38
              console.log "#{h1}up#{h1}"
              e.preventDefault()
            when 39
              console.log "#{h1}right#{h1}"
              rowId = comparison_controller.current_row.id
              if comparison_controller.within_bounds(rowId, 0, parseInt(comparison_controller.current_label[rowId][0])+1)
                comparison_controller.labelify_span(rowId, 0, parseInt(comparison_controller.current_label[rowId][0])+1)
                comparison_controller.current_label[rowId][0]+= 1                
                
            when 40
              console.log "#{h1}down#{h1}"
              e.preventDefault()

    within_bounds: (row, col, idx) ->
      len = $("##{row}-#{col}").children().length-1
      return idx <= len and idx >= 0
      

    loop_through_aligned_forms: ->
      aligned_forms = $ "td.aligned-form"
      transcriptions = $ "td.transcriptions"
      for transcription in transcriptions
        letterIndex = 0
        transcription = $ transcription
        row = transcription.parent()
        col = row.children("td.aligned-form")
        rowId = transcription.parent().attr("id")
        colId = col.attr("id")[-1..]
        console.log colId
        comparison_controller.current_label[rowId] = []
        comparison_controller.current_label[rowId][0] = 0        
        for letter in transcription.text()
          letter = $ letter
          s=$("<span>").html(letter.selector)
          s.attr("id", "#{rowId}-#{colId}-#{letterIndex}")
          $("tr##{rowId}").children("td.aligned-form").append(s)
          letterIndex++
        comparison_controller.labelify_span(rowId,colId, 0)
      
    labelify_span: (row, col, index) ->
      column = $("##{row}").children("##{row}-#{col}")
      column.children().removeClass()
      column.children("##{row}-#{col}-#{index}").addClass("label label-info")

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "click", "tr.trans-form", (e) ->
        console.log e.target
        comparison_controller.current_row = e.target.parentNode;

    add_ids: ->
      rowCounter = 0
      rows = $ ".trans-form"
      for row in rows
        row = $ row
        comparison_controller.current_label[comparison_controller.id_counter] = comparison_controller.id_counter
        row.attr("id", "#{comparison_controller.id_counter}")
        col = row.children("td.aligned-form")
        col.attr("id", "#{comparison_controller.id_counter}-0")
        comparison_controller.id_counter++

    add_ids_to_column: (column_id) ->
      counter: 0
      column = $ "##{column_number}"
      for span in column
        span = $ span
        span.attr("id", "#{counter}")
        counter++

    updateSpan: (aligned_form, index, direction) ->
      return

  comparison_controller.add_ids()
  comparison_controller.loop_through_aligned_forms()
  comparison_controller.set_up_key_listener()
  comparison_controller.set_up_inputs()
