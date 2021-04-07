const dragArea = document.querySelector("#dragArea");
let file;
const inputFile = document.querySelector("#input_file") 
let buttonFile = document.querySelector("#button_file")
const buttonSend = document.querySelector("#send")

function showFile(){
    const fileType = file.type;
    const valid = ["image/jpeg", "image/jpg", "image/png"]
    if(valid.includes(fileType)){
        const fileReader = new FileReader();
        fileReader.onload = () => {
            const fileURL = fileReader.result
            const img = `<img src="${fileURL}" alt="">`
            dragArea.innerHTML = img        
        };
        fileReader.readAsDataURL(file);
    }else{
        dragArea.classList.remove("active");
    }
}


function open(){
    inputFile.click();
}

buttonFile.addEventListener("click", open)

inputFile.addEventListener("change", function(){
    file = this.files[0];
    showFile()
    dragArea.classList.remove("active");
});

/*dragArea.addEventListener("dragover", (e)=>{
    e.preventDefault()
    dragArea.classList.add("pulse")
});

dragArea.addEventListener("dragleave", ()=>{
    dragArea.classList.remove("pulse")
})

dragArea.addEventListener("drop", (e)=>{
    e.preventDefault()
    file = e.dataTransfer.files[0];
    dragArea.classList.remove("pulse")
    showFile()
})*/

