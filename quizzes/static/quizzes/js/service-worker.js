// Names of the caches used by the service worker
const CACHE_NAME = 'static-cache-v1';
const DATA_CACHE_NAME = 'data-cache-v1';

// List of local resources we want to cache
const FILES_TO_CACHE = [
  '/',
  '/static/quizzes/css/styles.css',
  '/static/quizzes/js/app.js',
  '/static/quizzes/images/favicon.ico',
  '/quizzes/', // Adjust paths as necessary to match your app structure
  '/quizzes/packages/',
  '/quizzes/contact/',
  '/quizzes/login/'
];

// Install
self.addEventListener('install', (evt) => {
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Your files were pre-cached successfully!');
      return cache.addAll(FILES_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate the service worker and remove old data from the cache
self.addEventListener('activate', (evt) => {
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME && key !== DATA_CACHE_NAME) {
          console.log('Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();
});

// Fetch
self.addEventListener('fetch', (evt) => {
  if (evt.request.url.includes('/quizzes/')) {
    evt.respondWith(
      caches.open(DATA_CACHE_NAME).then((cache) => {
        return fetch(evt.request)
          .then((response) => {
            // If the response was good, clone it and store it in the cache.
            if (response.status === 200) {
              cache.put(evt.request.url, response.clone());
            }
            return response;
          })
          .catch((err) => {
            // Network request failed, try to get it from the cache.
            return cache.match(evt.request);
          });
      }).catch((err) => console.log(err))
    );
  } else {
    evt.respondWith(
      caches.match(evt.request).then((response) => {
        return response || fetch(evt.request);
      })
    );
  }
});

