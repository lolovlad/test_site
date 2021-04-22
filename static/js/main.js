const menu_up = document.querySelector(".header_menu")
const menu_down = document.querySelector(".button_close")


menu_up.addEventListener("click", (e)=>{
    const body_menu = document.querySelector(".menu_back") 
    body_menu.style.display = "flex"
    body_menu.style.opacity = "1"
})

menu_down.addEventListener("click", (e)=>{
    const body_menu = document.querySelector(".menu_back") 
    body_menu.style.opacity = "0"
    body_menu.style.display = "none"
})




const model_wind_button = document.querySelector("#button_model")
const model_wind = document.querySelector("#model")

try {
    model_wind_button.addEventListener("click", (e)=>{
        model_wind.classList.add("model_activ");
    })
    
    model_wind.addEventListener("click", (e)=>{
        if(e.target == model_wind){
            model_wind.classList.remove("model_activ");
        }
    })
  } catch (err) {}



setTimeout(()=>{
    const acc = document.getElementsByClassName("accordion")

    for(let i = 0; acc.length > i; i++){
        acc[i].onclick = function(){
            this.classList.toggle("active")
    
            const panel = this.nextElementSibling
    
            if(panel.style.maxHeight){
                panel.style.maxHeight = null
                panel.style.padding = null
            }else{
                panel.style.padding = "18px"     
                panel.style.maxHeight = panel.scrollHeight + "px"       
            }
        }
    }
}, 1000)
