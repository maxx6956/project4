document.addEventListener('DOMContentLoaded', function(){
    

    document.querySelectorAll('.post').forEach(function(button) {
        button.onclick = () => {
            like(button);
        }
    })

    document.querySelectorAll('.postText').forEach(function(button) {
        button.onclick = () => {
            const text = document.createElement("textarea");
            const div = button.parentNode.childNodes[3]
            curr = div.querySelector("p");
            console.log(div.childNodes)
            text.value = curr.innerHTML;
            text.style.width = "100%";
            //div.innerHTML = "";
            div.querySelector("p").innerHTML = "";

            const save = document.createElement("button")
            save.innerHTML = "Save";
            save.classList.add("btn", "btn-info")
            div.prepend(text)
            div.after(save)
            save.onclick = () => {
                const newText = text.value;
                const p = document.createElement("p");
                p.innerHTML = newText;
                //div.innerHTML = "";
                div.querySelector("p").remove();
                div.querySelector("textarea").remove();
                div.prepend(p);
                save.remove();
            
                fetch(`/get_post/${button.dataset.postid}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        text: newText
                    })
                  })
            }
        }
    })
})

async function like(button) {
    await fetch(`/like_post/${button.dataset.postid}`, {
        method: 'PUT',
      });
    likeCount(button);
}

function likeCount(button){
    fetch(`/like_post/${button.dataset.postid}`)
    .then(response => response.json())
    .then(post => {
        // Print post
        console.log(post["like"]);
        button.innerHTML = `${post["like"].length} Likes`
    })
    button.classList.toggle("btn-light")
    button.classList.toggle("btn-warning")
}