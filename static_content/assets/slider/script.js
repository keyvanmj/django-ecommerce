let thumbnails = document.getElementsByClassName('thumbnails')
let activeimages = document.getElementsByClassName('actives')
for (var i = 0; i < thumbnails.length; i++) {
    thumbnails[i].addEventListener('mouseover', function () {
        console.log(activeimages)

        if (activeimages.length > 0) {
            activeimages[0].classList.remove('actives')
        }
        this.classList.add('actives')
        document.getElementById('featured').src = this.src

    })
}
// let buttonRight = document.getElementById('slideRight');
// let buttonLeft = document.getElementById('slideLeft');
// buttonLeft.addEventListener('click',function () {
//     document.getElementById('slider').scrollLeft-=180
// })
// buttonRight.addEventListener('click',function () {
//     document.getElementById('slider').scrollLeft +=180
//
// })
