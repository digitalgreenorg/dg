





<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  <link rel="dns-prefetch" href="https://assets-cdn.github.com">
  <link rel="dns-prefetch" href="https://avatars0.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars1.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars2.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars3.githubusercontent.com">
  <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
  <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">



  <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/frameworks-f27d807afb610bf126cbfb9ce429438a328e012239e5a77fc8152b794553dfc0.css" integrity="sha256-8n2AevthC/Emy/uc5ClDijKOASI55ad/yBUreUVT38A=" media="all" rel="stylesheet" />
  <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github-1d7717dfa90687d65ce00c80ab42271195164d949715783c2c80c9f85595784e.css" integrity="sha256-HXcX36kGh9Zc4AyAq0InEZUWTZSXFXg8LIDJ+FWVeE4=" media="all" rel="stylesheet" />
  
  
  
  

  <meta name="viewport" content="width=device-width">
  
  <title>dg/removal.py at master · digitalgreenorg/dg</title>
  <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
  <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
  <meta property="fb:app_id" content="1401488693436528">

    
    <meta content="https://avatars1.githubusercontent.com/u/1179852?s=400&amp;v=4" property="og:image" /><meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="digitalgreenorg/dg" property="og:title" /><meta content="https://github.com/digitalgreenorg/dg" property="og:url" /><meta content="dg - COCO Analytics Website LOOP Training" property="og:description" />

  <link rel="assets" href="https://assets-cdn.github.com/">
  <link rel="web-socket" href="wss://live.github.com/_sockets/VjI6MjM3NzIyNTY3OmVkYTQzMjg5MTZiODNlMWRhYmFlYzY4ZmE1ODM5MDA0N2IyYTkwZTBkMDhmNzkyZjk5Nzk0ZjUwYzU0MTU5YTA=--7385223b6e73fbff8345953a3bd65b280aaecd9d">
  <meta name="pjax-timeout" content="1000">
  <link rel="sudo-modal" href="/sessions/sudo_modal">
  <meta name="request-id" content="C6DB:295D5:5FE4C37:8F3D6FA:5A54D5FD" data-pjax-transient>
  

  <meta name="selected-link" value="repo_source" data-pjax-transient>

    <meta name="google-site-verification" content="KT5gs8h0wvaagLKAVWq8bbeNwnZZK1r1XQysX3xurLU">
  <meta name="google-site-verification" content="ZzhVyEFwb7w3e0-uOTltm8Jsck2F5StVihD0exw2fsA">
  <meta name="google-site-verification" content="GXs5KoUUkNCoaAZn7wPN-t01Pywp9M3sEjnt_3_ZWPc">
    <meta name="google-analytics" content="UA-3769691-2">

<meta content="collector.githubapp.com" name="octolytics-host" /><meta content="github" name="octolytics-app-id" /><meta content="https://collector.githubapp.com/github-external/browser_event" name="octolytics-event-url" /><meta content="C6DB:295D5:5FE4C37:8F3D6FA:5A54D5FD" name="octolytics-dimension-request_id" /><meta content="sea" name="octolytics-dimension-region_edge" /><meta content="iad" name="octolytics-dimension-region_render" /><meta content="13827569" name="octolytics-actor-id" /><meta content="Divish" name="octolytics-actor-login" /><meta content="0c021f266922bb9a30642930a0a8a82c148835706764373d6991a48bc6f5884d" name="octolytics-actor-hash" />
<meta content="/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show" data-pjax-transient="true" name="analytics-location" />




  <meta class="js-ga-set" name="dimension1" content="Logged In">


  

      <meta name="hostname" content="github.com">
  <meta name="user-login" content="Divish">

      <meta name="expected-hostname" content="github.com">
    <meta name="js-proxy-site-detection-payload" content="Yjc1ZWY0NWJhZDgyZWNhYmQzY2U1YzhhN2FkNDFjYjg1NTkxNDQ2YjdjMjY0ZTUzYTExZWFiMzBmYzA2MTkzMnx7InJlbW90ZV9hZGRyZXNzIjoiMTAzLjc0LjEwOC45OSIsInJlcXVlc3RfaWQiOiJDNkRCOjI5NUQ1OjVGRTRDMzc6OEYzRDZGQTo1QTU0RDVGRCIsInRpbWVzdGFtcCI6MTUxNTUwOTI0NiwiaG9zdCI6ImdpdGh1Yi5jb20ifQ==">

    <meta name="enabled-features" content="UNIVERSE_BANNER,FREE_TRIALS">

  <meta name="html-safe-nonce" content="ce9c4747b9a131b54f15998fe12fb35490670d47">

  <meta http-equiv="x-pjax-version" content="a4f161b0bc9c20ec4e182a798cd97229">
  

      <link href="https://github.com/digitalgreenorg/dg/commits/master.atom" rel="alternate" title="Recent Commits to dg:master" type="application/atom+xml">

  <meta name="description" content="dg - COCO Analytics Website LOOP Training">
  <meta name="go-import" content="github.com/digitalgreenorg/dg git https://github.com/digitalgreenorg/dg.git">

  <meta content="1179852" name="octolytics-dimension-user_id" /><meta content="digitalgreenorg" name="octolytics-dimension-user_login" /><meta content="2742622" name="octolytics-dimension-repository_id" /><meta content="digitalgreenorg/dg" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="2742622" name="octolytics-dimension-repository_network_root_id" /><meta content="digitalgreenorg/dg" name="octolytics-dimension-repository_network_root_nwo" /><meta content="false" name="octolytics-dimension-repository_explore_github_marketplace_ci_cta_shown" />


    <link rel="canonical" href="https://github.com/digitalgreenorg/dg/blob/master/loop_ivr/outliers/removal.py" data-pjax-transient>


  <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">

  <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">

  <link rel="mask-icon" href="https://assets-cdn.github.com/pinned-octocat.svg" color="#000000">
  <link rel="icon" type="image/x-icon" class="js-site-favicon" href="https://assets-cdn.github.com/favicon.ico">

<meta name="theme-color" content="#1e2327">


  <meta name="u2f-support" content="true">

  </head>

  <body class="logged-in env-production page-blob">
    

  <div class="position-relative js-header-wrapper ">
    <a href="#start-of-content" tabindex="1" class="bg-black text-white p-3 show-on-focus js-skip-to-content">Skip to content</a>
    <div id="js-pjax-loader-bar" class="pjax-loader-bar"><div class="progress"></div></div>

    
    
    



        
<header class="Header  f5" role="banner">
  <div class="d-flex px-3 flex-justify-between container-lg">
    <div class="d-flex flex-justify-between">
      <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" data-ga-click="Header, go to dashboard, icon:logo">
  <svg aria-hidden="true" class="octicon octicon-mark-github" height="32" version="1.1" viewBox="0 0 16 16" width="32"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
</a>


    </div>

    <div class="HeaderMenu d-flex flex-justify-between flex-auto">
      <div class="d-flex">
            <div class="">
              <div class="header-search scoped-search site-scoped-search js-site-search" role="search">
  <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/digitalgreenorg/dg/search" class="js-site-search-form" data-scoped-search-url="/digitalgreenorg/dg/search" data-unscoped-search-url="/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <label class="form-control header-search-wrapper js-chromeless-input-container">
        <a href="/digitalgreenorg/dg/blob/master/loop_ivr/outliers/removal.py" class="header-search-scope no-underline">This repository</a>
      <input type="text"
        class="form-control header-search-input js-site-search-focus js-site-search-field is-clearable"
        data-hotkey="s"
        name="q"
        value=""
        placeholder="Search"
        aria-label="Search this repository"
        data-unscoped-placeholder="Search GitHub"
        data-scoped-placeholder="Search"
        autocapitalize="off">
        <input type="hidden" class="js-site-search-type-field" name="type" >
    </label>
</form></div>

            </div>

          <ul class="d-flex pl-2 flex-items-center text-bold list-style-none" role="navigation">
            <li>
              <a href="/pulls" aria-label="Pull requests you created" class="js-selected-navigation-item HeaderNavlink px-2" data-ga-click="Header, click, Nav menu - item:pulls context:user" data-hotkey="g p" data-selected-links="/pulls /pulls/assigned /pulls/mentioned /pulls">
                Pull requests
</a>            </li>
            <li>
              <a href="/issues" aria-label="Issues you created" class="js-selected-navigation-item HeaderNavlink px-2" data-ga-click="Header, click, Nav menu - item:issues context:user" data-hotkey="g i" data-selected-links="/issues /issues/assigned /issues/mentioned /issues">
                Issues
</a>            </li>
                <li>
                  <a href="/marketplace" class="js-selected-navigation-item HeaderNavlink px-2" data-ga-click="Header, click, Nav menu - item:marketplace context:user" data-selected-links=" /marketplace">
                    Marketplace
</a>                </li>
            <li>
              <a href="/explore" class="js-selected-navigation-item HeaderNavlink px-2" data-ga-click="Header, click, Nav menu - item:explore" data-selected-links="/explore /trending /trending/developers /integrations /integrations/feature/code /integrations/feature/collaborate /integrations/feature/ship showcases showcases_search showcases_landing /explore">
                Explore
</a>            </li>
          </ul>
      </div>

      <div class="d-flex">
        
<ul class="user-nav d-flex flex-items-center list-style-none" id="user-links">
  <li class="dropdown js-menu-container">
    <span class="d-inline-block  px-2">
      
    <a href="/notifications" aria-label="You have unread notifications" class="notification-indicator tooltipped tooltipped-s  js-socket-channel js-notification-indicator" data-channel="notification-changed:13827569" data-ga-click="Header, go to notifications, icon:unread" data-hotkey="g n">
        <span class="mail-status unread"></span>
        <svg aria-hidden="true" class="octicon octicon-bell" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 12v1H0v-1l.73-.58c.77-.77.81-2.55 1.19-4.42C2.69 3.23 6 2 6 2c0-.55.45-1 1-1s1 .45 1 1c0 0 3.39 1.23 4.16 5 .38 1.88.42 3.66 1.19 4.42l.66.58H14zm-7 4c1.11 0 2-.89 2-2H5c0 1.11.89 2 2 2z"/></svg>
</a>
    </span>
  </li>

  <li class="dropdown js-menu-container">
    <details class="dropdown-details details-reset js-dropdown-details d-flex px-2 flex-items-center">
      <summary class="HeaderNavlink"
         aria-label="Create new…"
         data-ga-click="Header, create new, icon:add">
        <svg aria-hidden="true" class="octicon octicon-plus float-left mr-1 mt-1" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 9H7v5H5V9H0V7h5V2h2v5h5z"/></svg>
        <span class="dropdown-caret mt-1"></span>
      </summary>

      <ul class="dropdown-menu dropdown-menu-sw">
        
<a class="dropdown-item" href="/new" data-ga-click="Header, create new repository">
  New repository
</a>

  <a class="dropdown-item" href="/new/import" data-ga-click="Header, import a repository">
    Import repository
  </a>

