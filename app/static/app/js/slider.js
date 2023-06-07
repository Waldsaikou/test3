const slider = document.querySelector("#slider");
let sliderSelection = document.querySelectorAll(".slider_selection");
let sliderSelectionLast = sliderSelection[sliderSelection.length -1];

const btnLeft = document.querySelector("#btn-left");
const btnRight = document.querySelector("#btn-right");

slider.insertAdjacentElement('afterbegin' ,sliderSelectionLast);

function Next() {
    let sliderSelectionFirst = document.querySelectorAll(".slider_selection")[0];
    slider.style.marginLeft = "-200%";
    slider.style.transition = "all 0.5s";
    setTimeout(function(){
        slider.style.transition = "none";
        slider.insertAdjacentElement('beforeend', sliderSelectionFirst);
        slider.style.marginLeft = "-100%";
    }, 500);

}
function Prev() {
    let sliderSelection = document.querySelectorAll(".slider_selection");
    let sliderSelectionLast = sliderSelection[sliderSelection.length -1];
    slider.style.marginLeft = "0%";
    slider.style.transition = "all 0.5s";
    setTimeout(function(){
        slider.style.transition = "none";
        slider.insertAdjacentElement('afterbegin' ,sliderSelectionLast);
        slider.style.marginLeft = "-100%";
    }, 500);

}

btnRight.addEventListener('click', function(){
    Next();
});
btnLeft.addEventListener('click', function(){
    Prev();
});

setInterval(function(){
    Next();
}, 5000);

