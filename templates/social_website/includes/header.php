<?php
    if (!isset($jsController)) {
        $jsController = "";
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- META DATA -->
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="MSSmartTagsPreventParsing" content="true" />
        <meta http-equiv="imagetoolbar" content="no" />
        <!--[if IE]><meta http-equiv="cleartype" content="on" /><![endif]-->

        <!-- SEO -->
        <title>Digital Green</title>
        <meta name="description" content="" />
        <meta name="author" content="" />

        <!-- HTML5 SHIV -->
        <!--[if lt IE 9]><script type="text/javascript" src="assets/scripts/html5shiv.js"></script><![endif]-->

        <!-- ICONS -->
        <link rel="shortcut icon" type="image/ico" href="assets/images/favicon.ico" />

        <!-- STYLESHEETS -->
        <link rel="stylesheet" media="screen, projection" href="assets/styles/screen.css" />
        <link rel="stylesheet" media="screen, projection" href="assets/styles/NCarousel.css" />
        <link rel="stylesheet" media="print" href="assets/styles/print.css" />
        <!--[if IE 9]><link rel="stylesheet" type="text/css" media="screen, projection" href="assets/styles/ie9.css" /><![endif]-->
        <!--[if lte IE 8]><link rel="stylesheet" type="text/css" media="screen, projection" href="assets/styles/ie8.css" /><![endif]-->
        <!--[if lte IE 7]><link rel="stylesheet" type="text/css" media="screen, projection" href="assets/styles/ie7.css" /><![endif]-->
    </head>
    <!--
        =======================
        | Implementation Note |
        =======================

        The body needs to have this "data-controller" attribute 
        on it to control which JS controller is loaded.

        Current list includes:
            Home
            About
            Collections
            ViewCollections
            Profile
    -->
    <!-- Implementation Note: the user-id data attribute on the body below must be present on page load for like functionality to work -->
    <body data-controller="<?php echo $jsController; ?>" data-user-id="3442">
        <!-- Begin Main Wrapper -->
        <div class="wrapper-main wrapper">
            <div class="header-wrapper clearfix">
                <header class="global-nav">
                    <a class="skip-to-content" href="#main">Skip to content</a>
                    <div class="wrapper">
                        <nav class="inner-nav" role="navigation">
                            <ul class="nav">
                                <!-- Indicate the current active nav item by adding the "selected" class to a li element below -->
                                <li class="logo"><a href="#">Green Digital</a></li>
                                <li class="nav-pipe nav-size hdg-e selected"><a href="#">Discover <span class="nav-sub hdg-f">great videos</span></a></li>
                                <li class="nav-pipe nav-size hdg-e"><a href="#">Connect <span class="nav-sub hdg-f">with your community</span></a></li>
                                <li class="nav-pipe nav-size hdg-e"><a href="#">Tools <span class="nav-sub hdg-f">lorem ipsum dolor</span></a></li>
                                <li class="nav-pipe nav-size hdg-e"><a href="#">About Us <span class="nav-sub hdg-f">lorem ipsum dolor</span></a></li>
                                <li class="nav-pipe copy copy-dk hdg-upper nav-small"><a href="#">Donate</a></li>
                                <?php
                                if (isset($loggedIn) && $loggedIn):
                                ?>
                                <li><a class="btn-sign-in" href="#">Sign in</a></li>
                                <?php
                                else:
                                ?>
                                <li>
                                    <a class="btn-sign-in btn-signed" href="#">
                                        <div class="media">
                                            <div class="img">
                                                <img src="http://placehold.it/16x16">
                                            </div>
                                            <div class="bd">
                                                Hi, Rikin
                                            </div>
                                        </div>
                                    </a>
                                </li>
                                <?php
                                endif;
                                ?>
                            </ul>
                        </nav> <!-- End .inner-nav -->
                    </div>  <!-- End .wrapper -->
                </header> <!-- End .global-nav -->
            </div>