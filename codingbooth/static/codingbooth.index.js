var cb = cb || {};

cb.cur_id = null;

cb.compile_success = function (data, textStatus, jqXHR) {
    cb.cur_id = data.id;
    output = data.output.output;
    $('#rightside').text(output);
};

cb.run_success = function (data, textStatus, jqXHR) {
    output = data.output.output;
    $('#rightside').text(output);
};

$(document).ready(function() {

    // Attach to the compile click
    $('#compile_button').click(function () {

        // Prepare request data
        request_data = {'code': $('#code_input').val()};

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
});
