!function(n){"use strict";jQuery(document).on("ready",function(){jQuery(".mean-menu").meanmenu({meanScreenWidth:"991"}),n(window).on("scroll",function(){n(this).scrollTop()>120?n(".navbar-area").addClass("is-sticky"):n(".navbar-area").removeClass("is-sticky")}),n(".close-btn").on("click",function(){n(".search-overlay").fadeOut(),n(".search-btn").show(),n(".close-btn").removeClass("active")}),n(".search-btn").on("click",function(){n(this).hide(),n(".search-overlay").fadeIn(),n(".close-btn").addClass("active")}),n(".popup-youtube").magnificPopup({disableOn:320,type:"iframe",mainClass:"mfp-fade",removalDelay:160,preloader:!1,fixedContentPos:!1}),n(function(){n(".accordion").find(".accordion-title").on("click",function(){n(this).toggleClass("active"),n(this).next().slideToggle("fast"),n(".accordion-content").not(n(this).next()).slideUp("fast"),n(".accordion-title").not(n(this)).removeClass("active")})}),n("select").niceSelect(),setInterval(function(){var e,t,o,a,i,s,l;e=new Date(dateData.endTime),e=Date.parse(e)/1e3,t=new Date,o=e-(t=Date.parse(t)/1e3),a=Math.floor(o/86400),i=Math.floor((o-86400*a)/3600),s=Math.floor((o-86400*a-3600*i)/60),l=Math.floor(o-86400*a-3600*i-60*s),i<"10"&&(i="0"+i),s<"10"&&(s="0"+s),l<"10"&&(l="0"+l),n("#days").html(a+"<span>Days</span>"),n("#hours").html(i+"<span>Hours</span>"),n("#minutes").html(s+"<span>Minutes</span>"),n("#seconds").html(l+"<span>Seconds</span>")},1e3),function(n){n(".tab ul.tabs").addClass("active").find("> li:eq(0)").addClass("current"),n(".tab ul.tabs li a").on("click",function(e){var t=n(this).closest(".tab"),o=n(this).closest("li").index();t.find("ul.tabs > li").removeClass("current"),n(this).closest("li").addClass("current"),t.find(".tab_content").find("div.tabs_item").not("div.tabs_item:eq("+o+")").slideUp(),t.find(".tab_content").find("div.tabs_item:eq("+o+")").slideDown(),e.preventDefault()})}(jQuery),n(".input-counter").each(function(){var n=jQuery(this),e=n.find('input[type="text"]'),t=n.find(".plus-btn"),o=n.find(".minus-btn"),a=e.attr("min"),i=e.attr("max");t.on("click",function(){var t=parseFloat(e.val());if(t>=i)var o=t;else o=t+1;n.find("input").val(o),n.find("input").trigger("change")}),o.on("click",function(){var t=parseFloat(e.val());if(t<=a)var o=t;else o=t-1;n.find("input").val(o),n.find("input").trigger("change")})}),n(function(){n(window).on("scroll",function(){var e=n(window).scrollTop();e>300&&n(".go-top").addClass("active"),e<300&&n(".go-top").removeClass("active")}),n(".go-top").on("click",function(){n("html, body").animate({scrollTop:"0"},500)})})}),n(window).on("load",function(){n(".wow").length&&new WOW({boxClass:"wow",animateClass:"animated",offset:20,mobile:!0,live:!0}).init()}),n(window).on("load",function(){n(".preloader").addClass("preloader-deactivate")});var e=function(n,e){e(".partner-slides").owlCarousel({loop:!0,nav:!1,dots:!1,autoplayHoverPause:!0,autoplay:!0,mouseDrag:!0,margin:30,navText:["<i class='flaticon-arrow-pointing-to-left'></i>","<i class='flaticon-arrow-pointing-to-right'></i>"],responsive:{0:{items:2},576:{items:3},768:{items:4},1200:{items:6}}})};n(window).on("elementor/frontend/init",function(){elementorFrontend.hooks.addAction("frontend/element_ready/partner-logo.default",e)});var t=function(n,e){e(".circlechart").circlechart()};n(window).on("elementor/frontend/init",function(){elementorFrontend.hooks.addAction("frontend/element_ready/funfact-widget.default",t)});var o=function(n,e){e(".feedback-slides").owlCarousel({loop:!0,nav:!1,dots:!1,autoplayHoverPause:!0,autoplay:!0,mouseDrag:!0,margin:30,navText:["<i class='flaticon-arrow-pointing-to-left'></i>","<i class='flaticon-arrow-pointing-to-right'></i>"],responsive:{0:{items:1},576:{items:2},768:{items:2},1200:{items:3}}})};n(window).on("elementor/frontend/init",function(){elementorFrontend.hooks.addAction("frontend/element_ready/feedback-widget.default",o)})}(jQuery);