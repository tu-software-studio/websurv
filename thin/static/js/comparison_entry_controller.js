// Generated by CoffeeScript 1.7.1
(function() {
  var comparison_entry_controller,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  $(function() {});

  comparison_entry_controller = {
    current_input: null,
    current_input_counter: 0,
    align_form_counter: 0,
    loop_through_spans: function() {
      var currentLetters, input, inputCounter, inputs, span, spanCounter, spans, _i, _j, _len, _len1, _results;
      console.log("Grabbing all first letters...");
      inputs = $("input.trans-form");
      spans = $("span.current");
      currentLetters = [];
      inputCounter = 0;
      spanCounter = 0;
      inputs[0].autofocus = true;
      for (_i = 0, _len = inputs.length; _i < _len; _i++) {
        input = inputs[_i];
        currentLetters[inputCounter] = input.value[0];
        inputCounter++;
      }
      _results = [];
      for (_j = 0, _len1 = spans.length; _j < _len1; _j++) {
        span = spans[_j];
        span.innerHTML = currentLetters[spanCounter];
        _results.push(spanCounter++);
      }
      return _results;
    },
    check_keys: function() {
      return $("body").on("keydown", function(e) {
        var _ref;
        if ((_ref = e.which, __indexOf.call([37, 38, 39, 40], _ref) >= 0) && comparison_entry_controller.current_input) {
          switch (e.which) {
            case 37:
              console.log("left");
              if (comparison_entry_controller.current_input_counter > 0) {
                comparison_entry_controller.current_input_counter -= 1;
              }
              break;
            case 38:
              console.log("up");
              e.preventDefault();
              break;
            case 39:
              console.log("right");
              if (comparison_entry_controller.current_input_counter < comparison_entry_controller.current_input[0].value.length - 1) {
                comparison_entry_controller.current_input_counter += 1;
              }
              break;
            case 40:
              console.log("down");
              e.preventDefault();
          }
          console.log(comparison_entry_controller.current_input_counter);
          return comparison_entry_controller.update_current_cell();
        }
      });
    },
    update_current_cell: function() {
      var inputValue, tableRow;
      console.log("updating cell");
      inputValue = comparison_entry_controller.current_input[0].value;
      tableRow = comparison_entry_controller.current_input[0].parentNode.parentNode;
      return tableRow.children[1].firstChild.innerHTML = inputValue[comparison_entry_controller.current_input_counter];
    },
    set_up_inputs: function() {
      console.log("Adding listeners to inputs for comparison entries...");
      return $("body").on("focus", "input.trans-form", function(e) {
        console.log("setting input to: " + e.target.name);
        comparison_entry_controller.current_input = $(e.target);
        return comparison_entry_controller.current_input.blur(function() {
          comparison_entry_controller.current_input_counter = 0;
          return comparison_entry_controller.current_input = null;
        });
      });
    }
  };

  comparison_entry_controller.loop_through_spans();

  comparison_entry_controller.check_keys();

  comparison_entry_controller.set_up_inputs();

}).call(this);

//# sourceMappingURL=comparison_entry_controller.map
