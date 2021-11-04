let flash = document.querySelector('#flash');
let tooltipTriggerList = [].slice.call(document.querySelectorAll('.tt'))
let tooltipList = tooltipTriggerList.map(tooltipTriggerEl => {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

flash.onclick = () => {
    let opacity = 1;
    
    let timer = setInterval(() => {
        if (opacity <= 0.1){
            clearInterval(timer);
            flash.style.display = 'none';
        }
        flash.style.opacity = opacity;
        flash.style.filter = `alpha(opacity={opacity * 100})`;
        opacity -= opacity * 0.1;
    }, 10);
}
