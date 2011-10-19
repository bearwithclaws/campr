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
        var message = JSON.parse(data);

        if (message.status) {
            bubble = $('#'+message.status.checkin_id+' div.twipsy-inner');
            bubble.hide().html(message.status.message).fadeIn('slow');
        }
        else if (message.checkin) {
            var checkin = message.checkin;
            if (checkin.present) {
                var $checkins = $('#checkins');

                // Only add checkin to page if not already there
                if (!checkins.find('#'+checkin.id).size()) {
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

                // If user logged out from another location!
                if (checkin.id == $('#update-status input[name="checkin_id"]').val()) {
                    // window.location.href($('a.logout').first().attr('href'));
                    $('a.logout').first().attr('href').click();
                }
            }
        }

    });
});
