let start = 0

window.onload = ()=>{
    const message = {
        start: start,
        end: start + 20 
    }
    fetch(`${window.origin}/load_music_view`, {
        method:"POST",
        credentials: "include",
        body: JSON.stringify(message),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then((response)=>{
        if(response.status !== 200){
            console.log("lol")
            return;
        }
        response.json().then((data)=>{
            view(data.data)
        })
    })
}


function view(data){
    const mainBody = document.querySelector(".list_music")
    for(music of data){
        const card = `<div class="music_card">
        <div class="music_card_img">
            <img src="${music.img}">
            <div class="music_card_play">
                <span class="material-icons">play_arrow</span>
            </div>
        </div>
        <div class="music_card_text">
            <div class="card_text_listener">
                <h1>${music.name}</h1>
                <h3>${music.listening}<span class="material-icons">headset</span></h3>
            </div>
            <div class="card_text_info">
                <h3><span class="material-icons">thumb_up</span>${music.like}</h3>
                <h3><span class="material-icons">thumb_down</span>${music.dislike}</h3>
                <h3><span class="material-icons">question_answer</span>0</h3>
            </div>
        </div>
    </div>`
        mainBody.insertAdjacentHTML("beforeEnd", card);
    }    
}
