$(function() {
    $('#update-status').submit(function() {
        var form = $(this);
        var status_message = form.find('textarea[name=status]').val();
        $('.speech', '.my-status').html(status_message);
        return false;
        // $.post(
        //     form.attr('action'),
        //     form.serialize(),
        //     function(response) {
        //         if (response.success === 'success') {
        //             $('speech', '.my-status').html(status_message);
        //         }
        //     },
        //     'json'
        // );
        // return false;
    });

    // $('.vote').click(function() {
    //     var link = $(this);
    //     var url_components = link.attr('href').split('?');
    //     $.post(
    //         url_components[0],
    //         url_components[1],
    //         function(response) {
    //             if (response.status === 'success') {
    //                 link.hide();
    //                 link.siblings('.voted').show();
    //             }
    //         },
    //         'json'
    //     );
    //     return 'false';
    // });


    // setTimeout("update_participants()", 3000);
});


// function update_participants() {
//     var event_id = '1001';
//     $.get(
//         '/api/event/'+event_id+'/messages',
//         function(response) {
//             if (typeof response.statuses == 'Object') {
//                 for (statu in response.statuses) {
//                     $('#' + statu.user.username + ' .message').html(statu.message);
//                 }
//             }
//         },
//         'json',
//     );
// }
