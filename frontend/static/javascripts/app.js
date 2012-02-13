$(function() {

    var socket = new io.Socket(
            window.location.hostname,
            {port: window.location.port, rememberTransport: false}
        );
    socket.connect();

    $('#update-status').submit(function() {
        var form = $(this);

        // First we post the update...
        $.post(
            form.attr('action'),
            form.serialize(),
            function() {
                // ...and when we know it has successfully been saved
                // to DB, broadcast to other participants.
                socket.send(JSON.stringify({
                    "type":       'update',
                    "message":    form.find('textarea[name=message]').val(),
                    "checkin_id": form.find('input[name=checkin_id]').val()
                }));
            },
            'json'
        );

        return false;
    });

    $('a.logout').click(function() {
        var me = $('li.me');

        socket.send(JSON.stringify({
            "type": 'checkin',
            "checkin": {
                "id": me.attr('id'),
                "present": false
            }
        }));

        me.hide('slow');
    });

    socket.addEvent('connect', function() {
        // Inefficient, but will serve our needs for the time-being...
        if ($('#checkins').size()) {

            var me = $('li.me');
            var username = me.find('.checkin-name a').html().substr(1);  // chop off the leading @

            socket.send(JSON.stringify({
                "type": 'checkin',
                "checkin": {
                    "id": me.attr('id'),
                    "profile_image_url": me.find('img').attr('src'),
                    "username": username,
                    "latest_message": me.find('.twipsy-inner').html(),
                    "present": true
                }
            }));
        }
    });

    socket.addEvent('message', function(data) {
        var message = JSON.parse(data);

        if (message.type == 'update') {
            bubble = $('#'+message.checkin_id+' div.twipsy-inner');
            bubble.hide().html(message.message).fadeIn('slow');
        }
        else if (message.type == 'checkin') {
            var checkin = message.checkin;

            if (checkin.present) {
                var $checkins = $('#checkins');

                // Only add checkin to page if not already there
                if (!$checkins.find('#'+checkin.id).size()) {
                    var $new_checkin = $checkins.find('.checkin').first().clone();
                    $new_checkin.hide();
                    $new_checkin.attr('id', checkin.id);
                    $new_checkin.find('img').attr('src', checkin.profile_image_url);
                    $new_checkin.find('.checkin-name a').attr('href', 'http://twitter.com/'+checkin.username).html('@'+checkin.username);
                    $new_checkin.find('div.twipsy-inner').html(checkin.latest_message);

                    $new_checkin.appendTo($checkins).show('slow');
                }
            }
            else {
                var $checkin = $('#'+checkin.id);
                $checkin.hide('slow', function() { $checkin.remove(); });
            }
        }
    });
});
