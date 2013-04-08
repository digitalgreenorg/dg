<?php
$jsController = "Profile";
$loggedIn = true;
include("includes/header.php");
?>
        <?php include("includes/partials/search.php"); ?>
        
        <div id="main" role="main" class="wrapper">
            <div class="inner-wrapper">
                <div class="media layout-vr-md">
                    <div class="img img-lg">
                        <img src="http://placehold.it/302x222" alt="" />
                    </div>
                    <div class="bd">
                        <div class="grid">
                            <div class="grid-col grid-size2of3">
                                <div class="media">
                                    <div class="img">
                                        <img src="http://placehold.it/61x61" alt="" />
                                    </div>
                                    <div class="bd">
                                        <h1 class="hdg-b hdg-bold push-top-sm">ASA</h1>
                                    </div>
                                </div>
                                <h2 class="copy hdg-bold layout-vr-tiny">State, Country</h2>
                                <h3 class="layout-vr-sm copy">Member since 2009</h3>
                                <p class="copy">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas neque orci, lacinia ac adipiscing at, accumsan vitae felis. Vivamus sed leo justo, vitae ultricies dui. Nam iaculis varius purus, eget consequat justo vehicula at. Integer in lorem vitae nisl accumsan malesuada. Phasellus suscipit porttitor leo.</p>
                            </div>
                            <div class="grid-col grid-size1of3">
                                <div class="borderLt grid-margin-lt-lg">
                                    <ul class="v-list-md stats-list">
                                        <li><a class="hdg-c hdg-bold hdg-lt stats-watch" href="#"><span class="text-hide">Watched</span> 520</a></li>
                                        <li><a class="hdg-c hdg-bold hdg-lt stats-view" href="#"><span class="text-hide">Viewed</span> 1,220</a></li>
                                        <li><a class="hdg-c hdg-bold hdg-lt stats-like" href="#"><span class="text-hide">Liked</span> 500</a></li>
                                        <li><a class="hdg-c hdg-bold hdg-lt stats-adopt" href="#"><span class="text-hide">Adopted</span> 1,750</a></li>
                                        <li><a class="hdg-c hdg-bold hdg-lt stats-award" href="#"><span class="text-hide">Awards</span> 10</a></li>
                                    </ul>
                                </div>
                            </div>
                        </div> <!-- End .grid -->
                    </div> <!-- End .bd -->
                </div> <!-- End .media -->
                <h3 class="hdg-upper hdg-source-semibold hdg-upper hdg-extra-lt hdg-f layout-vr-sm">Farmers</h3>
                <div class="box-list partner-farmers js-partner-farmers-carousel-container">
                    <ul class="js-partner-farmers-pages-container">
                        <!-- dynamic farmer content here-->
                    </ul>
                    <a href="#" class="arrow-left js-prev-partner-farmers-page">Previous</a>
                    <a href="#" class="arrow-right js-next-partner-farmers-page">Next</a>
                </div>
            </div> <!-- End .inner-wrapper -->
        </div> <!-- End .wrapper -->
        
        <div class="gradientBg-profile profile-page sectionBorder-top push-top-lg js-profile-wrapper">
            <div class="wrapper">
                <div class="inner-wrapper">
                    <header class="clearfix layout-vr-lg">
                        <div class="grid-col">
                            <h1 class="hdg-a hdg-source-lt">
                                <span class="js-number-of-collections">
                                    <!-- Dynamic number of collections content here -->
                                </span> 
                                Collections
                            </h1>
                        </div>
                        <div class="grid-rt">
                            <ul class="filterOptions filterOptions-plain hdg-upper copy clearfix">
                                <li><a href="#" class="js-collection-type" data-collection-id="recent"><span>Recently Viewed</span></a></li>
                                <li><a href="#" class="js-collection-type" data-collection-id="completed"><span>Completed Collections</span></a></li>
                            </ul>
                        </div>
                    </header> <!-- End .clearfix -->
                    <div class="js-collections-container">

                        <!-- Dynamic video collections content here -->

                    </div>
                    <div class="centered layout-vr-lg profile-buttons">
                        <a href="#" class="btn js-show-more">Show More</a>
                        <a href="#" class="arrow-up js-hide-collections">Remove</a>
                    </div>
                </div> <!-- End .inner-wrapper -->
            </div> <!-- End .wrapper -->
        </div> <!-- End .homeCollections -->
        
        <section class="wrapper layout-vr-lg">
            <div class="activities-wrapper inner-wrapper">
                <h2 class="hdg-a hdg-source-lt layout-vr-md">Activities</h2>
                <ul class="js-activities-container">
                    
                    <!-- Dynamic activities content here -->

                </ul>
                <div class="timeline-fade"></div>
            </div> <!-- End .inner-wrapper -->

        </section> <!-- End .wrapper -->

<?php
include ("includes/footer.php");
?>