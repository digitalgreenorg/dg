define("controllers/AboutController",["require","controllers/DigitalGreenPageController","jquery","libs/NCarousel/NCarousel","libs/external/swfobject/swfobject"],function(e){var t=e("controllers/DigitalGreenPageController"),n=e("jquery"),r=e("libs/NCarousel/NCarousel");e("libs/external/swfobject/swfobject");var i=t.extend({constructor:function(e,t){return this.base(e,t),this},_initReferences:function(e,t){this.base(t);var i=this._references;i.$mainCarouselWrapper=n("#main-carousel"),i.mainCarousel=new r(i.$mainCarouselWrapper,{transition:"slide",autoPlay:!0,autoPlayDelay:8e3}),i.$playButton=n(".play-button")},_initEvents:function(){this.base();var e=this._references,t=this._boundFunctions;t.onPlayButtonClick=this._onVideoPlayButtonClick.bind(this),e.$playButton.on("click",t.onPlayButtonClick)},_initVideoPlayer:function(){var e="a4HXqhxkTjo",t={allowScriptAccess:"always"},n={id:"player","class":"main-carousel-video-player"};swfobject.embedSWF("https://www.youtube.com/v/"+e+"?enablejsapi=1&playerapiid=ytplayer&version=3","player","1024","424","8",null,null,t,n),window.onYouTubePlayerReady=this._onYouTubePlayerReady.bind(this),$("#video-img > div").not("#player").each(function(e,t){$(t).hide()}),$("#player").show()},_onYouTubePlayerReady:function(){window.onYouTubePlayerReady=undefined;var e=n("#player").get(0);this._references.videoPlayer=e,window.onYouTubePlayerStateChange=this._onYouTubePlayerStateChange.bind(this),e.addEventListener("onStateChange","onYouTubePlayerStateChange"),e.playVideo()},_onYouTubePlayerStateChange:function(e){e==0&&($("#player").hide(),$("#video-img > div").not("#player").each(function(e,t){$(t).show()}))},_onVideoPlayButtonClick:function(e){this._initVideoPlayer()},destroy:function(){this.base()}});return i});