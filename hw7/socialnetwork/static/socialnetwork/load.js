function loadPostsOnGlobalPage() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePageOnGlobalPage(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-global", true)
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.send()
}

function loadPostsOnFollowerPage() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return
        updatePageOnFollowerPage(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-follower", true)
    xhr.setRequestHeader("X-CSRFToken", getCSRFToken())
    xhr.send()
}

function updatePageOnGlobalPage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateListOnGlobalPage(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function updatePageOnFollowerPage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateListOnFollowerPage(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function updateListOnGlobalPage(items) {
    // Removes the old to-do list items
    let list = document.getElementById("my-posts-go-here")
    // while (list.hasChildNodes()) {
    //     list.removeChild(list.firstChild)
    // }

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        
        let element = document.createElement("p")
        element.innerHTML = ''
        if (document.getElementById('id_post_div_' + item.id) == null){
            let post_time = new Date(item.creation_time)
            post_time = post_time.toLocaleDateString() + ' ' + post_time.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
            element.innerHTML += '<div id="id_post_div_' + item.id + '">' + 
                                    `Post by <a id="id_post_profile_${item.id}" style="font-family: verdana; font-size: 18px;" href="/other_profile/${item.user_id}">${item.user_firstname + " " + item.user_lastname}</a> - <b id="id_post_text_${item.id}" style="font-size: 18px;">${item.text}</b> - <p id="id_post_date_time_${item.id}" style="font-family: Times; font-size: 18px;">${post_time}</p>` + 
                            '</div>' 
            element.innerHTML += '<div id="my-comments-go-here-for-post-' + item.id + '"></div>'
            element.innerHTML += `
                                <label>Comment:</label>
                                <input id="id_comment_input_text_${item.id}" type="text" name="comment_input_text">
                                <button id="id_comment_button_${item.id}" type="submit" onclick="addCommentsOnGlobalPage(${item.id})">Submit</button>
                                <input type='hidden' name='csrfmiddlewaretoken' value="${getCSRFToken()}" />
                                <input type='hidden' name='post_id' value="${item.id}" />
                            `
            // list.appendChild(element)
            list.insertBefore(element, list.firstChild)
        }

        let comment_list = document.getElementById("my-comments-go-here-for-post-" + item.id)
        for (let j = 0; j < item.comments.length; j++) {
            let comment_element = document.createElement("ul")
            comment_element.innerHTML = ''
            let comment = item.comments[j]
            // if (document.getElementById('id_comment_div_' + comment.id) == null) {
            if (document.getElementById('my-comments-' + comment.id + '-go-here-for-post-' + item.id) == null) {
                // console.log('my-comments-' + comment.id + '-go-here-for-post-' + item.id)
                // console.log(comment.text)
                let comment_time = new Date(comment.creation_time)
                comment_time = comment_time.toLocaleDateString() + ' ' + comment_time.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
                comment_element.innerHTML += '<div id="my-comments-' + comment.id + '-go-here-for-post-' + item.id + '">'
                comment_element.innerHTML += `<div id="id_comment_div_${comment.id}">Comment by <a id="id_comment_profile_${comment.id}" style="font-family: verdana; font-size: 18px;" href="/other_profile/${comment.user_id}">${comment.user_firstname + " " + comment.user_lastname}</a> - <b id="id_comment_text_${comment.id}" style="font-size: 18px; ">${comment.text}</b> - <p id="id_comment_date_time_${comment.id}" style="font-family: Times; font-size: 18px; ">${comment_time}</p></div>`
                comment_element.innerHTML += `</div>`

                // comment_list.appendChild(comment_element)
                comment_list.insertBefore(comment_element, comment_list.firstChild)
            }
        }
    }
}

function updateListOnFollowerPage(items) {
    // Removes the old to-do list items
    let list = document.getElementById("my-posts-go-here")
    // while (list.hasChildNodes()) {
    //     list.removeChild(list.firstChild)
    // }

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        
        let element = document.createElement("p")
        element.innerHTML = ''
        if (document.getElementById('id_post_div_' + item.id) == null){
            let post_time = new Date(item.creation_time)
            post_time = post_time.toLocaleDateString() + ' ' + post_time.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
            element.innerHTML += '<div id="id_post_div_' + item.id + '">' + 
                                    `Post by <a id="id_post_profile_${item.id}" style="font-family: verdana; font-size: 18px;" href="/other_profile/${item.user_id}">${item.user_firstname + " " + item.user_lastname}</a> - <b id="id_post_text_${item.id}" style="font-size: 18px;">${item.text}</b> - <p id="id_post_date_time_${item.id}" style="font-family: Times; font-size: 18px;">${post_time}</p>` + 
                            '</div>' 
            element.innerHTML += '<div id="my-comments-go-here-for-post-' + item.id + '"></div>'
            element.innerHTML += `
                                <label>Comment:</label>
                                <input id="id_comment_input_text_${item.id}" type="text" name="comment_input_text">
                                <button id="id_comment_button_${item.id}" type="submit" onclick="addCommentsOnFollowerPage(${item.id})">Submit</button>
                                <input type='hidden' name='csrfmiddlewaretoken' value="${getCSRFToken()}" />
                                <input type='hidden' name='post_id' value="${item.id}" />
                            `
            // list.appendChild(element)
            list.insertBefore(element, list.firstChild)
        }

        let comment_list = document.getElementById("my-comments-go-here-for-post-" + item.id)
        for (let j = 0; j < item.comments.length; j++) {
            let comment_element = document.createElement("ul")
            comment_element.innerHTML = ''
            let comment = item.comments[j]
            // if (document.getElementById('id_comment_div_' + comment.id) == null) {
            if (document.getElementById('my-comments-' + comment.id + '-go-here-for-post-' + item.id) == null) {
                // console.log('my-comments-' + comment.id + '-go-here-for-post-' + item.id)
                // console.log(comment.text)
                let comment_time = new Date(comment.creation_time)
                comment_time = comment_time.toLocaleDateString() + ' ' + comment_time.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
                comment_element.innerHTML += '<div id="my-comments-' + comment.id + '-go-here-for-post-' + item.id + '">'
                comment_element.innerHTML += `<div id="id_comment_div_${comment.id}">Comment by <a id="id_comment_profile_${comment.id}" style="font-family: verdana; font-size: 18px;" href="/other_profile/${comment.user_id}">${comment.user_firstname + " " + comment.user_lastname}</a> - <b id="id_comment_text_${comment.id}" style="font-size: 18px; ">${comment.text}</b> - <p id="id_comment_date_time_${comment.id}" style="font-family: Times; font-size: 18px; ">${comment_time}</p></div>`
                comment_element.innerHTML += `</div>`

                // comment_list.appendChild(comment_element)
                comment_list.insertBefore(comment_element, comment_list.firstChild)
            }
        }
    }
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function addCommentsOnGlobalPage(id) {
    let itemTextElement = document.getElementById("id_comment_input_text_" + id)
    let itemTextValue   = itemTextElement.value
    // console.log("itemTextValue")
    // console.log(itemTextValue)

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    // displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        console.log(xhr)
        updatePageOnGlobalPage(xhr)
    }

    xhr.open("POST", addCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("post_id="+id+"&comment_text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function addCommentsOnFollowerPage(id) {
    let itemTextElement = document.getElementById("id_comment_input_text_" + id)
    let itemTextValue   = itemTextElement.value
    // console.log("itemTextValue")
    // console.log(itemTextValue)

    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    // displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        console.log(xhr)
        updatePageOnFollowerPage(xhr)
    }

    xhr.open("POST", addCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("post_id="+id+"&comment_text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken()+"&follower=true");
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}