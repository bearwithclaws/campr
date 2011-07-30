$(function() {
    $('#update-status').submit(function() {
        var form = $(this);
        var status_message = form.find('textarea[name=status]').val();
        $.post(
            form.attr('action'),
            form.serialize(),
            function(response) {
                if (response.success === 'success')
                {
                    $('speech', '.my-status').html(status_message);
                }
            },
            'json'
        );
        return false;
    });
});
