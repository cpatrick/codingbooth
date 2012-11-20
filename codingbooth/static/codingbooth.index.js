var cb = cb || {};

cb.cur_id = null;

cb.compile_success = function (data, textStatus, jqXHR) {
    cb.cur_id = data.id;
    output = data.output.output;
    cb.output.setValue(output);
};

cb.run_success = function (data, textStatus, jqXHR) {
    output = data.output.output;
    cb.output.setValue(output);
};

$(document).ready(function() {

    // Setup input editor
    cb.editor = ace.edit("code_input");
    cb.editor.setTheme("ace/theme/monokai");
    cb.editor.getSession().setMode("ace/mode/c_cpp");

    // Output "code editor"
    cb.output = ace.edit("code_output");
    cb.output.setTheme("ace/theme/monokai");
    cb.output.getSession().setMode("ace/mode/c_cpp");
    cb.output.setReadOnly(true);
    cb.output.setShowPrintMargin(false);
    cb.output.getSession().setUseWrapMode(true);

    // Setup code if passed into the index template
    if (cb.cur_code) {
        cb.editor.setValue(cb.cur_code);
    }

    // Attach to the compile click
    $('#compile_button').click(function () {

        // Prepare request data
        request_data = {'code': cb.editor.getValue()};
        if (cb.cur_id) {
            request_data.id = cb.cur_id;
        }

        // Send the request
        $.ajax({
          type: 'POST',
          url: '/compile',
          data: request_data,
          success: cb.compile_success
        });

    });

    // Attach to the run click
    $('#run_button').click(function () {

        request_data = {'id': cb.cur_id};
        $.ajax({
          type: 'POST',
          url: '/run',
          data: request_data,
          success: cb.run_success
        });

    });

    // Clear the output editor
    $('#clear_button').click(function () {
        cb.output.setValue("");
    });

});
