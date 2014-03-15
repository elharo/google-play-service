window.scraperLoadCompleted = false;
var interval = null, previousDocHeight = 0;
interval = setInterval(function () {
    if (previousDocHeight < document.body.scrollHeight) {
        window.scrollTo(0, Math.max(document.documentElement.scrollHeight, document.body.scrollHeight, document.documentElement.clientHeight));
        document.getElementById('show-more-button').click();
        previousDocHeight = document.body.scrollHeight;
    } else {
        clearInterval(interval);
        window.scraperLoadCompleted = true;
    }
}, 3000);