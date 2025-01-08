const burger = document.querySelector('.menu');
const fixed = document.querySelector('.fixed');
burger.addEventListener('click', () =>{
    fixed.classList.add("show");
});

fixed.addEventListener("click", (event) => {
    const rect = fixed.getBoundingClientRect();
    const isInTopRightCorner = event.clientX > rect.right - 50 && event.clientY < rect.top + 50;
    if (isInTopRightCorner) {
        fixed.classList.remove("show");
    }
});