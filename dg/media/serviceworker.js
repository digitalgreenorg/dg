const urlsToCache = [
  "/coco/coco/",
  "/qacoco/",
  "/coco/faq/",
  "/media/assets/manifest.json",
  "/media/assets/images/CocoLogo_FullAll_Primary.png",
  "/media/assets/images/icons/manifest-icon-192.maskable.png",
  "/media/assets/images/icons/manifest-icon-512.maskable.png",
  "/media/configs.js",
  "/media/qa_config.js",
  "/media/coco/dist/scripts/main.js",
  "/media/coco/dist/scripts/qa_main.js",
  "/media/coco/app/scripts/libs/require.js",
  "/media/coco/app/scripts/libs/bootstrap/css/bootstrap.css",
  "/media/coco/app/scripts/libs/datatablejs_media/css/demo_table.css",
  "/media/coco/app/scripts/libs/tabletools_media/css/dataTables.tableTools.css",
  "/media/coco/app/scripts/libs/bootstrap/img/glyphicons-halflings.png",
  "/media/coco/app/scripts/libs/bootstrap/fonts/glyphicons-halflings-regular.woff",
  "/media/coco/app/scripts/libs/bootstrap/fonts/glyphicons-halflings-regular.ttf",
  "/media/coco/app/scripts/libs/bootstrap/fonts/glyphicons-halflings-regular.svg",
  "/media/coco/app/scripts/libs/bootstrap/fonts/glyphicons-halflings-regular.eot",
  "/media/img/admin/nav-bg.gif",
  "/media/coco/app/styles/css/coco.css",
  "/media/coco/app/styles/css/datepicker.css",
  "/media/coco/app/styles/css/bootstrap-timepicker.css",
  "/media/coco/app/scripts/libs/chosen-select/chosen.css",
  "/media/coco/app/styles/css/chosen-magic.css",
  "/media/coco/app/styles/css/tabletools_custom.css",
  "/media/coco/app/scripts/libs/datatablejs_media/images/back_disabled.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/back_enabled_hover.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/back_enabled.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/favicon.ico",
  "/media/coco/app/scripts/libs/datatablejs_media/images/forward_disabled.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/forward_enabled_hover.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/forward_enabled.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/sort_asc_disabled.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/sort_asc.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/sort_both.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/sort_desc_disabled.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/sort_desc.png",
  "/media/coco/app/scripts/libs/datatablejs_media/images/Sorting%20icons.psd",
  "/media/coco/app/images/loading_text.gif",
  "/media/coco/app/scripts/libs/chosen-select/chosen-sprite.png",
  "/media/coco/app/styles/css/chosen-sprite.png",
  "/media/coco/app/images/offline.png",
  "/media/coco/app/images/online.png",
  "/media/coco/app/images/add.png",
  "/media/coco/app/images/table.png",
  "/media/coco/app/images/sync.png",
  "/media/coco/app/images/feedback.png",
  "/media/coco/app/images/default.png",
  "/media/coco/app/images/dg4.png",
  "/media/coco/app/images/logo.png",
  "/media/coco/app/images/favicon.ico",
  "/media/coco/app/images/coco_logo.png",
  "/media/coco/app/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
  "/media/assets/fonts/sourcesanspro-light-webfont.woff",
  "/media/assets/fonts/sourcesanspro-lightitalic-webfont.woff",
  "/media/assets/fonts/sourcesanspro-bold-webfont.woff",
  "/media/assets/fonts/sourcesanspro-bolditalic-webfont.woff",
  "/media/assets/fonts/sourcesanspro-black-webfont.woff",
  "/media/assets/fonts/sourcesanspro-blackitalic-webfont.woff",
  "/media/assets/fonts/sourcesanspro-regular-webfont.woff",
  "/media/assets/fonts/sourcesanspro-italic-webfont.woff",
  "/media/assets/fonts/sourcesanspro-extralight-webfont.woff",
  "/media/assets/fonts/sourcesanspro-extralightitalic-webfont.woff",
  "/media/assets/fonts/sourcesanspro-semibold-webfont.woff",
  "/media/assets/fonts/sourcesanspro-semibolditalic-webfont.woff",
];

// Name of the cache to store the above resources to
const CACHE_NAME = "coco-cache-v2";
// Specify allowed cache keys
const ALLOWED_CACHES_LIST = ["coco-cache-v2"];

self.addEventListener("install", function (event) {
  // Add all the assets in the array to the cache instance for later use.
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(urlsToCache);
      })
      .catch((error) => {
        console.log("Error in service worker while caching ", error);
      })
  );
});

self.addEventListener("activate", function (event) {
  // Get all the currently active `Cache` instances.
  event.waitUntil(
    caches.keys().then((keys) => {
      // Delete all caches that aren't in the allow list:
      return Promise.all(
        keys.map((key) => {
          if (!ALLOWED_CACHES_LIST.includes(key)) {
            return caches.delete(key);
          }
        })
      );
    })
  );
});

self.addEventListener("fetch", (event) => {
  // Serve from cache if the request is same-origin else fetch from server
  event.respondWith(
    caches
      .match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
      .catch((error) => {
        console.log("Error in service worker ", error);
      })
  );
});
