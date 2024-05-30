// JavaScript to hide preloader and display content after a delay
window.addEventListener('load', function() {
    // Delay in milliseconds (e.g., 3000 = 3 seconds)
    var delay = 3000;

    setTimeout(function() {
        document.querySelector('.preloader').style.display = 'none';
        document.querySelector('.container').style.display = 'block';
    }, delay);
});