<a class="dropdown-item" href="https://gist.github.com/" data-ga-click="Header, create new gist">
  New gist
</a>

  <a class="dropdown-item" href="/organizations/new" data-ga-click="Header, create new organization">
    New organization
  </a>



  <div class="dropdown-divider"></div>
  <div class="dropdown-header">
    <span title="digitalgreenorg/dg">This repository</span>
  </div>
    <a class="dropdown-item" href="/digitalgreenorg/dg/issues/new" data-ga-click="Header, create new issue">
      New issue
    </a>

      </ul>
    </details>
  </li>

  <li class="dropdown js-menu-container">

    <details class="dropdown-details details-reset js-dropdown-details d-flex pl-2 flex-items-center">
      <summary class="HeaderNavlink name mt-1"
        aria-label="View profile and more"
        data-ga-click="Header, show menu, icon:avatar">
        <img alt="@Divish" class="avatar float-left mr-1" src="https://avatars3.githubusercontent.com/u/13827569?s=40&amp;v=4" height="20" width="20">
        <span class="dropdown-caret"></span>
      </summary>

      <ul class="dropdown-menu dropdown-menu-sw">
        <li class="dropdown-header header-nav-current-user css-truncate">
          Signed in as <strong class="css-truncate-target">Divish</strong>
        </li>

        <li class="dropdown-divider"></li>

        <li><a class="dropdown-item" href="/Divish" data-ga-click="Header, go to profile, text:your profile">
          Your profile
        </a></li>
        <li><a class="dropdown-item" href="/Divish?tab=stars" data-ga-click="Header, go to starred repos, text:your stars">
          Your stars
        </a></li>
          <li><a class="dropdown-item" href="https://gist.github.com/" data-ga-click="Header, your gists, text:your gists">Your Gists</a></li>

        <li class="dropdown-divider"></li>

        <li><a class="dropdown-item" href="https://help.github.com" data-ga-click="Header, go to help, text:help">
          Help
        </a></li>

        <li><a class="dropdown-item" href="/settings/profile" data-ga-click="Header, go to settings, icon:settings">
          Settings
        </a></li>

        <li><!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/logout" class="logout-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="xOMSC6i+FbgrXeAO6uaCXzuNRS/QSINqEgwQ/3M7dM1XgMAyWQa1x7Pw3p1V3KShYyMC1i/Vlyz+9wb0t6yIxQ==" /></div>
          <button type="submit" class="dropdown-item dropdown-signout" data-ga-click="Header, sign out, icon:logout">
            Sign out
          </button>
        </form></li>
      </ul>
    </details>
  </li>
</ul>


        <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/logout" class="sr-only right-0" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="w7l8UJk8HEESgh0WfyWjhPezdNzNl94vo5onOVPwDI1Q2q5paIS8PoovI4XAH4V6rx0zJTIKymlPYTEyl2fwhQ==" /></div>
          <button type="submit" class="dropdown-item dropdown-signout" data-ga-click="Header, sign out, icon:logout">
            Sign out
          </button>
</form>      </div>
    </div>
  </div>
</header>

      

  </div>

  <div id="start-of-content" class="show-on-focus"></div>

    <div id="js-flash-container">
</div>



  <div role="main" >
        <div itemscope itemtype="http://schema.org/SoftwareSourceCode" class="">
    <div id="js-repo-pjax-container" data-pjax-container >
      




  



  <div class="pagehead repohead instapaper_ignore readability-menu experiment-repo-nav  ">
    <div class="repohead-details-container clearfix container">

      <ul class="pagehead-actions">
  <li>
        <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="RGbaqsxNjOOOOcAe3lTlfxE5GZQUXR4Tiu7N3a8cKREXxmMpae+oG31nT/Pa0uMM74k4SQmOePKiyxsBNf3u4w==" /></div>      <input class="form-control" id="repository_id" name="repository_id" type="hidden" value="2742622" />

        <div class="select-menu js-menu-container js-select-menu">
          <a href="/digitalgreenorg/dg/subscription"
            class="btn btn-sm btn-with-count select-menu-button js-menu-target"
            role="button"
            aria-haspopup="true"
            aria-expanded="false"
            aria-label="Toggle repository notifications menu"
            data-ga-click="Repository, click Watch settings, action:blob#show">
            <span class="js-select-button">
                <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6C13 14 16 8 16 8s-3-6-7.94-6zM8 12c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4zm2-4c0 1.11-.89 2-2 2-1.11 0-2-.89-2-2 0-1.11.89-2 2-2 1.11 0 2 .89 2 2z"/></svg>
                Unwatch
            </span>
          </a>
          <a class="social-count js-social-count"
            href="/digitalgreenorg/dg/watchers"
            aria-label="22 users are watching this repository">
            22
          </a>

        <div class="select-menu-modal-holder">
          <div class="select-menu-modal subscription-menu-modal js-menu-content">
            <div class="select-menu-header js-navigation-enable" tabindex="-1">
              <svg aria-label="Close" class="octicon octicon-x js-menu-close" height="16" role="img" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M7.48 8l3.75 3.75-1.48 1.48L6 9.48l-3.75 3.75-1.48-1.48L4.52 8 .77 4.25l1.48-1.48L6 6.52l3.75-3.75 1.48 1.48z"/></svg>
              <span class="select-menu-title">Notifications</span>
            </div>

              <div class="select-menu-list js-navigation-container" role="menu">

                <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                  <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
                  <div class="select-menu-item-text">
                    <input id="do_included" name="do" type="radio" value="included" />
                    <span class="select-menu-item-heading">Not watching</span>
                    <span class="description">Be notified when participating or @mentioned.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6C13 14 16 8 16 8s-3-6-7.94-6zM8 12c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4zm2-4c0 1.11-.89 2-2 2-1.11 0-2-.89-2-2 0-1.11.89-2 2-2 1.11 0 2 .89 2 2z"/></svg>
                      Watch
                    </span>
                  </div>
                </div>

                <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
                  <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
                  <div class="select-menu-item-text">
                    <input checked="checked" id="do_subscribed" name="do" type="radio" value="subscribed" />
                    <span class="select-menu-item-heading">Watching</span>
                    <span class="description">Be notified of all conversations.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6C13 14 16 8 16 8s-3-6-7.94-6zM8 12c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4zm2-4c0 1.11-.89 2-2 2-1.11 0-2-.89-2-2 0-1.11.89-2 2-2 1.11 0 2 .89 2 2z"/></svg>
                        Unwatch
                    </span>
                  </div>
                </div>

                <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                  <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
                  <div class="select-menu-item-text">
                    <input id="do_ignore" name="do" type="radio" value="ignore" />
                    <span class="select-menu-item-heading">Ignoring</span>
                    <span class="description">Never be notified.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <svg aria-hidden="true" class="octicon octicon-mute" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M8 2.81v10.38c0 .67-.81 1-1.28.53L3 10H1c-.55 0-1-.45-1-1V7c0-.55.45-1 1-1h2l3.72-3.72C7.19 1.81 8 2.14 8 2.81zm7.53 3.22l-1.06-1.06-1.97 1.97-1.97-1.97-1.06 1.06L11.44 8 9.47 9.97l1.06 1.06 1.97-1.97 1.97 1.97 1.06-1.06L13.56 8l1.97-1.97z"/></svg>
                        Stop ignoring
                    </span>
                  </div>
                </div>

              </div>

            </div>
          </div>
        </div>
</form>
  </li>

  <li>
    
  <div class="js-toggler-container js-social-container starring-container ">
    <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/digitalgreenorg/dg/unstar" class="starred js-social-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="d5Ob/5PV0DSQj5kIvMZzZtZ45z+In0gFUZmLxz0pphRtH0rXib9KDOClcoV8YPayuYpcyDwoO9WoFbVYahwmZw==" /></div>
      <input type="hidden" name="context" value="repository"></input>
      <button
        type="submit"
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Unstar this repository" title="Unstar digitalgreenorg/dg"
        data-ga-click="Repository, click unstar button, action:blob#show; text:Unstar">
        <svg aria-hidden="true" class="octicon octicon-star" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z"/></svg>
        Unstar
      </button>
        <a class="social-count js-social-count" href="/digitalgreenorg/dg/stargazers"
           aria-label="11 users starred this repository">
          11
        </a>
</form>
    <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/digitalgreenorg/dg/star" class="unstarred js-social-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="j0/VhfNNzO9OuhbEQccRPSAQm46GxhdpDkMUj0hMrdJTqm5NLPDzJPFyQcm3K8Vw/H7KI2AYp20lyw9cYcmSJA==" /></div>
      <input type="hidden" name="context" value="repository"></input>
      <button
        type="submit"
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Star this repository" title="Star digitalgreenorg/dg"
        data-ga-click="Repository, click star button, action:blob#show; text:Star">
        <svg aria-hidden="true" class="octicon octicon-star" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 6l-4.9-.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14 7 11.67 11.33 14l-.93-4.74z"/></svg>
        Star
      </button>
        <a class="social-count js-social-count" href="/digitalgreenorg/dg/stargazers"
           aria-label="11 users starred this repository">
          11
        </a>
</form>  </div>

  </li>

  <li>
          <a href="#fork-destination-box" class="btn btn-sm btn-with-count"
              title="Fork your own copy of digitalgreenorg/dg to your account"
              aria-label="Fork your own copy of digitalgreenorg/dg to your account"
              rel="facebox"
              data-ga-click="Repository, show fork modal, action:blob#show; text:Fork">
              <svg aria-hidden="true" class="octicon octicon-repo-forked" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path fill-rule="evenodd" d="M8 1a1.993 1.993 0 0 0-1 3.72V6L5 8 3 6V4.72A1.993 1.993 0 0 0 2 1a1.993 1.993 0 0 0-1 3.72V6.5l3 3v1.78A1.993 1.993 0 0 0 5 15a1.993 1.993 0 0 0 1-3.72V9.5l3-3V4.72A1.993 1.993 0 0 0 8 1zM2 4.2C1.34 4.2.8 3.65.8 3c0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2zm3 10c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2zm3-10c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2z"/></svg>
            Fork
          </a>

          <div id="fork-destination-box" style="display: none;">
            <h2 class="facebox-header" data-facebox-id="facebox-header">Where should we fork this repository?</h2>
            <include-fragment src=""
                class="js-fork-select-fragment fork-select-fragment"
                data-url="/digitalgreenorg/dg/fork?fragment=1">
              <img alt="Loading" height="64" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-128.gif" width="64" />
            </include-fragment>
          </div>

    <a href="/digitalgreenorg/dg/network" class="social-count"
       aria-label="7 users forked this repository">
      7
    </a>
  </li>
</ul>

      <h1 class="public ">
  <svg aria-hidden="true" class="octicon octicon-repo" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M4 9H3V8h1v1zm0-3H3v1h1V6zm0-2H3v1h1V4zm0-2H3v1h1V2zm8-1v12c0 .55-.45 1-1 1H6v2l-1.5-1.5L3 16v-2H1c-.55 0-1-.45-1-1V1c0-.55.45-1 1-1h10c.55 0 1 .45 1 1zm-1 10H1v2h2v-1h3v1h5v-2zm0-10H2v9h9V1z"/></svg>
  <span class="author" itemprop="author"><a href="/digitalgreenorg" class="url fn" rel="author">digitalgreenorg</a></span><!--
