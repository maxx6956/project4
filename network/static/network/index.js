document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('.post').forEach(function(button) {
        fetch(`/get_post/${button.dataset.postid}`)
        .then(response => response.json())
        .then(post => {
            // Print post
            console.log(post["like"]);
            button.innerHTML = `ggg: ${post["like"].length}`
        })
    })
    

    document.querySelectorAll('.post').forEach(function(button) {
        button.onclick = () => {
            like(button);
            likeCount(button);
        }
    })

    function like(button) {
        fetch(`/get_post/${button.dataset.postid}`, {
            method: 'PUT',
          })
    }

    function likeCount(button){
        fetch(`/get_post/${button.dataset.postid}`)
        .then(response => response.json())
        .then(post => {
            // Print post
            console.log(post["like"]);
            button.innerHTML = `ggg: ${post["like"].length}`
        })
    }
})