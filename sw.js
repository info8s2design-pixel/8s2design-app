const CACHE='8s2design-v1.2.9';
const CORE=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/favicon.ico','./icons/favicon-32.png','./icons/favicon-48.png','./icons/apple-touch-icon.png','./assets/home-trasformiamo.jpg','./assets/prenota-call.jpg','./assets/perche-8s2design.jpg','./assets/offerta-bcard-originale.jpg','./assets/garanzie-originale.jpg'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(CORE)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(Promise.all([caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('8s2design-')&&key!==CACHE).map(key=>caches.delete(key)))),self.clients.claim()])));
self.addEventListener('fetch',event=>{
 const request=event.request;
 if(request.method!=='GET'||new URL(request.url).origin!==self.location.origin)return;
 const url=new URL(request.url);
 const isBlog=url.pathname.endsWith('/data/blog.json');
 const isAsset=/\/(assets|icons)\//.test(url.pathname);
 if(isBlog){event.respondWith(fetch(request,{cache:'no-store'}).catch(()=>caches.match(request)));return;}
 if(isAsset){event.respondWith(caches.match(request).then(hit=>hit||fetch(request).then(response=>{if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)));}return response;})));return;}
 event.respondWith(fetch(request,{cache:'no-store'}).then(response=>{if(response.ok){const copy=response.clone();event.waitUntil(caches.open(CACHE).then(cache=>cache.put(request,copy)));}return response;}).catch(async()=>await caches.match(request)|| (request.mode==='navigate'?await caches.match('./index.html'):Response.error())));
});