--><span class="path-divider">/</span><!--
--><strong itemprop="name"><a href="/digitalgreenorg/dg" data-pjax="#js-repo-pjax-container">dg</a></strong>

</h1>

    </div>
    
<nav class="reponav js-repo-nav js-sidenav-container-pjax container"
     itemscope
     itemtype="http://schema.org/BreadcrumbList"
     role="navigation"
     data-pjax="#js-repo-pjax-container">

  <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
    <a href="/digitalgreenorg/dg" class="js-selected-navigation-item selected reponav-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches repo_packages /digitalgreenorg/dg" itemprop="url">
      <svg aria-hidden="true" class="octicon octicon-code" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M9.5 3L8 4.5 11.5 8 8 11.5 9.5 13 14 8 9.5 3zm-5 0L0 8l4.5 5L6 11.5 2.5 8 6 4.5 4.5 3z"/></svg>
      <span itemprop="name">Code</span>
      <meta itemprop="position" content="1">
</a>  </span>

    <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
      <a href="/digitalgreenorg/dg/issues" class="js-selected-navigation-item reponav-item" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /digitalgreenorg/dg/issues" itemprop="url">
        <svg aria-hidden="true" class="octicon octicon-issue-opened" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"/></svg>
        <span itemprop="name">Issues</span>
        <span class="Counter">32</span>
        <meta itemprop="position" content="2">
</a>    </span>

  <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
    <a href="/digitalgreenorg/dg/pulls" class="js-selected-navigation-item reponav-item" data-hotkey="g p" data-selected-links="repo_pulls /digitalgreenorg/dg/pulls" itemprop="url">
      <svg aria-hidden="true" class="octicon octicon-git-pull-request" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M11 11.28V5c-.03-.78-.34-1.47-.94-2.06C9.46 2.35 8.78 2.03 8 2H7V0L4 3l3 3V4h1c.27.02.48.11.69.31.21.2.3.42.31.69v6.28A1.993 1.993 0 0 0 10 15a1.993 1.993 0 0 0 1-3.72zm-1 2.92c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2zM4 3c0-1.11-.89-2-2-2a1.993 1.993 0 0 0-1 3.72v6.56A1.993 1.993 0 0 0 2 15a1.993 1.993 0 0 0 1-3.72V4.72c.59-.34 1-.98 1-1.72zm-.8 10c0 .66-.55 1.2-1.2 1.2-.65 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2zM2 4.2C1.34 4.2.8 3.65.8 3c0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2z"/></svg>
      <span itemprop="name">Pull requests</span>
      <span class="Counter">14</span>
      <meta itemprop="position" content="3">
</a>  </span>

    <a href="/digitalgreenorg/dg/projects" class="js-selected-navigation-item reponav-item" data-hotkey="g b" data-selected-links="repo_projects new_repo_project repo_project /digitalgreenorg/dg/projects">
      <svg aria-hidden="true" class="octicon octicon-project" height="16" version="1.1" viewBox="0 0 15 16" width="15"><path fill-rule="evenodd" d="M10 12h3V2h-3v10zm-4-2h3V2H6v8zm-4 4h3V2H2v12zm-1 1h13V1H1v14zM14 0H1a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h13a1 1 0 0 0 1-1V1a1 1 0 0 0-1-1z"/></svg>
      Projects
      <span class="Counter" >1</span>
</a>
    <a href="/digitalgreenorg/dg/wiki" class="js-selected-navigation-item reponav-item" data-hotkey="g w" data-selected-links="repo_wiki /digitalgreenorg/dg/wiki">
      <svg aria-hidden="true" class="octicon octicon-book" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M3 5h4v1H3V5zm0 3h4V7H3v1zm0 2h4V9H3v1zm11-5h-4v1h4V5zm0 2h-4v1h4V7zm0 2h-4v1h4V9zm2-6v9c0 .55-.45 1-1 1H9.5l-1 1-1-1H2c-.55 0-1-.45-1-1V3c0-.55.45-1 1-1h5.5l1 1 1-1H15c.55 0 1 .45 1 1zm-8 .5L7.5 3H2v9h6V3.5zm7-.5H9.5l-.5.5V12h6V3z"/></svg>
      Wiki
</a>

  <a href="/digitalgreenorg/dg/pulse" class="js-selected-navigation-item reponav-item" data-selected-links="repo_graphs repo_contributors dependency_graph pulse /digitalgreenorg/dg/pulse">
    <svg aria-hidden="true" class="octicon octicon-graph" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M16 14v1H0V0h1v14h15zM5 13H3V8h2v5zm4 0H7V3h2v10zm4 0h-2V6h2v7z"/></svg>
    Insights
</a>
    <a href="/digitalgreenorg/dg/settings" class="js-selected-navigation-item reponav-item" data-selected-links="repo_settings repo_branch_settings hooks integration_installations repo_keys_settings /digitalgreenorg/dg/settings">
      <svg aria-hidden="true" class="octicon octicon-gear" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M14 8.77v-1.6l-1.94-.64-.45-1.09.88-1.84-1.13-1.13-1.81.91-1.09-.45-.69-1.92h-1.6l-.63 1.94-1.11.45-1.84-.88-1.13 1.13.91 1.81-.45 1.09L0 7.23v1.59l1.94.64.45 1.09-.88 1.84 1.13 1.13 1.81-.91 1.09.45.69 1.92h1.59l.63-1.94 1.11-.45 1.84.88 1.13-1.13-.92-1.81.47-1.09L14 8.75v.02zM7 11c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"/></svg>
      Settings
</a>
</nav>


  </div>

<div class="container new-discussion-timeline experiment-repo-nav ">
  <div class="repository-content ">

    
  <a href="/digitalgreenorg/dg/blob/4a9d20843f0d5b2b3f11c8ca7e20f7a60183e2d6/loop_ivr/outliers/removal.py" class="d-none js-permalink-shortcut" data-hotkey="y">Permalink</a>

  <!-- blob contrib key: blob_contributors:v21:4b313df5c839302276ab2becb4b54721 -->

  <div class="file-navigation js-zeroclipboard-container">
    
