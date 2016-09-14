
/* Based on https://css-tricks.com/scaled-proportional-blocks-with-css-and-javascript/ */

var el = document.getElementById("slide-contents");
var elWidth = el.offsetWidth;
var elHeight = el.offsetHeight;
document.body.onresize = doResize;
document.body.onload = doResize;

function doResize(event, ui) {
    var scale;
    scale = Math.min(
        window.innerWidth / elWidth,
        window.innerHeight / elHeight
    )*0.9;
    console.log("Resizing. Element original size is "+elWidth+"x"+elHeight+ ", and the new body size is "+window.innerWidth+"x"+window.innerHeight+". Scale to "+scale);
    el.style.transform = "translate(100%, 100%) " + "scale(" + scale + ")";
}

