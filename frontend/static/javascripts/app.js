$(function() {
    $('#update-status').submit(function() {
        var form = $(this);
        var status_message = form.find('textarea[name=message]').val();
        $.post(
            form.attr('action'),
            form.serialize(),
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
            bubble = $('#'+message.fields.checkin+' div.twipsy-inner');
            bubble.hide().html(message.fields.message).fadeIn('slow');
        }
    });
});
