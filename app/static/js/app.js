var myCustomScrollbar = document.querySelector('.my-custom-scrollbar');
Ps.initialize(myCustomScrollbar);

var scrollbarY = myCustomScrollbar.querySelector('.ps.ps--active-y>.ps__scrollbar-y-rail');

myCustomScrollbar.onscroll = function() {
  	scrollbarY.style.cssText = `top: ${this.scrollTop}px!important; height: 400px; right: ${-this.scrollLeft}px`;  
}