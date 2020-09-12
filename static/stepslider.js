//Global Variables
let text = "";
let sentences = [];
let currentSlideIndex = 0; 

//DOM Elements 
const recipe = document.querySelector("#recipe-input");
const backBtn = document.querySelector("#back-btn");
const nextBtn = document.querySelector("#next-btn");
const display = document.querySelector("#slide");
const progress = document.querySelector("#progress");
const h1 = display.childNodes[0];
const h1progress = progress.childNodes[0];

//Store recipe into the text variable 
function storeRecipe (x) {
  // text = recipe.value;
  text = x
};

//Separate each sentence and store in array
function separateSentences() {
  let movingIndice = 0;
  for(let i = 0; i < text.length; i++){
    if(text[i] === "."){
      sentences.push(text.slice(movingIndice, i+1));
      movingIndice = i+1;
    }
  }
  h1.textContent = sentences[currentSlideIndex];
  h1progress.textContent = (currentSlideIndex + 1) + " / " + (sentences.length);
};

//Display appropriate sentence based on navigation buttons
function displayStep (){
  backBtn.addEventListener("click", () => {
    if(currentSlideIndex > 0){
      currentSlideIndex --;
      h1.textContent = sentences[currentSlideIndex];
      h1progress.textContent = (currentSlideIndex + 1) + " / " + (sentences.length);
    }
  });
  nextBtn.addEventListener("click", () => {
    if(currentSlideIndex < sentences.length-1){
      currentSlideIndex ++;
      h1.textContent = sentences[currentSlideIndex];
      h1progress.textContent = (currentSlideIndex + 1) + " / " + (sentences.length);
    }
  });
  h1progress.textContent = (currentSlideIndex + 1) + " / " + (sentences.length);
};

displayStep();