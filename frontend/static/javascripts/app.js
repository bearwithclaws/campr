$(function() {
    $('#update-status').submit(function() {
        var form = $(this);
        var status_message = form.find('textarea[name=message]').val();
        $.post(
            form.attr('action'),
            form.serialize(),
            function(response) {
                if (response.message) {
                    $('#' + response.checkin.user_id + ' .twipsy-inner').html(response.message);
                }
            },
            'json'
        );
        return false;
    });
});

$(function() {
    var s = new io.Socket(window.location.hostname, {port: 8001, rememberTransport: false});
    s.connect();

    s.addEvent('message', function(data) {
        messages = JSON.parse(data);

        // why doesn't for..in work here?
        for (var i=0; i < messages.length; i++) {
            message = messages[i];
            speech = $('#'+message.fields.checkin+' div.speech');
            speech.hide().html(message.fields.message).fadeIn('slow');
        }
    });
});
