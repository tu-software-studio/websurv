$ ->
  h1 = Array(10).join('#')
  comparison_controller =
    current_input_counter: 0
    current_group: 1
    current_row: null
    id_counter: 0
    align_form_counter: 0

    set_up_key_listener: ->
      $("body").on "keydown", (e) ->
        if e.which in [37..40] # Reordered conditions for short-circuiting
          switch e.which
            when 37
              console.log "#{h1}left#{h1}"
              comparison_controller.updateSpan(aligned_form, comparison_controller.current_input_counter, "left")
            when 38
              console.log "#{h1}up#{h1}"
              e.preventDefault()
            when 39
              console.log "#{h1}right#{h1}"
            when 40
              console.log "#{h1}down#{h1}"
              e.preventDefault()

    loop_through_aligned_forms: ->
      aligned_forms = $ "td.aligned-form"
      transcriptions = $ "td.transcriptions"
      for transcription in transcriptions
        transcription = $ transcription
        rowId = transcription.parent().attr("id")
        for letter in transcription.text()
          letter = $ letter
          s=$("<span>").html(letter.selector)
          console.log letter
          $("tr##{rowId}").children("td.aligned-form").append(s)

    set_up_inputs: ->
      console.log "Adding listeners to inputs for comparison entries..."
      $("body").on "click", "tr.trans-form", (e) ->
        console.log e.target
        comparison_controller.current_row = e.target;

    add_ids_to_rows: ->
      rows = $ ".trans-form"
      for row in rows
        row = $ row
        row.attr("id", "#{comparison_controller.id_counter}")
        comparison_controller.id_counter++

    updateSpan: (aligned_form, index, direction) ->
      return

  comparison_controller.add_ids_to_rows()
  comparison_controller.loop_through_aligned_forms()
  comparison_controller.set_up_key_listener()
  comparison_controller.set_up_inputs()