<div class="select-menu branch-select-menu js-menu-container js-select-menu float-left">
  <button class=" btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    
    type="button" aria-label="Switch branches or tags" aria-expanded="false" aria-haspopup="true">
      <i>Branch:</i>
      <span class="js-select-button css-truncate-target">master</span>
  </button>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax>

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <svg aria-label="Close" class="octicon octicon-x js-menu-close" height="16" role="img" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M7.48 8l3.75 3.75-1.48 1.48L6 9.48l-3.75 3.75-1.48-1.48L4.52 8 .77 4.25l1.48-1.48L6 6.52l3.75-3.75 1.48 1.48z"/></svg>
        <span class="select-menu-title">Switch branches/tags</span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Find or create a branch…" id="context-commitish-filter-field" class="form-control js-filterable-field js-navigation-enable" placeholder="Find or create a branch…">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Find or create a branch…" class="js-select-menu-tab" role="tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab" role="tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches" role="menu">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/Adminloop/loop_ivr/outliers/removal.py"
               data-name="Adminloop"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                Adminloop
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/ack_loop_pilot/loop_ivr/outliers/removal.py"
               data-name="ack_loop_pilot"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                ack_loop_pilot
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/aggregator_api/loop_ivr/outliers/removal.py"
               data-name="aggregator_api"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                aggregator_api
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/airflow/loop_ivr/outliers/removal.py"
               data-name="airflow"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                airflow
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/analytics_analysis/loop_ivr/outliers/removal.py"
               data-name="analytics_analysis"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                analytics_analysis
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/analytics_atulya/loop_ivr/outliers/removal.py"
               data-name="analytics_atulya"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                analytics_atulya
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/analytics_login/loop_ivr/outliers/removal.py"
               data-name="analytics_login"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                analytics_login
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/analytics_theme_changes_sujit/loop_ivr/outliers/removal.py"
               data-name="analytics_theme_changes_sujit"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                analytics_theme_changes_sujit
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/api_payment_phone/loop_ivr/outliers/removal.py"
               data-name="api_payment_phone"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                api_payment_phone
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/assign_animator/loop_ivr/outliers/removal.py"
               data-name="assign_animator"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                assign_animator
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/blog_wiki/loop_ivr/outliers/removal.py"
               data-name="blog_wiki"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                blog_wiki
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/census_codes/loop_ivr/outliers/removal.py"
               data-name="census_codes"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                census_codes
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/coco_brand_changes/loop_ivr/outliers/removal.py"
               data-name="coco_brand_changes"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                coco_brand_changes
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/coco_example_app/loop_ivr/outliers/removal.py"
               data-name="coco_example_app"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                coco_example_app
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/coco_old_for_reference/loop_ivr/outliers/removal.py"
               data-name="coco_old_for_reference"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                coco_old_for_reference
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/country-message/loop_ivr/outliers/removal.py"
               data-name="country-message"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                country-message
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/crop_volume_fix/loop_ivr/outliers/removal.py"
               data-name="crop_volume_fix"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                crop_volume_fix
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/d_check/loop_ivr/outliers/removal.py"
               data-name="d_check"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                d_check
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/dj-apvideo/loop_ivr/outliers/removal.py"
               data-name="dj-apvideo"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                dj-apvideo
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/django_admin_changes/loop_ivr/outliers/removal.py"
               data-name="django_admin_changes"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                django_admin_changes
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/django_admin_dataCleanup/loop_ivr/outliers/removal.py"
               data-name="django_admin_dataCleanup"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                django_admin_dataCleanup
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot-hnn/loop_ivr/outliers/removal.py"
               data-name="djangobot-hnn"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot-hnn
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot-offlineanalytics/loop_ivr/outliers/removal.py"
               data-name="djangobot-offlineanalytics"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot-offlineanalytics
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot-qacoco/loop_ivr/outliers/removal.py"
               data-name="djangobot-qacoco"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot-qacoco
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot-srb/loop_ivr/outliers/removal.py"
               data-name="djangobot-srb"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot-srb
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot-tagging/loop_ivr/outliers/removal.py"
               data-name="djangobot-tagging"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot-tagging
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot-website/loop_ivr/outliers/removal.py"
               data-name="djangobot-website"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot-website
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobot_jslps_dasboard/loop_ivr/outliers/removal.py"
               data-name="djangobot_jslps_dasboard"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobot_jslps_dasboard
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/djangobotmaster/loop_ivr/outliers/removal.py"
               data-name="djangobotmaster"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                djangobotmaster
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/domain_test/loop_ivr/outliers/removal.py"
               data-name="domain_test"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                domain_test
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/download_vrp_mrp/loop_ivr/outliers/removal.py"
               data-name="download_vrp_mrp"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                download_vrp_mrp
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/export_csv_admin/loop_ivr/outliers/removal.py"
               data-name="export_csv_admin"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                export_csv_admin
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/filling_latlong_loop/loop_ivr/outliers/removal.py"
               data-name="filling_latlong_loop"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                filling_latlong_loop
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/footer_changes_sujit/loop_ivr/outliers/removal.py"
               data-name="footer_changes_sujit"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                footer_changes_sujit
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/gaddidar_mandi_manytomany/loop_ivr/outliers/removal.py"
               data-name="gaddidar_mandi_manytomany"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                gaddidar_mandi_manytomany
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/geo_tag/loop_ivr/outliers/removal.py"
               data-name="geo_tag"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                geo_tag
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/hack4farming/loop_ivr/outliers/removal.py"
               data-name="hack4farming"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                hack4farming
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/health-nutrition/loop_ivr/outliers/removal.py"
               data-name="health-nutrition"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                health-nutrition
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/hnn-djangobot/loop_ivr/outliers/removal.py"
               data-name="hnn-djangobot"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                hnn-djangobot
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/impact_2/loop_ivr/outliers/removal.py"
               data-name="impact_2"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                impact_2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/ivr_dynamic/loop_ivr/outliers/removal.py"
               data-name="ivr_dynamic"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                ivr_dynamic
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/ivr_mailer/loop_ivr/outliers/removal.py"
               data-name="ivr_mailer"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                ivr_mailer
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/jharkhand_ivr/loop_ivr/outliers/removal.py"
               data-name="jharkhand_ivr"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                jharkhand_ivr
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/jslps_fix/loop_ivr/outliers/removal.py"
               data-name="jslps_fix"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                jslps_fix
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_admin_loopuser/loop_ivr/outliers/removal.py"
               data-name="loop_admin_loopuser"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_admin_loopuser
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_analytics_sujit_new/loop_ivr/outliers/removal.py"
               data-name="loop_analytics_sujit_new"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_analytics_sujit_new
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_email_automation/loop_ivr/outliers/removal.py"
               data-name="loop_email_automation"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_email_automation
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_farmer_message/loop_ivr/outliers/removal.py"
               data-name="loop_farmer_message"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_farmer_message
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_ivr_extention/loop_ivr/outliers/removal.py"
               data-name="loop_ivr_extention"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_ivr_extention
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_ivr_test/loop_ivr/outliers/removal.py"
               data-name="loop_ivr_test"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_ivr_test
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_ivr_verification_broadcast/loop_ivr/outliers/removal.py"
               data-name="loop_ivr_verification_broadcast"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_ivr_verification_broadcast
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_maharashtra_data_import/loop_ivr/outliers/removal.py"
               data-name="loop_maharashtra_data_import"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_maharashtra_data_import
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_maharashtra_helpline/loop_ivr/outliers/removal.py"
               data-name="loop_maharashtra_helpline"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_maharashtra_helpline
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_merge_atulya/loop_ivr/outliers/removal.py"
               data-name="loop_merge_atulya"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_merge_atulya
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_mi_email_changes/loop_ivr/outliers/removal.py"
               data-name="loop_mi_email_changes"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_mi_email_changes
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/loop_payment_test/loop_ivr/outliers/removal.py"
               data-name="loop_payment_test"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                loop_payment_test
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/master_ivr_usaid/loop_ivr/outliers/removal.py"
               data-name="master_ivr_usaid"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                master_ivr_usaid
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/master_nonnegotiable_download/loop_ivr/outliers/removal.py"
               data-name="master_nonnegotiable_download"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                master_nonnegotiable_download
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/master_subtitle/loop_ivr/outliers/removal.py"
               data-name="master_subtitle"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                master_subtitle
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/master_usaid_workshop/loop_ivr/outliers/removal.py"
               data-name="master_usaid_workshop"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                master_usaid_workshop
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/digitalgreenorg/dg/blob/master/loop_ivr/outliers/removal.py"
               data-name="master"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                master
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/mi_changes_regex_integrate_outlier/loop_ivr/outliers/removal.py"
               data-name="mi_changes_regex_integrate_outlier"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                mi_changes_regex_integrate_outlier
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/mi_enhance/loop_ivr/outliers/removal.py"
               data-name="mi_enhance"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                mi_enhance
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/mi_template/loop_ivr/outliers/removal.py"
               data-name="mi_template"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                mi_template
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/mr_transportation/loop_ivr/outliers/removal.py"
               data-name="mr_transportation"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                mr_transportation
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/mrp_vrp_export/loop_ivr/outliers/removal.py"
               data-name="mrp_vrp_export"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                mrp_vrp_export
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/new-branch/loop_ivr/outliers/removal.py"
               data-name="new-branch"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                new-branch
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/new_etl/loop_ivr/outliers/removal.py"
               data-name="new_etl"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                new_etl
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/offline-analytics-djangobot/loop_ivr/outliers/removal.py"
               data-name="offline-analytics-djangobot"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                offline-analytics-djangobot
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/offline_analytics_aman/loop_ivr/outliers/removal.py"
               data-name="offline_analytics_aman"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                offline_analytics_aman
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/offline_analytics/loop_ivr/outliers/removal.py"
               data-name="offline_analytics"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                offline_analytics
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/offline_sync/loop_ivr/outliers/removal.py"
               data-name="offline_sync"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                offline_sync
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/old_dashboards/loop_ivr/outliers/removal.py"
               data-name="old_dashboards"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                old_dashboards
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/old_jhar_ivr/loop_ivr/outliers/removal.py"
               data-name="old_jhar_ivr"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                old_jhar_ivr
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/outlier_removal_loop_analysis/loop_ivr/outliers/removal.py"
               data-name="outlier_removal_loop_analysis"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                outlier_removal_loop_analysis
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/payment_api_authorization_fix/loop_ivr/outliers/removal.py"
               data-name="payment_api_authorization_fix"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                payment_api_authorization_fix
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/payment_fix/loop_ivr/outliers/removal.py"
               data-name="payment_fix"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                payment_fix
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/payment_login/loop_ivr/outliers/removal.py"
               data-name="payment_login"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                payment_login
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/payment_sheet_dynamic/loop_ivr/outliers/removal.py"
               data-name="payment_sheet_dynamic"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                payment_sheet_dynamic
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/payments_new_model_bug_fixes/loop_ivr/outliers/removal.py"
               data-name="payments_new_model_bug_fixes"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                payments_new_model_bug_fixes
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/push_sms_email/loop_ivr/outliers/removal.py"
               data-name="push_sms_email"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                push_sms_email
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/push_sms/loop_ivr/outliers/removal.py"
               data-name="push_sms"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                push_sms
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/raw_data_ui/loop_ivr/outliers/removal.py"
               data-name="raw_data_ui"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                raw_data_ui
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/raw_data_video_clear/loop_ivr/outliers/removal.py"
               data-name="raw_data_video_clear"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                raw_data_video_clear
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/raw_data_video_id/loop_ivr/outliers/removal.py"
               data-name="raw_data_video_id"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                raw_data_video_id
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/rawDataAnimatorAdd/loop_ivr/outliers/removal.py"
               data-name="rawDataAnimatorAdd"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                rawDataAnimatorAdd
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/rawDataDownloadLargeData/loop_ivr/outliers/removal.py"
               data-name="rawDataDownloadLargeData"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                rawDataDownloadLargeData
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/rawdata_ui/loop_ivr/outliers/removal.py"
               data-name="rawdata_ui"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                rawdata_ui
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/rda_update/loop_ivr/outliers/removal.py"
               data-name="rda_update"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                rda_update
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/recruitment_test/loop_ivr/outliers/removal.py"
               data-name="recruitment_test"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                recruitment_test
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/reordering_admin/loop_ivr/outliers/removal.py"
               data-name="reordering_admin"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                reordering_admin
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/sms_infinite_bug_fix/loop_ivr/outliers/removal.py"
               data-name="sms_infinite_bug_fix"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                sms_infinite_bug_fix
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/sms_line/loop_ivr/outliers/removal.py"
               data-name="sms_line"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                sms_line
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/sms_script/loop_ivr/outliers/removal.py"
               data-name="sms_script"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                sms_script
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/sql_optimizations/loop_ivr/outliers/removal.py"
               data-name="sql_optimizations"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                sql_optimizations
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/test_configure_loop_ivr/loop_ivr/outliers/removal.py"
               data-name="test_configure_loop_ivr"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                test_configure_loop_ivr
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/testUserSyncStop/loop_ivr/outliers/removal.py"
               data-name="testUserSyncStop"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                testUserSyncStop
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/testtest/loop_ivr/outliers/removal.py"
               data-name="testtest"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                testtest
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/textlocal_api/loop_ivr/outliers/removal.py"
               data-name="textlocal_api"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                textlocal_api
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/upgrade_lib/loop_ivr/outliers/removal.py"
               data-name="upgrade_lib"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                upgrade_lib
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/username_password_mailer/loop_ivr/outliers/removal.py"
               data-name="username_password_mailer"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                username_password_mailer
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/video_upload/loop_ivr/outliers/removal.py"
               data-name="video_upload"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                video_upload
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/website_brand_launch_compiled/loop_ivr/outliers/removal.py"
               data-name="website_brand_launch_compiled"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                website_brand_launch_compiled
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/website_domain_changes/loop_ivr/outliers/removal.py"
               data-name="website_domain_changes"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                website_domain_changes
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
               href="/digitalgreenorg/dg/blob/website_office/loop_ivr/outliers/removal.py"
               data-name="website_office"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text">
                website_office
              </span>
            </a>
        </div>

          <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/digitalgreenorg/dg/branches" class="js-create-branch select-menu-item select-menu-new-item-form js-navigation-item js-new-item-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="UPq5JaDIVyB9Hn+Jl1Yv0LaDWjIODdqDUyXuIqcik6UXSji/mJ0Ejf9FYDLnVF/DPV5VRlfgAr82hsG4KpBqfQ==" /></div>
          <svg aria-hidden="true" class="octicon octicon-git-branch select-menu-item-icon" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path fill-rule="evenodd" d="M10 5c0-1.11-.89-2-2-2a1.993 1.993 0 0 0-1 3.72v.3c-.02.52-.23.98-.63 1.38-.4.4-.86.61-1.38.63-.83.02-1.48.16-2 .45V4.72a1.993 1.993 0 0 0-1-3.72C.88 1 0 1.89 0 3a2 2 0 0 0 1 1.72v6.56c-.59.35-1 .99-1 1.72 0 1.11.89 2 2 2 1.11 0 2-.89 2-2 0-.53-.2-1-.53-1.36.09-.06.48-.41.59-.47.25-.11.56-.17.94-.17 1.05-.05 1.95-.45 2.75-1.25S8.95 7.77 9 6.73h-.02C9.59 6.37 10 5.73 10 5zM2 1.8c.66 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2C1.35 4.2.8 3.65.8 3c0-.65.55-1.2 1.2-1.2zm0 12.41c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2zm6-8c-.66 0-1.2-.55-1.2-1.2 0-.65.55-1.2 1.2-1.2.65 0 1.2.55 1.2 1.2 0 .65-.55 1.2-1.2 1.2z"/></svg>
            <div class="select-menu-item-text">
              <span class="select-menu-item-heading">Create branch: <span class="js-new-item-name"></span></span>
              <span class="description">from ‘master’</span>
            </div>
            <input type="hidden" name="name" id="name" class="js-new-item-value">
            <input type="hidden" name="branch" id="branch" value="master">
            <input type="hidden" name="path" id="path" value="loop_ivr/outliers/removal.py">
