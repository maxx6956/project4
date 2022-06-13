document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('.post').forEach(function(button) {
        button.onclick = () => {
            fetch(`/get_post/${button.dataset.postid}`, {
                method: 'PUT',
              })
            .then(
                fetch(`/get_post/${button.dataset.postid}`)
                .then(response => response.json())
                .then(post => {
                    // Print post
                    console.log(post["like"]);
                    button.innerHTML = `ggg: ${post["like"].length}`
                })
            )
        }
    })
})