const CACHE_NAME = 'hangarin-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/soft-ui-dashboard.min.css',
    '/static/css/nucleo-icons.min.css',
    '/static/css/form.min.css',
    '/static/css/widget.min.css',
    '/static/css/soft-ui-dashboard.css',
    '/static/css/widget.css',
    '/static/css/form.css',
    '/static/css/nucleo-svg.css',
    '/static/css/nucleo-icons.css',
    '/static/css/custom.css',
    '/static/css/bootstrap.css',
    '/static/js/core/jquery.3.2.1.min.js',
    '/static/js/plugin/jquery-ui-1.12.1.custom/jquery-ui.min.js',
    '/static/js/core/popper.min.js',
    '/static/js/core/bootstrap.min.js',
    '/static/js/ready.min.js',
    'https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Itim&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    '/static/img/profile_ko.jpg'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});