</form>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.3/loop_ivr/outliers/removal.py"
              data-name="v1.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.3">
                v1.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.2/loop_ivr/outliers/removal.py"
              data-name="v1.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.2">
                v1.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.1.5/loop_ivr/outliers/removal.py"
              data-name="v1.1.5"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.5">
                v1.1.5
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.1.4/loop_ivr/outliers/removal.py"
              data-name="v1.1.4"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.4">
                v1.1.4
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.1.3/loop_ivr/outliers/removal.py"
              data-name="v1.1.3"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.3">
                v1.1.3
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.1.2/loop_ivr/outliers/removal.py"
              data-name="v1.1.2"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.2">
                v1.1.2
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.1.1/loop_ivr/outliers/removal.py"
              data-name="v1.1.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1.1">
                v1.1.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.1/loop_ivr/outliers/removal.py"
              data-name="v1.1"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.1">
                v1.1
              </span>
            </a>
            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/digitalgreenorg/dg/tree/v1.0/loop_ivr/outliers/removal.py"
              data-name="v1.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M12 5l-8 8-4-4 1.5-1.5L4 10l6.5-6.5z"/></svg>
              <span class="select-menu-item-text css-truncate-target" title="v1.0">
                v1.0
              </span>
            </a>
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>

    <div class="BtnGroup float-right">
      <a href="/digitalgreenorg/dg/find/master"
            class="js-pjax-capture-input btn btn-sm BtnGroup-item"
            data-pjax
            data-hotkey="t">
        Find file
      </a>
      <button aria-label="Copy file path to clipboard" class="js-zeroclipboard btn btn-sm BtnGroup-item tooltipped tooltipped-s" data-copied-hint="Copied!" type="button">Copy path</button>
    </div>
    <div class="breadcrumb js-zeroclipboard-target">
      <span class="repo-root js-repo-root"><span class="js-path-segment"><a href="/digitalgreenorg/dg"><span>dg</span></a></span></span><span class="separator">/</span><span class="js-path-segment"><a href="/digitalgreenorg/dg/tree/master/loop_ivr"><span>loop_ivr</span></a></span><span class="separator">/</span><span class="js-path-segment"><a href="/digitalgreenorg/dg/tree/master/loop_ivr/outliers"><span>outliers</span></a></span><span class="separator">/</span><strong class="final-path">removal.py</strong>
    </div>
  </div>


  
  <div class="commit-tease">
      <span class="float-right">
        <a class="commit-tease-sha" href="/digitalgreenorg/dg/commit/61eb2f37801b63754f3257b2f261cd1aa339ba46" data-pjax>
          61eb2f3
        </a>
        <relative-time datetime="2018-01-05T07:51:42Z">Jan 5, 2018</relative-time>
      </span>
      <div>
        <img alt="@Abhishek-lodha" class="avatar" height="20" src="https://avatars1.githubusercontent.com/u/7737588?s=40&amp;v=4" width="20" />
        <a href="/Abhishek-lodha" class="user-mention" rel="contributor">Abhishek-lodha</a>
          <a href="/digitalgreenorg/dg/commit/61eb2f37801b63754f3257b2f261cd1aa339ba46" class="message" data-pjax="true" title="changed dataframe sort order">changed dataframe sort order</a>
      </div>

    <div class="commit-tease-contributors">
      <button type="button" class="btn-link muted-link contributors-toggle" data-facebox="#blob_contributors_box">
        <strong>2</strong>
         contributors
      </button>
          <a class="avatar-link tooltipped tooltipped-s" aria-label="Abhishek-lodha" href="/digitalgreenorg/dg/commits/master/loop_ivr/outliers/removal.py?author=Abhishek-lodha"><img alt="@Abhishek-lodha" class="avatar" height="20" src="https://avatars1.githubusercontent.com/u/7737588?s=40&amp;v=4" width="20" /> </a>
    <a class="avatar-link tooltipped tooltipped-s" aria-label="sujit22993" href="/digitalgreenorg/dg/commits/master/loop_ivr/outliers/removal.py?author=sujit22993"><img alt="@sujit22993" class="avatar" height="20" src="https://avatars1.githubusercontent.com/u/8048341?s=40&amp;v=4" width="20" /> </a>


    </div>

    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header" data-facebox-id="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list" data-facebox-id="facebox-description">
          <li class="facebox-user-list-item">
            <img alt="@Abhishek-lodha" height="24" src="https://avatars0.githubusercontent.com/u/7737588?s=48&amp;v=4" width="24" />
            <a href="/Abhishek-lodha">Abhishek-lodha</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="@sujit22993" height="24" src="https://avatars0.githubusercontent.com/u/8048341?s=48&amp;v=4" width="24" />
            <a href="/sujit22993">sujit22993</a>
          </li>
      </ul>
    </div>
  </div>


  <div class="file">
    <div class="file-header">
  <div class="file-actions">

    <div class="BtnGroup">
      <a href="/digitalgreenorg/dg/raw/master/loop_ivr/outliers/removal.py" class="btn btn-sm BtnGroup-item" id="raw-url">Raw</a>
        <a href="/digitalgreenorg/dg/blame/master/loop_ivr/outliers/removal.py" class="btn btn-sm js-update-url-with-hash BtnGroup-item" data-hotkey="b">Blame</a>
      <a href="/digitalgreenorg/dg/commits/master/loop_ivr/outliers/removal.py" class="btn btn-sm BtnGroup-item" rel="nofollow">History</a>
    </div>

        <a class="btn-octicon tooltipped tooltipped-nw"
           href="https://desktop.github.com"
           aria-label="Open this file in GitHub Desktop"
           data-ga-click="Repository, open with desktop, type:windows">
            <svg aria-hidden="true" class="octicon octicon-device-desktop" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M15 2H1c-.55 0-1 .45-1 1v9c0 .55.45 1 1 1h5.34c-.25.61-.86 1.39-2.34 2h8c-1.48-.61-2.09-1.39-2.34-2H15c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1zm0 9H1V3h14v8z"/></svg>
        </a>

        <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/digitalgreenorg/dg/edit/master/loop_ivr/outliers/removal.py" class="inline-form js-update-url-with-hash" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="uumEJaX/A9L6WMfhoZLWsuYRuygio9sDvPDAeG699/U2qR/T2VE6Djdb4Bw+Xk6VOZHiYcLSmceRHR6rXh5SuQ==" /></div>
          <button class="btn-octicon tooltipped tooltipped-nw" type="submit"
            aria-label="Edit this file" data-hotkey="e" data-disable-with>
            <svg aria-hidden="true" class="octicon octicon-pencil" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path fill-rule="evenodd" d="M0 12v3h3l8-8-3-3-8 8zm3 2H1v-2h1v1h1v1zm10.3-9.3L12 6 9 3l1.3-1.3a.996.996 0 0 1 1.41 0l1.59 1.59c.39.39.39 1.02 0 1.41z"/></svg>
          </button>
</form>        <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="/digitalgreenorg/dg/delete/master/loop_ivr/outliers/removal.py" class="inline-form" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="RYbVfyKpEnJqWvB7CC02EU/PFLJzZcQWTuA0XiqQJmwYXMECGVjw1jQlmYl/JLQxGOSvqOsA9z9bOwGmnNQ8uA==" /></div>
          <button class="btn-octicon btn-octicon-danger tooltipped tooltipped-nw" type="submit"
            aria-label="Delete this file" data-disable-with>
            <svg aria-hidden="true" class="octicon octicon-trashcan" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M11 2H9c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1H2c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1v9c0 .55.45 1 1 1h7c.55 0 1-.45 1-1V5c.55 0 1-.45 1-1V3c0-.55-.45-1-1-1zm-1 12H3V5h1v8h1V5h1v8h1V5h1v8h1V5h1v9zm1-10H2V3h9v1z"/></svg>
          </button>
</form>  </div>

  <div class="file-info">
      124 lines (97 sloc)
      <span class="file-info-divider"></span>
    7.42 KB
  </div>
