<?php
$jsController = "ViewCollections";
include("includes/header.php");
    ?>
        <?php include("includes/partials/search.php"); ?>
        
        <section class="gradientBg">
            <div id="main" role="main" class="wrapper">
                <div class="inner-wrapper">
                    <div class="grid layout-vr-sm">
                        <div class="grid-col grid-size2of3">
                            <h1 class="hdg-bold hdg-a layout-vr-tiny">Veri Composting in Southwest Region</h1>
                            <h2 class="hdg-upper copy">Veri Composting</h2>
                        </div>
                        <div class="grid-col grid-size1of3">
                            <div class="push-top-sm">
                                <div class="featured-ft-videoDetails">
                                    <ul class="h-list h-list-sm h-list-divided copy copy-white">
                                       <li>12 Videos</li>
                                       <li>1:05:00</li>
                                   </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="media layout-vr-md">
                        <div class="video-wrapper">
                            <!-- Implementation Note: include the youtube video id and video uid in the data tag below -->
                            <div id="video-target" data-video-id="cpc_iSun0xA" data-video-uid="432">
                                You need Flash player 8+ and JavaScript enabled to view this video.
                            </div>
                        </div>

                        <div class="bd">
                            <div class="media">
                                <div class="img">
                                    <img src="http://placehold.it/60x60" alt="" />
                                </div>
                                <div class="bd">
                                    <h2 class="copy hdg-bold layout-vr-tiny">ASA</h2>
                                    <p class="copy layout-vr-tiny">Member since 2009</p>
                                    <a class="hdg-bold copy" href="#">50 Collections</a>
                                </div>
                            </div> <!-- End .media -->
                            <h3 class="copy hdg-bold layout-vr-tiny">State, Country</h3>
                            <h3 class="copy layout-vr-md">Language</h3>
                            
                            <!-- Collection Stats -->
                            <div class="collection-stats">
                                <div class="stat-bar-wrapper clearfix js-stat-bar-wrapper">
                                    <div class="icon adopted"></div>
                                    <div class="stat-bar-container">
                                        <!-- <div class="left-value js-left-value"></div> -->
                                        <div class="right-value js-right-value"></div>
                                        <div class="stat-bar js-stat-bar" data-left-value="0" data-right-value="1220">
                                            <div class="stat-indicator js-stat-indicator"></div>
                                        </div>
                                        <div class="right-stat-label">Adopted</div>
                                    </div>
                                </div>

                                <div class="stat-bar-wrapper clearfix js-stat-bar-wrapper">
                                    <div class="icon views"></div>
                                    <div class="stat-bar-container">
                                        <div class="left-value js-left-value"></div>
                                        <div class="right-value js-right-value"></div>
                                        <div class="stat-bar js-stat-bar" data-left-value="4000" data-right-value="1000">
                                            <div class="stat-indicator js-stat-indicator"></div>
                                        </div>
                                        <div class="left-stat-label">Online Views</div>
                                        <div class="right-stat-label">Offline Views</div>
                                    </div>
                                </div>

                                <div class="stat-bar-wrapper clearfix js-stat-bar-wrapper">
                                    <div class="icon likes"></div>
                                    <div class="stat-bar-container">
                                        <div class="left-value js-left-value"></div>
                                        <div class="right-value js-right-value"></div>
                                        <div class="stat-bar js-stat-bar" data-left-value="1750" data-right-value="1520">
                                            <div class="stat-indicator js-stat-indicator"></div>
                                        </div>
                                        <div class="left-stat-label">Online Likes</div>
                                        <div class="right-stat-label">Offline Likes</div>
                                    </div>
                                </div>
                            </div>

                            <div class="layout-vr-sm">
                                <!-- Implementation Note: the data attribute on the button below must be present on page load for like functionality to work -->
                                <a class="btn like-btn js-like-button" data-video-uid="42"><div class="icon"></div><span class="label">Like</span></a>
                            </div>
                            <a class="btn share-btn"><div class="icon"></div>
                                <span class="label">Share</span>

                                <div class="sharethis-wrapper">
                                    <div class='st_facebook_hcount' displayText='Facebook'></div>
                                    <div class='st_twitter_hcount' displayText='Tweet'></div>
                                    <div class='st_linkedin_hcount' displayText='LinkedIn'></div>
                                    <div class='st_email_hcount' displayText='Email'></div>
                                </div>
                            </a>



                        </div> <!-- End .bd -->
                    </div> <!-- End .media -->
                    <div class="boxWhite carousel-pad-rt layout-vr-lg">

                        <!-- Begin video carousel -->
                        <div id="collection-videos-carousel" class="collection-video-carousel carousel-wrapper">
                            <div class="carousel-container js-carousel-container">
                                <ul class="carousel-list">
                                    
                                    <!-- Each carousel slide will be in a li here -->
                                    <?php for ($i = 0; $i < 5; $i++): ?>
                                    <li>
                                        <ul class="h-list h-list-xlg clearfix">
                                            <?php for ($j = 0; $j < 5; $j++): ?>
                                            <!-- The "show-playing" and "show-progress" classes toggle display of the respective overlays -->
                                            <!-- <li class="vidDrawer-video show-playing show-progress js-vidDrawer-video"> -->
                                            <!-- <li class="vidDrawer-video show-playing js-vidDrawer-video"> -->
                                            <li class="vidDrawer-video show-progress js-vidDrawer-video">
                                            <!-- <li class="vidDrawer-video js-vidDrawer-video"> -->
                                                <div class="vidDrawer-image">
                                                    <img src="http://placehold.it/155x95" alt="" />
                                                    <div class="overlay now-playing">
                                                        Now Playing
                                                    </div>
                                                    <div class="overlay progress">
                                                        <div class="progress-inner">
                                                            <span class="amount">48</span>
                                                            <span class="percent">%</span>
                                                            <div class="watched">watched</div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="vidDrawer-flag copy-white">
                                                    5:13
                                                </div>
                                                <div class="vidDrawer-hd copy-dk">
                                                    1. <span class="copy-extra-lt">Video Title</span>
                                                </div>
                                            </li>
                                            <?php endfor; ?>
                                        </ul>
                                    </li>
                                    <?php endfor; ?>
                                    <!-- End carousel slides -->
                                </ul>
                            </div>
                            <div class="arrow-left carousel-previous-slide js-carousel-previous-slide">
                                Previous
                            </div>
                            <div class="arrow-right carousel-next-slide js-carousel-next-slide">
                                Next
                            </div>
                        </div>
                    </div>
                    <div class="layout-vr-lg">
                        <h2 class="hdg-e hdg-black hdg-bold layout-vr-sm">1. Veri Composting in Southwest Region</h2>
                        <p class="copy copy-lt layout-vr-sm">Jan. 10, 2013</p>
                        <p class="copy copy-margin">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas neque orci, lacinia ac adipiscing at, accumsan vitae felis. Vivamus sed leo justo, vitae ultricies dui. Nam iaculis varius purus, eget consequat justo vehicula at. Integer in lorem vitae nisl accumsan malesuada. Phasellus suscipit porttitor leo, at fermentum velit ultricies ut. </p>
                        <h3 class="tag">Tag</h3>
                        <ul class="h-list h-list-sm push-top-tiny">
                            <li><a href="#">Compost,</a></li>
                            <li><a href="#">Agricultural,</a></li>
                            <li><a href="#">Methods,</a></li>
                            <li><a href="#">Veri Composting,</a></li>
                            <li><a href="#">ASA</a></li>
                        </ul>
                    </div>
                </div> <!-- End .inner-wrapper -->
            </div> <!-- End .wrapper -->
        </section>
        
        <section class="wrapper layout-vr-lg">
            <div class="inner-wrapper">
                <div class="grid">
                    <div class="grid-col grid-size2of3">
                        <h2 class="hdg-a hdg-source-lt layout-vr-sm"><span class="js-comment-count"></span> Comments</h2>
                        <div class="commentBox js-comments-feed-wrapper">
                            <div class="commentBox-form">
                                <div class="media commentLeft-border">
                                    <div class="img">
                                        <img src="http://placehold.it/60x60" alt="" />
                                    </div>
                                    <div class="bd">
                                        <form>
                                            <label for="comment" class="text-hide">Comment</label>
                                            <textarea class="comment-text" id="comment"></textarea>
                                            <div class="grid layout-vr-md">
                                                <div class="grid-col">
                                                    <input type="checkbox" id="facebook" />
                                                    <label class="copy" for="facebook">Post to Facebook</label>
                                                </div>
                                                <div class="grid-rt">
                                                    <p class="copy">Posting as Rikin Gandhi (<a href="#">Not you?</a>)</p>
                                                </div>
                                            </div>
                                            <div class="centered">
                                                <input type="submit" value="Add a Comment" class="comment-btn" />
                                            </div>
                                        </form>
                                    </div>
                                </div>
                                <div class="grid layout-vr-md">
                                    <div class="grid-col">
                                        <ul class="h-list key">
                                            <li class="key-offline">Offline</li>
                                            <li class="key-online">Online</li>
                                        </ul>
                                    </div>
                                    <div class="grid-rt">
                                        <a class="hdg-source-semibold hdg-upper" href="#">View All</a>
                                    </div>
                                </div>
                                <ol class="comment-list js-comment-list">
                                <!-- dynamic comments content here -->
                                </ol>
                                <div class="centered">
                                    <a class="btn js-comments-show-more-btn" href="#">Show More</a>
                                </div>
                            </div> <!-- End .commentBox-form -->
                        </div> <!-- End .commentBox -->
                    </div> <!-- End .grid-size2of3 -->
                    <div class="grid-col grid-size1of3">
                        <div class="grid-pad-lt">
                            <h2 class="hdg-a hdg-source-lt layout-vr-sm">Related Videos</h2>
                            <div class="boxPlain">
                                <ul class="v-list-lg">
                                    <li>
                                        <div class="vid-cat-selected">
                                            <div class="vid-cat">
                                                <img src="http://placehold.it/217x124" />
                                                <div class="vid-flag">
                                                    <ul class="copy-sm copy-white h-list h-list-sm h-list-divided">
                                                        <li>12 Videos</li>
                                                        <li>1:20:13</li>
                                                    </ul>
                                                </div>
                                                <div class="vid-cat-inner">
                                                    <div class="vid-cat-hd">
                                                        <h3 class="hdg-green hdg-f hdg-bold">Veri Composting in Southwest Region</h3>
                                                    </div>
                                                    <div class="vid-cat-bd">
                                                        <p class="copy copy-sm layout-vr-tiny">Village X | Language</p>
                                                        <p class="copy copy-sm">By: ASA</p>
                                                    </div>
                                                    <div class="vid-cat-ft">
                                                        <ul class="h-list h-list-sm copy-sm copy-lt vid-cat-list">
                                                            <li class="like"><span class="text-hide">Likes</span> 10,000</li>
                                                            <li class="view"><span class="text-hide">Viewed</span> 6,018</li>
                                                            <li class="check"><span class="text-hide">Adopted</span> 4, 020</li>
                                                        </ul>
                                                    </div>
                                                </div> <!-- End .vid-inner -->
                                            </div> <!-- End .vid-cat -->
                                        </div>
                                    </li>
                                    <li>
                                        <div class="vid-cat-selected">
                                            <div class="vid-cat">
                                                <img src="http://placehold.it/217x124" />
                                                <div class="vid-flag">
                                                    <ul class="copy-sm copy-white h-list h-list-sm h-list-divided">
                                                        <li>12 Videos</li>
                                                        <li>1:20:13</li>
                                                    </ul>
                                                </div>
                                                <div class="vid-cat-inner">
                                                    <div class="vid-cat-hd">
                                                        <h3 class="hdg-green hdg-f hdg-bold">Veri Composting in Southwest Region</h3>
                                                    </div>
                                                    <div class="vid-cat-bd">
                                                        <p class="copy copy-sm layout-vr-tiny">Village X | Language</p>
                                                        <p class="copy copy-sm">By: ASA</p>
                                                    </div>
                                                    <div class="vid-cat-ft">
                                                        <ul class="h-list h-list-sm copy-sm copy-lt vid-cat-list">
                                                            <li class="like"><span class="text-hide">Likes</span> 10,000</li>
                                                            <li class="view"><span class="text-hide">Viewed</span> 6,018</li>
                                                            <li class="check"><span class="text-hide">Adopted</span> 4, 020</li>
                                                        </ul>
                                                    </div>
                                                </div> <!-- End .vid-inner -->
                                            </div> <!-- End .vid-cat -->
                                        </div>
                                    </li>
                                    <li>
                                        <div class="vid-cat-selected">
                                            <div class="vid-cat">
                                                <img src="http://placehold.it/217x124" />
                                                <div class="vid-flag">
                                                    <ul class="copy-sm copy-white h-list h-list-sm h-list-divided">
                                                        <li>12 Videos</li>
                                                        <li>1:20:13</li>
                                                    </ul>
                                                </div>
                                                <div class="vid-cat-inner">
                                                    <div class="vid-cat-hd">
                                                        <h3 class="hdg-green hdg-f hdg-bold">Veri Composting in Southwest Region</h3>
                                                    </div>
                                                    <div class="vid-cat-bd">
                                                        <p class="copy copy-sm layout-vr-tiny">Village X | Language</p>
                                                        <p class="copy copy-sm">By: ASA</p>
                                                    </div>
                                                    <div class="vid-cat-ft">
                                                        <ul class="h-list h-list-sm copy-sm copy-lt vid-cat-list">
                                                            <li class="like"><span class="text-hide">Likes</span> 10,000</li>
                                                            <li class="view"><span class="text-hide">Viewed</span> 6,018</li>
                                                            <li class="check"><span class="text-hide">Adopted</span> 4, 020</li>
                                                        </ul>
                                                    </div>
                                                </div> <!-- End .vid-inner -->
                                            </div> <!-- End .vid-cat -->
                                        </div>
                                    </li>
                                    <li>
                                        <div class="vid-cat-selected">
                                            <div class="vid-cat">
                                                <img src="http://placehold.it/217x124" />
                                                <div class="vid-flag">
                                                    <ul class="copy-sm copy-white h-list h-list-sm h-list-divided">
                                                        <li>12 Videos</li>
                                                        <li>1:20:13</li>
                                                    </ul>
                                                </div>
                                                <div class="vid-cat-inner">
                                                    <div class="vid-cat-hd">
                                                        <h3 class="hdg-green hdg-f hdg-bold">Veri Composting in Southwest Region</h3>
                                                    </div>
                                                    <div class="vid-cat-bd">
                                                        <p class="copy copy-sm layout-vr-tiny">Village X | Language</p>
                                                        <p class="copy copy-sm">By: ASA</p>
                                                    </div>
                                                    <div class="vid-cat-ft">
                                                        <ul class="h-list h-list-sm copy-sm copy-lt vid-cat-list">
                                                            <li class="like"><span class="text-hide">Likes</span> 10,000</li>
                                                            <li class="view"><span class="text-hide">Viewed</span> 6,018</li>
                                                            <li class="check"><span class="text-hide">Adopted</span> 4, 020</li>
                                                        </ul>
                                                    </div>
                                                </div> <!-- End .vid-inner -->
                                            </div> <!-- End .vid-cat -->
                                        </div>
                                    </li>
                                </ul>
                                <div class="centered push-top-md">
                                    <a class="btn" href="#">Show More</a>
                                </div>
                            </div> <!-- End .boxplain -->
                        </div> <!-- End .grid-pad-lt -->
                    </div> <!-- End .grid-size1of3 -->
                </div> <!-- End .grid -->
            </div>
        </section>

<?php
include ("includes/footer.php");
?>
