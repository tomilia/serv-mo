jQuery(function($) {

var html = $('html');
var viewport = $(window);
var viewportHeight = viewport.height();


var scroll = $('#section-menu');
var timeout = null;

function menuFreeze() {
if (timeout !== null) {
scrollMenu.removeClass('freeze');
clearTimeout(timeout);
}

timeout = setTimeout(function() {
scrollMenu.addClass('freeze');
}, 2000);
}
scrollMenu.mouseover(menuFreeze);


/* ==========================================================================
   Build the Scroll Menu based on Sections .scroll-item
   ========================================================================== */

var sectionsHeight = {}, viewportheight, i = 0;
var scrollItem = $('.scroll-item');
var bannerHeight;

function sectionListen() {
viewportHeight = viewport.height();
bannerHeight = (viewportHeight);
$('.section').addClass('resize').css('height', bannerHeight);
scrollItem.each(function(){
sectionsHeight[this.title] = $(this).offset().top;
});
}
sectionListen();
viewport.resize(sectionListen);
viewport.bind('orientationchange', function() {
sectionListen();
});

var count = 0;

scrollItem.each(function(){
var anchor = $(this).attr('id');
var title = $(this).attr('title');
count ++;
$('#section-menu ul').append('<li><a id="nav_' + title + '" href="#' + anchor + '"><span>' + count + '</span> ' + title + '</a></li>');
});
function menuListen() {
var pos = $(this).scrollTop();
pos = pos + viewportHeight * 0.625;
for(i in sectionsHeight){
if(sectionsHeight[i] < pos) {
$('#section-menu a').removeClass('active');
$('#section-menu a#nav_' + i).addClass('active');;
var newHash = '#' + $('.scroll-item[title="' + i + '"]').attr('id');
if(history.pushState) {
    history.pushState(null, null, newHash);
} else {
    location.hash = newHash;
}
} else {
$('#section-menu a#nav_' + i).removeClass('active');
if (pos < viewportHeight - 72) {
history.pushState(null, null, ' ');
}
}
}
}
scrollMenu.css('margin-top', scrollMenu.height() / 2 * -1);

/* ==========================================================================
   Smooth Scroll for Anchor Links and URL refresh
   ========================================================================== */

scrollMenu.find('a').click(function() {
var href = $.attr(this, 'href');
$('html').animate({
scrollTop: $(href).offset().top
}, 500, function() {
window.location.hash = href;
});
return false;
});


/* ==========================================================================
   Fire functions on Scroll Event
   ========================================================================== */


function scrollHandler() {
menuListen();
menuFreeze();
}
scrollHandler();
viewport.on('scroll', function() {
scrollHandler();
//window.request<a href="https://www.jqueryscript.net/animation/">Animation</a>Frame(scrollHandler);
});
});
