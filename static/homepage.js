var slideIndex = 1;

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

let showSlides;

document.addEventListener('DOMContentLoaded', e => {

    showSlides = function(n) {
        var i;
        var slides = document.getElementsByClassName("photo");
        var dots = document.getElementsByClassName("dot");
        if (n > slides.length) { slideIndex = 1 }
        if (n < 1) { slideIndex = slides.length }
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }
        slides[slideIndex - 1].style.display = "block";
        dots[slideIndex - 1].className += " active";
    };

    showSlides(slideIndex);

    const sliding_interval = 3000;
    setInterval(() => plusSlides(1), sliding_interval);


    /* scroll to fade-in effect: */
    const fade_in_elements = [...document.querySelectorAll("section#visions-and-culture > *")];
    if (window.IntersectionObserver) { // 针对有探测功能的新版本浏览器：
        fade_in_elements.forEach(e => e.classList.remove("for-internet-explorer"));
        const intersectionObserver = new IntersectionObserver(entries => {
            console.log(entries);
            // if (entries[0].isIntersecting) {
            console.log(`此刻的交叉比例为：${entries[0].intersectionRatio}`);
            if (entries[0].intersectionRatio > 0.7) {
                console.log("完全进入视线框。");
                fade_in_elements.forEach(elm => elm.classList.add("fade-in-view"));
            }
            else {
                fade_in_elements.forEach(elm => elm.classList.remove("fade-in-view"));
            }
        }, {
            threshold: [0.7]
        });
        // const anchor_elm = document.querySelector("section#visions-and-culture > p:last-child");
        const anchor_elm = document.querySelector("section#visions-and-culture");
        intersectionObserver.observe(anchor_elm);
    }
    else { // 针对老版本的IE, 没有测探交叉功能的:
        fade_in_elements.forEach(elm => elm.classList.add("fade-in-view"));
    }

    const chat_bot_trigger = document.querySelector("#chat-bot > i");
    chat_bot_trigger.addEventListener("click", e => {
        x0p('Message', '聊天机器人在路上！', 'info');
    });
}, false);
