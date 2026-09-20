const CACHE_NAME = 'island-radio-v1';

const urlsToCache = [
    './',
    './index.html',
    './css/base.css',
    './css/player.css',
    './css/browse.css',
    './js/main.js',
    './js/player.js',
    './js/store.js',
    './data/stations.json',
    './images/icon.svg'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});