</div>

    

  <div itemprop="text" class="blob-wrapper data type-python">
      <table class="highlight tab-size js-file-line-container" data-tab-size="8">
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code blob-code-inner js-file-line"><span class="pl-k">import</span> pandas <span class="pl-k">as</span> pd</td>
      </tr>
      <tr>
        <td id="L2" class="blob-num js-line-number" data-line-number="2"></td>
        <td id="LC2" class="blob-code blob-code-inner js-file-line"><span class="pl-k">import</span> numpy <span class="pl-k">as</span> np</td>
      </tr>
      <tr>
        <td id="L3" class="blob-num js-line-number" data-line-number="3"></td>
        <td id="LC3" class="blob-code blob-code-inner js-file-line"><span class="pl-k">from</span> loop_ivr.outliers.common_functions <span class="pl-k">import</span> <span class="pl-k">*</span></td>
      </tr>
      <tr>
        <td id="L4" class="blob-num js-line-number" data-line-number="4"></td>
        <td id="LC4" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L5" class="blob-num js-line-number" data-line-number="5"></td>
        <td id="LC5" class="blob-code blob-code-inner js-file-line">group_by_list <span class="pl-k">=</span> [<span class="pl-s"><span class="pl-pds">&#39;</span>Date<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Market_Real<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Crop<span class="pl-pds">&#39;</span></span>]</td>
      </tr>
      <tr>
        <td id="L6" class="blob-num js-line-number" data-line-number="6"></td>
        <td id="LC6" class="blob-code blob-code-inner js-file-line">final_group_by <span class="pl-k">=</span> [<span class="pl-s"><span class="pl-pds">&#39;</span>Crop<span class="pl-pds">&#39;</span></span>,<span class="pl-s"><span class="pl-pds">&#39;</span>Market_Real<span class="pl-pds">&#39;</span></span>,<span class="pl-s"><span class="pl-pds">&#39;</span>Date<span class="pl-pds">&#39;</span></span>]</td>
      </tr>
      <tr>
        <td id="L7" class="blob-num js-line-number" data-line-number="7"></td>
        <td id="LC7" class="blob-code blob-code-inner js-file-line">columnlist_ct <span class="pl-k">=</span> [<span class="pl-s"><span class="pl-pds">&#39;</span>Date<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Aggregator<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Market_Real<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Crop<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Quantity_Real<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Price<span class="pl-pds">&#39;</span></span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Amount<span class="pl-pds">&#39;</span></span>]</td>
      </tr>
      <tr>
        <td id="L8" class="blob-num js-line-number" data-line-number="8"></td>
        <td id="LC8" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L9" class="blob-num js-line-number" data-line-number="9"></td>
        <td id="LC9" class="blob-code blob-code-inner js-file-line"><span class="pl-k">def</span> <span class="pl-en">remove_crop_outliers</span>(<span class="pl-smi">ct_data</span><span class="pl-k">=</span><span class="pl-c1">None</span>):</td>
      </tr>
      <tr>
        <td id="L10" class="blob-num js-line-number" data-line-number="10"></td>
        <td id="LC10" class="blob-code blob-code-inner js-file-line">    <span class="pl-k">try</span>:</td>
      </tr>
      <tr>
        <td id="L11" class="blob-num js-line-number" data-line-number="11"></td>
        <td id="LC11" class="blob-code blob-code-inner js-file-line">        daily_aggregator_market_crop_rate_query_result <span class="pl-k">=</span> <span class="pl-c1">list</span>(ct_data)</td>
      </tr>
      <tr>
        <td id="L12" class="blob-num js-line-number" data-line-number="12"></td>
        <td id="LC12" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L13" class="blob-num js-line-number" data-line-number="13"></td>
        <td id="LC13" class="blob-code blob-code-inner js-file-line">        combined_transactions_data <span class="pl-k">=</span> pd.DataFrame(daily_aggregator_market_crop_rate_query_result)</td>
      </tr>
      <tr>
        <td id="L14" class="blob-num js-line-number" data-line-number="14"></td>
        <td id="LC14" class="blob-code blob-code-inner js-file-line">        combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Date<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> pd.to_datetime(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Date<span class="pl-pds">&#39;</span></span>])</td>
      </tr>
      <tr>
        <td id="L15" class="blob-num js-line-number" data-line-number="15"></td>
        <td id="LC15" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L16" class="blob-num js-line-number" data-line-number="16"></td>
        <td id="LC16" class="blob-code blob-code-inner js-file-line">        combined_transactions_data <span class="pl-k">=</span> call_methods(combined_transactions_data)</td>
      </tr>
      <tr>
        <td id="L17" class="blob-num js-line-number" data-line-number="17"></td>
        <td id="LC17" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L18" class="blob-num js-line-number" data-line-number="18"></td>
        <td id="LC18" class="blob-code blob-code-inner js-file-line">        <span class="pl-k">for</span> recursion_counter <span class="pl-k">in</span> <span class="pl-c1">range</span>(<span class="pl-c1">0</span>,<span class="pl-c1">3</span>):</td>
      </tr>
      <tr>
        <td id="L19" class="blob-num js-line-number" data-line-number="19"></td>
        <td id="LC19" class="blob-code blob-code-inner js-file-line">            combined_transactions_data.fillna(<span class="pl-c1">0</span>,<span class="pl-v">inplace</span><span class="pl-k">=</span><span class="pl-c1">True</span>)</td>
      </tr>
      <tr>
        <td id="L20" class="blob-num js-line-number" data-line-number="20"></td>
        <td id="LC20" class="blob-code blob-code-inner js-file-line">            ct_data <span class="pl-k">=</span> combined_transactions_data[(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>D/STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1.3</span>)]</td>
      </tr>
      <tr>
        <td id="L21" class="blob-num js-line-number" data-line-number="21"></td>
        <td id="LC21" class="blob-code blob-code-inner js-file-line">            <span class="pl-k">if</span> ct_data <span class="pl-k">is</span> <span class="pl-k">not</span> <span class="pl-c1">None</span>:</td>
      </tr>
      <tr>
        <td id="L22" class="blob-num js-line-number" data-line-number="22"></td>
        <td id="LC22" class="blob-code blob-code-inner js-file-line">                combined_transactions_data <span class="pl-k">=</span> combined_transactions_data[(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>D/STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1.3</span>)]</td>
      </tr>
      <tr>
        <td id="L23" class="blob-num js-line-number" data-line-number="23"></td>
        <td id="LC23" class="blob-code blob-code-inner js-file-line">                combined_transactions_data <span class="pl-k">=</span> combined_transactions_data[columnlist_ct]</td>
      </tr>
      <tr>
        <td id="L24" class="blob-num js-line-number" data-line-number="24"></td>
        <td id="LC24" class="blob-code blob-code-inner js-file-line">                combined_transactions_data <span class="pl-k">=</span> call_methods(combined_transactions_data)</td>
      </tr>
      <tr>
        <td id="L25" class="blob-num js-line-number" data-line-number="25"></td>
        <td id="LC25" class="blob-code blob-code-inner js-file-line">            <span class="pl-k">else</span>:</td>
      </tr>
      <tr>
        <td id="L26" class="blob-num js-line-number" data-line-number="26"></td>
        <td id="LC26" class="blob-code blob-code-inner js-file-line">                <span class="pl-k">break</span></td>
      </tr>
      <tr>
        <td id="L27" class="blob-num js-line-number" data-line-number="27"></td>
        <td id="LC27" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L28" class="blob-num js-line-number" data-line-number="28"></td>
        <td id="LC28" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data = combined_transactions_data[(combined_transactions_data[&#39;D/STD&#39;] &lt;= 1.3)]</span></td>
      </tr>
      <tr>
        <td id="L29" class="blob-num js-line-number" data-line-number="29"></td>
        <td id="LC29" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data = combined_transactions_data[columnlist_ct]</span></td>
      </tr>
      <tr>
        <td id="L30" class="blob-num js-line-number" data-line-number="30"></td>
        <td id="LC30" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data = call_methods(combined_transactions_data)</span></td>
      </tr>
      <tr>
        <td id="L31" class="blob-num js-line-number" data-line-number="31"></td>
        <td id="LC31" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L32" class="blob-num js-line-number" data-line-number="32"></td>
        <td id="LC32" class="blob-code blob-code-inner js-file-line">        combined_transactions_data.fillna(<span class="pl-c1">0</span>,<span class="pl-v">inplace</span><span class="pl-k">=</span><span class="pl-c1">True</span>)</td>
      </tr>
      <tr>
        <td id="L33" class="blob-num js-line-number" data-line-number="33"></td>
        <td id="LC33" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data.to_csv(&quot;final_data_after_outliers_1.csv&quot;)</span></td>
      </tr>
      <tr>
        <td id="L34" class="blob-num js-line-number" data-line-number="34"></td>
        <td id="LC34" class="blob-code blob-code-inner js-file-line">        combined_transactions_data <span class="pl-k">=</span> combined_transactions_data.groupby(group_by_list).agg({<span class="pl-s"><span class="pl-pds">&#39;</span>Av_Rate<span class="pl-pds">&#39;</span></span>:[<span class="pl-s"><span class="pl-pds">&#39;</span>mean<span class="pl-pds">&#39;</span></span>], <span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span> : [<span class="pl-s"><span class="pl-pds">&#39;</span>mean<span class="pl-pds">&#39;</span></span>], <span class="pl-s"><span class="pl-pds">&#39;</span>Price<span class="pl-pds">&#39;</span></span>:[<span class="pl-s"><span class="pl-pds">&#39;</span>max<span class="pl-pds">&#39;</span></span>,<span class="pl-s"><span class="pl-pds">&#39;</span>min<span class="pl-pds">&#39;</span></span>],<span class="pl-s"><span class="pl-pds">&#39;</span>Total_Quantity<span class="pl-pds">&#39;</span></span>:[<span class="pl-s"><span class="pl-pds">&#39;</span>sum<span class="pl-pds">&#39;</span></span>]}).reset_index()</td>
      </tr>
      <tr>
        <td id="L35" class="blob-num js-line-number" data-line-number="35"></td>
        <td id="LC35" class="blob-code blob-code-inner js-file-line">        combined_transactions_data.columns <span class="pl-k">=</span> [<span class="pl-s"><span class="pl-pds">&quot;</span><span class="pl-pds">&quot;</span></span>.join(agg) <span class="pl-k">for</span> agg <span class="pl-k">in</span> combined_transactions_data.columns.ravel()]</td>
      </tr>
      <tr>
        <td id="L36" class="blob-num js-line-number" data-line-number="36"></td>
        <td id="LC36" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data.columns = combined_transactions_data.columns.droplevel(level=1)</span></td>
      </tr>
      <tr>
        <td id="L37" class="blob-num js-line-number" data-line-number="37"></td>
        <td id="LC37" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L38" class="blob-num js-line-number" data-line-number="38"></td>
        <td id="LC38" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span>Arranging dataframe according to crop, market and date</span></td>
      </tr>
      <tr>
        <td id="L39" class="blob-num js-line-number" data-line-number="39"></td>
        <td id="LC39" class="blob-code blob-code-inner js-file-line">        <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data = combined_transactions_data.groupby(final_group_by).apply(lambda x: x.sort_values([&#39;Crop&#39;,&#39;Market_Real&#39;,&#39;Date&#39;],ascending=[True,True,False])).reset_index(drop=True)</span></td>
      </tr>
      <tr>
        <td id="L40" class="blob-num js-line-number" data-line-number="40"></td>
        <td id="LC40" class="blob-code blob-code-inner js-file-line">        combined_transactions_data <span class="pl-k">=</span> combined_transactions_data.sort_values([<span class="pl-s"><span class="pl-pds">&#39;</span>Crop<span class="pl-pds">&#39;</span></span>,<span class="pl-s"><span class="pl-pds">&#39;</span>Market_Real<span class="pl-pds">&#39;</span></span>,<span class="pl-s"><span class="pl-pds">&#39;</span>Date<span class="pl-pds">&#39;</span></span>,<span class="pl-s"><span class="pl-pds">&#39;</span>Total_Quantitysum<span class="pl-pds">&#39;</span></span>],<span class="pl-v">ascending</span><span class="pl-k">=</span>[<span class="pl-c1">True</span>,<span class="pl-c1">True</span>,<span class="pl-c1">False</span>,<span class="pl-c1">False</span>])</td>
      </tr>
      <tr>
        <td id="L41" class="blob-num js-line-number" data-line-number="41"></td>
        <td id="LC41" class="blob-code blob-code-inner js-file-line">        <span class="pl-k">return</span> combined_transactions_data</td>
      </tr>
      <tr>
        <td id="L42" class="blob-num js-line-number" data-line-number="42"></td>
        <td id="LC42" class="blob-code blob-code-inner js-file-line">    <span class="pl-k">except</span> <span class="pl-c1">Exception</span> <span class="pl-k">as</span> e:</td>
      </tr>
      <tr>
        <td id="L43" class="blob-num js-line-number" data-line-number="43"></td>
        <td id="LC43" class="blob-code blob-code-inner js-file-line">        <span class="pl-k">return</span> <span class="pl-c1">None</span></td>
      </tr>
      <tr>
        <td id="L44" class="blob-num js-line-number" data-line-number="44"></td>
        <td id="LC44" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L45" class="blob-num js-line-number" data-line-number="45"></td>
        <td id="LC45" class="blob-code blob-code-inner js-file-line"><span class="pl-k">def</span> <span class="pl-en">call_methods</span>(<span class="pl-smi">combined_transactions_data</span>):</td>
      </tr>
      <tr>
        <td id="L46" class="blob-num js-line-number" data-line-number="46"></td>
        <td id="LC46" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> get_statistics(combined_transactions_data)</td>
      </tr>
      <tr>
        <td id="L47" class="blob-num js-line-number" data-line-number="47"></td>
        <td id="LC47" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> raise_flags(combined_transactions_data)</td>
      </tr>
      <tr>
        <td id="L48" class="blob-num js-line-number" data-line-number="48"></td>
        <td id="LC48" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L49" class="blob-num js-line-number" data-line-number="49"></td>
        <td id="LC49" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> combined_transactions_data[(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>]<span class="pl-k">==</span><span class="pl-c1">1</span>) <span class="pl-k">|</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>]<span class="pl-k">==</span><span class="pl-c1">5</span>)]</td>
      </tr>
      <tr>
        <td id="L50" class="blob-num js-line-number" data-line-number="50"></td>
        <td id="LC50" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L51" class="blob-num js-line-number" data-line-number="51"></td>
        <td id="LC51" class="blob-code blob-code-inner js-file-line">    <span class="pl-k">return</span> combined_transactions_data</td>
      </tr>
      <tr>
        <td id="L52" class="blob-num js-line-number" data-line-number="52"></td>
        <td id="LC52" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L53" class="blob-num js-line-number" data-line-number="53"></td>
        <td id="LC53" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L54" class="blob-num js-line-number" data-line-number="54"></td>
        <td id="LC54" class="blob-code blob-code-inner js-file-line"><span class="pl-k">def</span> <span class="pl-en">get_statistics</span>(<span class="pl-smi">combined_transactions_data</span>):</td>
      </tr>
      <tr>
        <td id="L55" class="blob-num js-line-number" data-line-number="55"></td>
        <td id="LC55" class="blob-code blob-code-inner js-file-line">    ct_data_with_mean <span class="pl-k">=</span> combined_transactions_data.groupby(group_by_list).apply(compute_mean).reset_index(<span class="pl-v">name</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>Av_Rate<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L56" class="blob-num js-line-number" data-line-number="56"></td>
        <td id="LC56" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> combined_transactions_data.merge(ct_data_with_mean,<span class="pl-v">how</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>left<span class="pl-pds">&#39;</span></span>,<span class="pl-v">on</span><span class="pl-k">=</span>group_by_list)</td>
      </tr>
      <tr>
        <td id="L57" class="blob-num js-line-number" data-line-number="57"></td>
        <td id="LC57" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L58" class="blob-num js-line-number" data-line-number="58"></td>
        <td id="LC58" class="blob-code blob-code-inner js-file-line">    ct_with_total_quanity <span class="pl-k">=</span> combined_transactions_data.groupby(group_by_list).apply(</td>
      </tr>
      <tr>
        <td id="L59" class="blob-num js-line-number" data-line-number="59"></td>
        <td id="LC59" class="blob-code blob-code-inner js-file-line">        compute_total_q).reset_index(<span class="pl-v">name</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>Total_Quantity<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L60" class="blob-num js-line-number" data-line-number="60"></td>
        <td id="LC60" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> combined_transactions_data.merge(ct_with_total_quanity, <span class="pl-v">how</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>left<span class="pl-pds">&#39;</span></span>,</td>
      </tr>
      <tr>
        <td id="L61" class="blob-num js-line-number" data-line-number="61"></td>
        <td id="LC61" class="blob-code blob-code-inner js-file-line">                                                                  <span class="pl-v">on</span><span class="pl-k">=</span>group_by_list)</td>
      </tr>
      <tr>
        <td id="L62" class="blob-num js-line-number" data-line-number="62"></td>
        <td id="LC62" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L63" class="blob-num js-line-number" data-line-number="63"></td>
        <td id="LC63" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> compute_deviation(combined_transactions_data)</td>
      </tr>
      <tr>
        <td id="L64" class="blob-num js-line-number" data-line-number="64"></td>
        <td id="LC64" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L65" class="blob-num js-line-number" data-line-number="65"></td>
        <td id="LC65" class="blob-code blob-code-inner js-file-line">    ct_with_max_deviation <span class="pl-k">=</span> combined_transactions_data.groupby(group_by_list).apply(compute_max_deviation).reset_index(<span class="pl-v">name</span><span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L66" class="blob-num js-line-number" data-line-number="66"></td>
        <td id="LC66" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> combined_transactions_data.merge(ct_with_max_deviation,<span class="pl-v">how</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>left<span class="pl-pds">&#39;</span></span>,<span class="pl-v">on</span><span class="pl-k">=</span>group_by_list)</td>
      </tr>
      <tr>
        <td id="L67" class="blob-num js-line-number" data-line-number="67"></td>
        <td id="LC67" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L68" class="blob-num js-line-number" data-line-number="68"></td>
        <td id="LC68" class="blob-code blob-code-inner js-file-line">    ct_with_std <span class="pl-k">=</span> combined_transactions_data.groupby(group_by_list).apply(compute_std).reset_index(<span class="pl-v">name</span><span class="pl-k">=</span> <span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>)</td>
      </tr>
      <tr>
        <td id="L69" class="blob-num js-line-number" data-line-number="69"></td>
        <td id="LC69" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> combined_transactions_data.merge(ct_with_std,<span class="pl-v">how</span><span class="pl-k">=</span><span class="pl-s"><span class="pl-pds">&#39;</span>left<span class="pl-pds">&#39;</span></span>,<span class="pl-v">on</span><span class="pl-k">=</span>group_by_list)</td>
      </tr>
      <tr>
        <td id="L70" class="blob-num js-line-number" data-line-number="70"></td>
        <td id="LC70" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L71" class="blob-num js-line-number" data-line-number="71"></td>
        <td id="LC71" class="blob-code blob-code-inner js-file-line">    combined_transactions_data <span class="pl-k">=</span> compute_ratios(combined_transactions_data)</td>
      </tr>
      <tr>
        <td id="L72" class="blob-num js-line-number" data-line-number="72"></td>
        <td id="LC72" class="blob-code blob-code-inner js-file-line">    <span class="pl-k">return</span> combined_transactions_data</td>
      </tr>
      <tr>
        <td id="L73" class="blob-num js-line-number" data-line-number="73"></td>
        <td id="LC73" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L74" class="blob-num js-line-number" data-line-number="74"></td>
        <td id="LC74" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L75" class="blob-num js-line-number" data-line-number="75"></td>
        <td id="LC75" class="blob-code blob-code-inner js-file-line"><span class="pl-c"><span class="pl-c">#</span> Flag = 0: Untouched</span></td>
      </tr>
      <tr>
        <td id="L76" class="blob-num js-line-number" data-line-number="76"></td>
        <td id="LC76" class="blob-code blob-code-inner js-file-line"><span class="pl-c"><span class="pl-c">#</span> Flag = 1: Okay</span></td>
      </tr>
      <tr>
        <td id="L77" class="blob-num js-line-number" data-line-number="77"></td>
        <td id="LC77" class="blob-code blob-code-inner js-file-line"><span class="pl-c"><span class="pl-c">#</span> Flag = 2: MI Outlier</span></td>
      </tr>
      <tr>
        <td id="L78" class="blob-num js-line-number" data-line-number="78"></td>
        <td id="LC78" class="blob-code blob-code-inner js-file-line"><span class="pl-c"><span class="pl-c">#</span> Flag = 3: Incorrect data. Ask admin</span></td>
      </tr>
      <tr>
        <td id="L79" class="blob-num js-line-number" data-line-number="79"></td>
        <td id="LC79" class="blob-code blob-code-inner js-file-line"><span class="pl-c"><span class="pl-c">#</span> Flag = 4: No clue. Try other method. Don&#39;t send to MI.</span></td>
      </tr>
      <tr>
        <td id="L80" class="blob-num js-line-number" data-line-number="80"></td>
        <td id="LC80" class="blob-code blob-code-inner js-file-line"><span class="pl-c"><span class="pl-c">#</span> Flag = 5: Iterate.</span></td>
      </tr>
      <tr>
        <td id="L81" class="blob-num js-line-number" data-line-number="81"></td>
        <td id="LC81" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L82" class="blob-num js-line-number" data-line-number="82"></td>
        <td id="LC82" class="blob-code blob-code-inner js-file-line"><span class="pl-k">def</span> <span class="pl-en">raise_flags</span>(<span class="pl-smi">combined_transactions_data</span>):</td>
      </tr>
      <tr>
        <td id="L83" class="blob-num js-line-number" data-line-number="83"></td>
        <td id="LC83" class="blob-code blob-code-inner js-file-line">    <span class="pl-c"><span class="pl-c">#</span> All STD should get replaced by STD/Mean and/or D/Mean</span></td>
      </tr>
      <tr>
        <td id="L84" class="blob-num js-line-number" data-line-number="84"></td>
        <td id="LC84" class="blob-code blob-code-inner js-file-line">    <span class="pl-c"><span class="pl-c">#</span> For STD&lt; 1, still find Flag #3 by checking D/Mean ratio?</span></td>
      </tr>
      <tr>
        <td id="L85" class="blob-num js-line-number" data-line-number="85"></td>
        <td id="LC85" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1</span>, <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L86" class="blob-num js-line-number" data-line-number="86"></td>
        <td id="LC86" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L87" class="blob-num js-line-number" data-line-number="87"></td>
        <td id="LC87" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L88" class="blob-num js-line-number" data-line-number="88"></td>
        <td id="LC88" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">2</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L89" class="blob-num js-line-number" data-line-number="89"></td>
        <td id="LC89" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">5</span></td>
      </tr>
      <tr>
        <td id="L90" class="blob-num js-line-number" data-line-number="90"></td>
        <td id="LC90" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L91" class="blob-num js-line-number" data-line-number="91"></td>
        <td id="LC91" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">2</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L92" class="blob-num js-line-number" data-line-number="92"></td>
        <td id="LC92" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L93" class="blob-num js-line-number" data-line-number="93"></td>
        <td id="LC93" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1.3</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Deviation_Factor<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">0.5</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">2</span></td>
      </tr>
      <tr>
        <td id="L94" class="blob-num js-line-number" data-line-number="94"></td>
        <td id="LC94" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L95" class="blob-num js-line-number" data-line-number="95"></td>
        <td id="LC95" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">2</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L96" class="blob-num js-line-number" data-line-number="96"></td>
        <td id="LC96" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L97" class="blob-num js-line-number" data-line-number="97"></td>
        <td id="LC97" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1.3</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L98" class="blob-num js-line-number" data-line-number="98"></td>
        <td id="LC98" class="blob-code blob-code-inner js-file-line">        combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Deviation_Factor<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">0.5</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L99" class="blob-num js-line-number" data-line-number="99"></td>
        <td id="LC99" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L100" class="blob-num js-line-number" data-line-number="100"></td>
        <td id="LC100" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">2</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L101" class="blob-num js-line-number" data-line-number="101"></td>
        <td id="LC101" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">1</span></td>
      </tr>
      <tr>
        <td id="L102" class="blob-num js-line-number" data-line-number="102"></td>
        <td id="LC102" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L103" class="blob-num js-line-number" data-line-number="103"></td>
        <td id="LC103" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">3</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">2</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L104" class="blob-num js-line-number" data-line-number="104"></td>
        <td id="LC104" class="blob-code blob-code-inner js-file-line">        combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>]<span class="pl-k">/</span>combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">4</span></td>
      </tr>
      <tr>
        <td id="L105" class="blob-num js-line-number" data-line-number="105"></td>
        <td id="LC105" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L106" class="blob-num js-line-number" data-line-number="106"></td>
        <td id="LC106" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">3</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">2</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L107" class="blob-num js-line-number" data-line-number="107"></td>
        <td id="LC107" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">5</span></td>
      </tr>
      <tr>
        <td id="L108" class="blob-num js-line-number" data-line-number="108"></td>
        <td id="LC108" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L109" class="blob-num js-line-number" data-line-number="109"></td>
        <td id="LC109" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">3</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">6.5</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>]<span class="pl-k">/</span>combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">5</span></td>
      </tr>
      <tr>
        <td id="L110" class="blob-num js-line-number" data-line-number="110"></td>
        <td id="LC110" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L111" class="blob-num js-line-number" data-line-number="111"></td>
        <td id="LC111" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">3</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">6.5</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L112" class="blob-num js-line-number" data-line-number="112"></td>
        <td id="LC112" class="blob-code blob-code-inner js-file-line">        combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">4</span></td>
      </tr>
      <tr>
        <td id="L113" class="blob-num js-line-number" data-line-number="113"></td>
        <td id="LC113" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L114" class="blob-num js-line-number" data-line-number="114"></td>
        <td id="LC114" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L115" class="blob-num js-line-number" data-line-number="115"></td>
        <td id="LC115" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">6.5</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">9</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L116" class="blob-num js-line-number" data-line-number="116"></td>
        <td id="LC116" class="blob-code blob-code-inner js-file-line">        combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">5</span></td>
      </tr>
      <tr>
        <td id="L117" class="blob-num js-line-number" data-line-number="117"></td>
        <td id="LC117" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[</td>
      </tr>
      <tr>
        <td id="L118" class="blob-num js-line-number" data-line-number="118"></td>
        <td id="LC118" class="blob-code blob-code-inner js-file-line">        (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">6.5</span>) <span class="pl-k">&amp;</span> (combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">9</span>) <span class="pl-k">&amp;</span> (</td>
      </tr>
      <tr>
        <td id="L119" class="blob-num js-line-number" data-line-number="119"></td>
        <td id="LC119" class="blob-code blob-code-inner js-file-line">            combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>Max_Deviation<span class="pl-pds">&#39;</span></span>] <span class="pl-k">/</span> combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&lt;=</span> <span class="pl-c1">1.3</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">4</span></td>
      </tr>
      <tr>
        <td id="L120" class="blob-num js-line-number" data-line-number="120"></td>
        <td id="LC120" class="blob-code blob-code-inner js-file-line">
</td>
      </tr>
      <tr>
        <td id="L121" class="blob-num js-line-number" data-line-number="121"></td>
        <td id="LC121" class="blob-code blob-code-inner js-file-line">    combined_transactions_data.loc[(combined_transactions_data[<span class="pl-s"><span class="pl-pds">&#39;</span>STD<span class="pl-pds">&#39;</span></span>] <span class="pl-k">&gt;</span> <span class="pl-c1">9</span>), <span class="pl-s"><span class="pl-pds">&#39;</span>Flag<span class="pl-pds">&#39;</span></span>] <span class="pl-k">=</span> <span class="pl-c1">4</span></td>
      </tr>
      <tr>
        <td id="L122" class="blob-num js-line-number" data-line-number="122"></td>
        <td id="LC122" class="blob-code blob-code-inner js-file-line">    <span class="pl-c"><span class="pl-c">#</span> combined_transactions_data.to_csv(&quot;check_5.csv&quot;)</span></td>
      </tr>
      <tr>
        <td id="L123" class="blob-num js-line-number" data-line-number="123"></td>
        <td id="LC123" class="blob-code blob-code-inner js-file-line">    <span class="pl-k">return</span> combined_transactions_data</td>
      </tr>
</table>

  <div class="BlobToolbar position-absolute js-file-line-actions dropdown js-menu-container js-select-menu d-none" aria-hidden="true">
    <button class="btn-octicon ml-0 px-2 p-0 bg-white border border-gray-dark rounded-1 dropdown-toggle js-menu-target" id="js-file-line-action-button" type="button" aria-expanded="false" aria-haspopup="true" aria-label="Inline file action toolbar" aria-controls="inline-file-actions">
      <svg aria-hidden="true" class="octicon octicon-kebab-horizontal" height="16" version="1.1" viewBox="0 0 13 16" width="13"><path fill-rule="evenodd" d="M1.5 9a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/></svg>
    </button>
    <div class="dropdown-menu-content js-menu-content" id="inline-file-actions">
      <ul class="BlobToolbar-dropdown dropdown-menu dropdown-menu-se mt-2">
        <li><a class="js-zeroclipboard dropdown-item" style="cursor:pointer;" id="js-copy-lines" data-original-text="Copy lines">Copy lines</a></li>
        <li><a class="js-zeroclipboard dropdown-item" id= "js-copy-permalink" style="cursor:pointer;" data-original-text="Copy permalink">Copy permalink</a></li>
        <li><a href="/digitalgreenorg/dg/blame/4a9d20843f0d5b2b3f11c8ca7e20f7a60183e2d6/loop_ivr/outliers/removal.py" class="dropdown-item js-update-url-with-hash" id="js-view-git-blame">View git blame</a></li>
          <li><a href="/digitalgreenorg/dg/issues/new" class="dropdown-item" id="js-new-issue">Open new issue</a></li>
      </ul>
    </div>
  </div>

  </div>

  </div>

  <button type="button" data-facebox="#jump-to-line" data-facebox-class="linejump" data-hotkey="l" class="d-none">Jump to Line</button>
  <div id="jump-to-line" style="display:none">
    <!-- '"` --><!-- </textarea></xmp> --></option></form><form accept-charset="UTF-8" action="" class="js-jump-to-line-form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
      <input class="form-control linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" aria-label="Jump to line" autofocus>
      <button type="submit" class="btn">Go</button>
</form>  </div>


  </div>
  <div class="modal-backdrop js-touch-events"></div>
</div>

    </div>
  </div>

  </div>

      
<div class="footer container-lg px-3" role="contentinfo">
  <div class="position-relative d-flex flex-justify-between py-6 mt-6 f6 text-gray border-top border-gray-light ">
    <ul class="list-style-none d-flex flex-wrap ">
      <li class="mr-3">&copy; 2018 <span title="0.31584s from unicorn-3164537304-1gwrx">GitHub</span>, Inc.</li>
        <li class="mr-3"><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li class="mr-3"><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li class="mr-3"><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li class="mr-3"><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
        <li><a href="https://help.github.com" data-ga-click="Footer, go to help, text:help">Help</a></li>
    </ul>

    <a href="https://github.com" aria-label="Homepage" class="footer-octicon" title="GitHub">
      <svg aria-hidden="true" class="octicon octicon-mark-github" height="24" version="1.1" viewBox="0 0 16 16" width="24"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
</a>
    <ul class="list-style-none d-flex flex-wrap ">
        <li class="mr-3"><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact GitHub</a></li>
      <li class="mr-3"><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li class="mr-3"><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li class="mr-3"><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li class="mr-3"><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>

    </ul>
  </div>
</div>



  <div id="ajax-error-message" class="ajax-error-message flash flash-error">
    <svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M8.865 1.52c-.18-.31-.51-.5-.87-.5s-.69.19-.87.5L.275 13.5c-.18.31-.18.69 0 1 .19.31.52.5.87.5h13.7c.36 0 .69-.19.86-.5.17-.31.18-.69.01-1L8.865 1.52zM8.995 13h-2v-2h2v2zm0-3h-2V6h2v4z"/></svg>
    <button type="button" class="flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
      <svg aria-hidden="true" class="octicon octicon-x" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M7.48 8l3.75 3.75-1.48 1.48L6 9.48l-3.75 3.75-1.48-1.48L4.52 8 .77 4.25l1.48-1.48L6 6.52l3.75-3.75 1.48 1.48z"/></svg>
    </button>
    You can't perform that action at this time.
  </div>


    
    <script crossorigin="anonymous" integrity="sha256-+xnpyXbt6GVODbcDcHIEoyLXhTRuY1OEN4fS1Kp+FA4=" src="https://assets-cdn.github.com/assets/frameworks-fb19e9c976ede8654e0db703707204a322d785346e6353843787d2d4aa7e140e.js"></script>
    
    <script async="async" crossorigin="anonymous" integrity="sha256-vVFCjnK3gGWs5GTSbu17y2cmBatQwmT/dh4+V19Qu6k=" src="https://assets-cdn.github.com/assets/github-bd51428e72b78065ace464d26eed7bcb672605ab50c264ff761e3e575f50bba9.js"></script>
    
    
    
    
  <div class="js-stale-session-flash stale-session-flash flash flash-warn flash-banner d-none">
    <svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path fill-rule="evenodd" d="M8.865 1.52c-.18-.31-.51-.5-.87-.5s-.69.19-.87.5L.275 13.5c-.18.31-.18.69 0 1 .19.31.52.5.87.5h13.7c.36 0 .69-.19.86-.5.17-.31.18-.69.01-1L8.865 1.52zM8.995 13h-2v-2h2v2zm0-3h-2V6h2v4z"/></svg>
    <span class="signed-in-tab-flash">You signed in with another tab or window. <a href="">Reload</a> to refresh your session.</span>
    <span class="signed-out-tab-flash">You signed out in another tab or window. <a href="">Reload</a> to refresh your session.</span>
  </div>
  <div class="facebox" id="facebox" style="display:none;">
  <div class="facebox-popup">
    <div class="facebox-content" role="dialog" aria-labelledby="facebox-header" aria-describedby="facebox-description">
    </div>
    <button type="button" class="facebox-close js-facebox-close" aria-label="Close modal">
      <svg aria-hidden="true" class="octicon octicon-x" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path fill-rule="evenodd" d="M7.48 8l3.75 3.75-1.48 1.48L6 9.48l-3.75 3.75-1.48-1.48L4.52 8 .77 4.25l1.48-1.48L6 6.52l3.75-3.75 1.48 1.48z"/></svg>
    </button>
  </div>
</div>


  </body>
</html>

