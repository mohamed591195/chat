let socket = new ReconnectingWebSocket(`ws://${location.host}/users/`);

// status that will be sent to indicate if user is online or away
var userStatus = 'online';

socket.onmessage = function (e) {

    let data = JSON.parse(e.data);

    if (data.notification) {
        let notification = data.notification;
   
        unseenNotificationsExists = true;
        loadedNotificationsCount++;

        announceNotification(notification);

        $('.notifications-bill').addClass('notify');
    }

    else if (data.message) {

        let message = data.message;

        let targeted_thread = $(`.thread-row[data-id=${message.thread}]`);

        // status of the message to be sent back, if messaged reached here it means delivered
        var status = "DLV";

        if (targeted_thread.hasClass('selected')) {

            chatLog.append(`
                <div data-id=${message.id} class="chat-message friend">
                    <span class="message-avatar-container">
                        <img src=${message.sender_image} alt="avatar" class="message-avatar">
                    </span>
                    <p class="message-text">${message.text}</p>
                </div>
            `)   

            chatLog.animate({ scrollTop: chatLog.prop('scrollHeight') }, 1000)

            if (!document.hidden) {
                status = "SEN";
            }
            else {
                targeted_thread.addClass('new-message');
            }
            
        } 
        else {
            targeted_thread.addClass('new-message');
        }

        socket.send(JSON.stringify({
            action: 'update-message-status',
            messageId: message.id,
            status,
        }))

    }

    else if (data.message_with_updated_status) {

        let message = data.message_with_updated_status;

        // if the status is sent, it means the response came from our server for a message has just been saved
        if (message.status == "SNT") {

            targeted_message = $(`.chat-message[data-id='']`);

            targeted_message.attr('data-id', `${message.id}`);
        }
        else {
            if (message.status == 'SEN') { $('span.seen-style').empty() }
            targeted_message = $(`.chat-message[data-id="${message.id}"]`);
        }
        
        targeted_message.children('span').html(`${statusSwitcher(message)[message.status]}`)
    }
    
}

function announceNotification(notification) {

    let notificationsList = $('#notifications-list');

    if (notificationsList.text().includes('No Notifications')) {
        notificationsList.empty()
    }

    notificationsList.prepend(
        `<li data-id="${notification.id}"> 
            <a href="${notification.sender_url}"> ${notification.sender} </a> 
            ${notification.content}
        </li>`
    ); 
}


setInterval(function () {
    
    if (socket.readyState == 1) {
        
        socket.send(JSON.stringify({
            action: 'update-user-status',
            userStatus,
        }));
    }
    
}, 15000)

document.addEventListener('visibilitychange', function () {
    switch (document.visibilityState) {
        case 'hidden':
            userStatus = 'away';
            break;
        case 'visible':
            userStatus = 'online';
            break;
    }

})

$('.chat-container').on('click', function (e) {
    
    // if there is a thread with new message and is selected right now 
    let selectedThreadWithNewMsg = $('.thread-row.new-message.selected')

    if (selectedThreadWithNewMsg.length) {

        selectedThreadWithNewMsg.removeClass('new-message');

        socket.send(JSON.stringify({
            action: 'set-latest-messages-seen',
            threadId: selectedThreadWithNewMsg.data('id'),
        }))

    }
})

$('#message-input').on('keyup', e => {
    if (e.keyCode === 13) {
        $('.fa-paper-plane').trigger('click');
    }
})

$('.fa-paper-plane').on('click', () => {

    messageText = $('#message-input').val().trim();
    
    if (!messageText || !selectedThreadId) return;
    
    $('#message-input').val('')

    chatLog.append(`
                <div data-id="" class="chat-message">
                    <span class="message-avatar-container seen-style">
                        <i class="far fa-circle"></i>
                    </span> 
                    <p class="message-text">${messageText}</p>
                </div>
            `)   

    chatLog.animate({ scrollTop: chatLog.prop('scrollHeight') }, 1000)
    
    // we will need to respond from server that message sent
    // so we add sent mark 
    socket.send(JSON.stringify({
        action: 'send-message',
        text: messageText,
        threadId: selectedThreadId,
    }))
})
