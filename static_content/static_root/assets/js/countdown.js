var timers = setTimeout(function () {
    window.location = '/';
}, 3000);
var countDownDate = new Date(timers).getTime();

var x = setInterval(function () {

    var now = new Date().getTime();

    var distance = countDownDate - now;

    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("demo").innerHTML = seconds + "s ";

    // If the count down is finished, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("demo").innerHTML = "شما در حال انتقال به صفحه ی اصلی هستید";
    }
}, 1000);

