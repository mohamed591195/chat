var selectedThreadId;

$('.thread-row').on('click', function () {

    // deselecting last active thread
    $('.thread-row.selected').removeClass('selected');
    $(this).addClass('selected');

    $(this).removeClass('new-message')
    
    selectedThreadId = $(this).data('id');
    
    chatLog = $('.chat-log');
    chatLog.empty()

    $.ajax({
        type: 'GET',
        url: 'thread-data/',
        data: {
            id: selectedThreadId,
        },
        success: (data) => {
            generateMessages(data.messages);
        },
        error: () => console.log('error getting messages') 
    })
})


function statusSwitcher(message) {
    return {
        // for now we deal with two users threads so we get the first viewer (it's just one)
        'SEN': `<img src=${message.viewers[0]} alt="avatar" class="message-avatar">`,
        'DLV': `<i class="fas fa-check-circle"></i>`,
        'SNT': `<i class="far fa-check-circle"></i>`,
    }
}

function generateMessages(messages) {

    var lastReceivedMsgIndex;

    messages.forEach((message, i) => {

        if (currentUserId != message.sender) {

            chatLog.append(`
                <div data-id=${message.id} class="chat-message friend">
                    <span class="message-avatar-container">
                        <img src=${message.sender_image} alt="avatar" class="message-avatar">
                    </span>
                    <p class="message-text">${message.text}</p>
                </div>
            `)
            lastReceivedMsgIndex = i
        }
        else {
           
            chatLog.append(`
            <div data-id=${message.id} class="chat-message ">
                <span class="message-avatar-container seen-style">
                </span>  
                <p class="message-text">${message.text}</p>
            </div>
        `)
        }
        
    });

    // check if the last message in thread is not a received one
    lastMsgIndex = messages.length - 1

    if (lastReceivedMsgIndex != lastMsgIndex) {
        // any message sent after the last received one need indication of it's status
        // so we make a new array of them (it's reversed for the purpose of algorithm)
        let newarr = messages.slice(lastReceivedMsgIndex + 1).reverse()
        
        for (i = 0; i < newarr.length; i++) {

            message = newarr[i]
            targeted_message = $(`.chat-message[data-id='${message.id}']`);

            // if the last message is seen then we indicate it by the avatar, no thing more(break loop)
            // the user will know that the upper messages will also be seen ofcourse 
            if (!i && message.status == 'SEN') {
                targeted_message.children('span').html(`${statusSwitcher(message)[message.status]}`)
                
                break;
            }

            // being here means the last sent messsage isn't seen so we 
            // indicate its status untill we find seen message to break the loop without doing any thing to it

            if (message.status !== 'SEN') {
                targeted_message.children('span').html(`${statusSwitcher(message)[message.status]}`)
            } else {
                break;
            }
        }
    }

    chatLog.animate({scrollTop: chatLog.prop('scrollHeight')}, 1000)
} 