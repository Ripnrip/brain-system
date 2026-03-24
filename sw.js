/* Service Worker for Brain Search PWA */
const CACHE_NAME = 'brain-search-v1';
const API_CACHE_NAME = 'brain-api-v1';

// Cache strategies
const CACHE_STRATEGIES = {
    // Static assets - cache first, fallback to network
    static: {
        cacheName: CACHE_NAME,
        strategy: 'cacheFirst'
    },
    // API responses - network first, fallback to cache with short TTL
    api: {
        cacheName: API_CACHE_NAME,
        strategy: 'networkFirst',
        maxAge: 5 * 60 * 1000 // 5 minutes
    }
};

// Assets to cache on install
const PRECACHE_ASSETS = [
    '/',
    '/manifest.json'
];

// Install event - cache core assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(PRECACHE_ASSETS.map(url => new Request(url, {cache: 'reload'})))
                .catch(err => console.log('Precache failed:', err));
        })
    );
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter(name => name.startsWith('brain-') && name !== CACHE_NAME && name !== API_CACHE_NAME)
                    .map(name => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Only handle same-origin requests
    if (url.origin !== self.location.origin) {
        return;
    }

    // API requests - network first with cache fallback
    if (url.pathname.startsWith('/search') || url.pathname.startsWith('/api/') || url.pathname.startsWith('/graph')) {
        event.respondWith(handleAPIRequest(request));
        return;
    }

    // Static assets - cache first
    if (request.method === 'GET') {
        event.respondWith(handleStaticRequest(request));
        return;
    }
});

// Network-first strategy for API requests
async function handleAPIRequest(request) {
    const cache = await caches.open(API_CACHE_NAME);
    const cachedResponse = await cache.match(request);

    // Check if cached response is still valid (within maxAge)
    if (cachedResponse) {
        const cacheDate = new Date(cachedResponse.headers.get('date') || Date.now());
        const age = Date.now() - cacheDate.getTime();

        if (age < CACHE_STRATEGIES.api.maxAge) {
            // Return cached response, fetch in background
            fetchAndCache(request, cache);
            return cachedResponse;
        }
    }

    // No valid cache, fetch from network
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            await cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        // Network failed, return stale cache if available
        if (cachedResponse) {
            return cachedResponse;
        }
        // Return offline response
        return new Response(JSON.stringify({ offline: true, results: [] }), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Cache-first strategy for static assets
async function handleStaticRequest(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
        return cachedResponse;
    }

    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        // Return cached index.html for navigation requests
        if (request.mode === 'navigate') {
            return cache.match('/') || new Response('Offline - No cached content', {
                status: 503,
                headers: { 'Content-Type': 'text/plain' }
            });
        }
        throw error;
    }
}

// Background fetch and cache (non-blocking)
function fetchAndCache(request, cache) {
    fetch(request).then(response => {
        if (response.ok) {
            cache.put(request, response);
        }
    }).catch(() => {
        // Silently fail - this is just background sync
    });
}

// Background sync for queued searches
self.addEventListener('sync', (event) => {
    if (event.tag === 'brain-search-sync') {
        event.waitUntil(syncQueuedSearches());
    }
});

// Process queued searches from IndexedDB
async function syncQueuedSearches() {
    // This would integrate with IndexedDB to process queued searches
    // For now, it's a placeholder for the background sync feature
    try {
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({ type: 'SYNC_COMPLETE' });
        });
    } catch (error) {
        console.log('Sync failed:', error);
    }
}

// Handle messages from clients
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then(names => Promise.all(
                names.map(name => caches.delete(name))
            ))
        );
    }
});
