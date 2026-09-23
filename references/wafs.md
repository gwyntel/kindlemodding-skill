# WAFs & Mesquite

## Overview
WAF = Kindle "application" = webapp in fancy wrapper. Mesquite = runtime loading them.
- WAF folder: `/opt/var/local/mesquite/<name>/`, e.g. `/opt/var/local/mesquite/store`
- Declare WAF in `/opt/var/local/appreg.db` to make it launchable
- Every WAF has `config.xml` with launch metadata
- Optional `strings/` folder pattern: `locales/<locale>/strings/strings.js` for localisation
- `window.kindle` object in every WAF = JS-to-system bridge. Enabled APIs controlled by `<feature>` params in config.xml

`kindle` object properties:
- `kindle.version` = `1` (int, API version?)
- Local-dev mock build only: `kindle.isMock` = `1`, `kindle.extensions` = `{}`

## config.xml structure
Root: `<widget id="com.lab126.store" version="1.0" viewmodes="application" xmlns="http://www.w3.org/ns/widgets" xmlns:kindle="http://kindle.amazon.com/ns/widget-extensions">`
- `id` = unique Java-like namespace (any unique value OK)
- `viewmodes` = `application` (only known value)

Sections:
- `<name xml:lang="en">` / `<description xml:lang="en">` — display name/desc, `xml:lang` localised, unicode entities allowed
- `<content src="index.html" />` — entry file loaded on launch
- `<kindle:permissions>` — special permissions:
  - `<kindle:permission name="local-port-access" />` — localhost access (DB interface port 9101)
  - `<kindle:permission name="download-allowed" />` — download to `documents` folder
- `<kindle:network>` — networking:
  - `<kindle:asset key="user-agent" value="kindle://device-type" />` / `kindle://sw-version` / `kindle://pretty-sw-version` / custom UA string
  - `<kindle:asset key="http-header" value="kindle://transport-method" />` / `kindle://country-code`
  - `initialDNS`, `maxConnections` (6), `maxConnectionsPerHost` (2), `maxConnectionsPerProxy` (6), `overrideProxy` (`none` or URL), `enableCaching` (`false`)
  - browser WAF extras: `enableWrsProxy`=`true`, `allowTlsFallback`=`true`
  - `<kindle:errorPage src="..." />` — error page for failed loads
  - `enableCaching` does NOT cache WAF itself
- `<kindle:cookiejar>` — cookie policy:
  - `persistent`=`true`, `usePrivateCookies`=`false`, `useDeviceCookies`=`true`, `useAccessToken`=`true`
- `<kindle:chrome>`:
  - `<kindle:asset key="configureSearchBar" value="system" />` — known values `system`, `none`
- `<kindle:gestures>` — gesture config, feeds `kindle.gestures` API:
  - `<kindle:param name="tap" value="yes" properties="fire_on_tap:1 max_updown_delta:0" />`
  - `<kindle:param name="swipe" value="yes" />`
  - browser WAF: `drag`, `pinchzoom` (`properties="fire-on-zoom:1"`), `tap`, `multi_tap`, `hold`
- `<feature name="http://kindle.amazon.com/apis" required="true">` — toggles `kindle` sub-APIs. Params (value `yes`/`no`): `appmgr`, `net`, `todo`, `gestures`, `chrome`, `dev`, `dconfig`, `download`, `messaging`, `uitest`, `popup`, `bkgrnd`, `localprefs`, `device`, `winmgrUtils`, `bluetooth`
- `<kindle:messaging>` — whitelist of LIPC services callable via `kindle.messaging`, e.g. `<kindle:app name="com.lab126.pillow" value="yes" />`
- `<kindle:resources>` — local JS resources + storage quotas:
  - `<kindle:asset key="jquery" value="js/jquery.js" />`, `<kindle:asset key="sprite_v1" value="js/sprite_v1.js" />`
  - `AllowHTTPSApplicationManifestCrossDomain`=`true`, `ApplicationCachePath`=`/var/local/mesquite/store/resource/appcache`, `ApplicationCacheLoadDelay`=`6.0`, `LocalStorageQuota`=`26214400`
  - Other known keys: `LocalStoragePath`, `DatabaseStorageQuota`, `DatabaseStoragePath`, `ApplicationCacheQuota`
- `<kindle:settings>` — runtime settings:
  - store: `internetRequired`=`yes`, `saveContext`=`no`, `disable-wua-features`=`yes`
  - browser: `defaultFontSize`=`6`, `defaultFontSize300`=`6`, `defaultFontSize212`=`9`, `defaultFontSize167`=`9`, `zoomFactor`=`8.0`, `minimumFontSize`=`0`, `flattenFrames`=`yes`, `debug`=`no`
  - payment: `enforce96DPI`=`yes`, `enableW3CStd`=`yes`
- Read: parse XML, edit section, redeploy. Modify: change `value` attrs, add/remove `<kindle:param>`/`<param>` entries, keep `xmlns:kindle` namespace.

## kindle.chrome
Titlebar + dialog + content windows. Page WIP/incomplete.
- `isDecanterChromeEnabled` = `true` (boolean; firmware-version related)

Methods:
- `kindle.chrome.setTitleBar(centerText, leftText)` — sets title bar texts; possibly deprecated on modern firmware
- `kindle.chrome.createHeader(uri, height, tiled)` — uri string, height integer, tiled boolean; usage unknown
- `kindle.chrome.createDialog(uri, width, height, modal)` — creates visible dialog. uri: String (local file OK? unknown). width: Integer px. height: Integer px. modal: Boolean (usually `true`)
- `kindle.chrome.setSpinnerState(state, timeout, delay)` — titlebar spinner. state: String `start`|`stop`. timeout: Integer (max display time, units unknown). delay: Integer (wait before spinning). timeout+delay still required when state=`stop` (ignored but expected — `JSObjectChrome::setSpinnerState expects three arguments`)
- `kindle.chrome.createContentWindow(uri)` — usage unknown, returns window object/string. Content windows not fully understood
- `kindle.chrome.setContentWinDisplay(displayState)` — displayState: String `foreground`|`background` (show/hide)
- `kindle.chrome.setJavaScript(enabled)` — JS execution in contentWindow. enabled: String `enabled`|`disabled`
- `kindle.chrome.setImageRendering(enabled)` — image rendering in contentWindow. enabled: String `on`|`off`
- `kindle.chrome.onContentStart()` — overridable; fires on content load start
- `kindle.chrome.onContentProgress(progress)` — overridable; progress decimal 0–1
- `kindle.chrome.onContentUrlChanged(url)` — overridable; url String of new navigation target
- `kindle.chrome.onContentTitleChanged(title)` — overridable; title String of new contentWindow title
- `kindle.chrome.registerWindowOpenEventListener(callback)` — unknown purpose; callback called with url String

## kindle.dconfig
Store-specific config values. Purpose not fully known.
- `kindle.dconfig.getValue(key)` — returns config string for key. Known keys:
  - `url.store` = `https://www.amazon.co.uk/gp/digital/juno/index.html` — store WAF URL
  - `amz.cor` = `GB` — CORS-related?
  - `url.cantilever` = `https://digprjsurvey$DOMAIN/csad/workflow/ed89e52d` — `$DOMAIN` replaced at runtime
  - `marketplace.obfuscated.id` — 14-char alphanumeric (sensitive, not shared)
  - `url.ku.eligible` = `/gp/kindle/ku/sign-up/ajax/is-customer-eligible` — Kindle Unlimited
  - `url.ku.landing.page` = `/gp/kindle/ku/sign-up/ui/juno/upsell/ref=`
  - `url.mysn.reap` = `https://rexp-auth-proxy.amazon.cn/social_device_auth`
  - `url.odac` = `https://www.amazon.com`
  - `cmd.account.registration` = `gp/kw/land`
  - `url.website` = `https://www.amazon.co.uk` — used by `payment` WAF
  - `url.kindlestore.kcw.metrics` = `/mn/kcw/workflow/log-metrics` — used by `payment` WAF
  - `store.disableDiskFileUse` — returns nothing; used in `if` statement
  - `mesquite.interceptorIndicator` — 32-char alphanumeric (sensitive, not shared); used with hash fragment for cache-trigger URLs

## kindle.dev
Device property functions. Similar to `kindle.device` with differences. Docs incomplete/may be inaccurate.
- `contactInfo` = `'Your System Administrator'`
- `eid` = `BASE64 ENCODED DATA`
- `getRegistrationState` = `'registered'`
- `hasScreenLight` = `true`
- `hasKindleStoreAccess` = `true`
- `isWirelessMenuEnabled` = `true`
- `controlStatus` = `0` — `1` = Device Control, `2` = Parental, `3` = No Control

Methods:
- `kindle.dev.setSensitivity(useThreshold, threshold)` — eInk refresh sensitivity. useThreshold: Boolean (`false` = refresh normal, omit threshold). threshold: Integer 0–100 (`100` = refresh much more than `0`)
- `kindle.dev.setOrientation(orientation)` — screen orientation. Invalid string = no-op. Valid values: orientations enum
- `kindle.dev.getDPI()` — returns device DPI
- `kindle.dev.hasWirelessMenu()` — returns boolean
- `kindle.dev.log(logServiceName, logString, logLevel)` — writes to Kindle log. Params named `logEvent`/`logMsg`/`logLevel` in firmware. logLevel: `info`, `warn`, `error`, `debug`, `perf`. Kindle logs ARE sent to Amazon — be careful
- `kindle.dev.getLab126SessionToken()` — session token for internal DB API
- `kindle.dev.loadResource(frameId, resourceId)` — loads local JS file into any frame (XSS override). File must be declared in WAF config.xml. frameId: String DOM id, top frame = `_self`. resourceId: String identifier from config.xml, must be valid local file
- `kindle.dev.addDomainToWhitelist(uri, addSubDomains)` — adds URI to allowed domain list. uri: String e.g. `http://amazon.com`. addSubDomains: String `'true'`|`'false'`
- `kindle.dev.clearCookies()` — clears app cookie jar. On Mesquito: clears ALL cookies across ALL Mesquito apps → permanent blacklist. Warned.
- `kindle.dev.clearApplicationCache()` — clears app HTML cache. On Mesquito: may break Mesquito → permanent blacklist. Warned.
- `kindle.dev.clearCache()` — clears in-memory cached resources. Mesquito: buggy/annoying, avoid
- `kindle.dev.getMPDomain()` — marketplace domain. Seemingly non-functional. Firmware calls `.amazon.cn` the `CHINESE_OBFUSCATED_MARKETPLACE`
- `kindle.dev.getBaiduSearchURL()` — returns `https://www.baidu.com/s?tn=baiduhome_pg&ie=utf-8&rn=4&wd=`
- `kindle.dev.disableSecureApis()` — `payment` WAF related; disables "secure APIs" on non-Amazon URLs
- `kindle.dev.getRegisteredUserId()` — userId string; tracks registration change
- `kindle.dev.getDSN()` — returns string, purpose unknown
- `kindle.dev.getDeviceLocale()` — locale string, e.g. `en_GB`
- `kindle.dev.getDeviceTypeString()` — device type string, e.g. `malbec`

## kindle.device
Same properties as `kindle.dev` (contactInfo, eid, getRegistrationState, hasScreenLight, hasKindleStoreAccess, isWirelessMenuEnabled, controlStatus). Shares these methods with `kindle.dev`: `setSensitivity`, `setOrientation`, `getDPI`, `hasWirelessMenu`, `log`, `getLab126SessionToken`, `loadResource`, `addDomainToWhitelist`, `clearCookies`, `clearApplicationCache`, `clearCache`, `getMPDomain`, `getBaiduSearchURL`, `disableSecureApis`. Differences:
- `getMPDomain` documented as functional here (no non-functional warning)
- Extra methods below, not present on `kindle.dev`:
- `kindle.device.isInDemoMode()` — Boolean, `true` if demo mode
- `kindle.device.getSoftwareVersionNumber()` — int, e.g. `5.15.1.1` = `3924990005`
- `kindle.device.getSoftwareVersionString()` — string, e.g. `"1.15.1.1"`
- `kindle.device.getASRMode()` — number, meaning unknown (`0` on tested Kindle)
- `kindle.device.getCSSPixelsPerInch()` — CSS pixels per inch
- `kindle.dev` has these not on `kindle.device`: `getRegisteredUserId`, `getDSN`, `getDeviceLocale`, `getDeviceTypeString`

## kindle.gestures
Overridable gesture callbacks. Enable via `<kindle:gestures>` in config.xml. Only `onswipe` and `ontap` work on Mesquito (store config.xml limitation). Section UNFINISHED.
- `kindle.gestures.onswipe(direction, pageX, pageY)` — direction: String (direction enum), pageX/pageY: swipe location
- `kindle.gestures.onflick(direction)` — direction: String (direction enum)
- `kindle.gestures.onpan(event)` — event content unknown
- `kindle.gestures.onpinch(event)` — event content unknown
- `kindle.gestures.onhold(event)` — event content unknown
- `kindle.gestures.onzoom(event)` — zoom gesture; event content unknown (firmware shows `onzooms`)
- `kindle.gestures.ontap(event)` — event content unknown

## kindle.messaging
LIPC messaging (Kindle IPC). Whitelisted services declared in `<kindle:messaging>` of config.xml. Page WIP.
- `kindle.messaging.sendMessage(id, eventType, eventData)` — eventData: Object. Example: id=`com.lab126.chromebar`, eventType=`configureChrome`, eventData=`{appId:'com.lab126.store', topNavBar:{template:'title', title:"Mesquito Loader"}}`
- `kindle.messaging.sendStringMessage(id, eventType, eventData)` — eventData: String. Example: id=`com.lab126.mfa`, eventType=`switchViewMode`, eventData=`fullscreen`
- `kindle.messaging.recieveMessage(eventType, callback)` — note spelling `recieveMessage`. Registers callback for LIPC messages sent to WAF. Callback: `callback(property, json)` — property: String = eventType, json: data payload (or string)

## kindle.net
Network functions.
- `backgroundRequestHeader` = `'WAF-HTTP-REQUEST-BACKGROUND-HEADER'`
- `roaming` = `false` (3G roaming)
- `rffSessionId` = `''`

Methods:
- `kindle.net.getWirelessState()` — returns String `'on'`|`'off'`
- `kindle.net.getActiveInterface()` — returns String of connectionTypes enum
- `kindle.net.setWirelessPrompt(promptLevel)` — promptLevel: connectionPromptLevels enum
- `kindle.net.confirmSSLException(confirm, callback)` — accept/cancel last invalid cert. confirm: `'yes'`|`'no'`. callback optional, params unknown
- `kindle.net.ensureWifiConnection(promptLevel, callback)` — ensures WiFi. promptLevel: connectionPromptLevels. callback gets `response` String: `'success'` on success; see connectionResults
- `kindle.net.ensureConnection(promptLevel, forceConnect, callback)` — ensures any connection. promptLevel: connectionPromptLevels. forceConnect: Boolean. callback gets single String: connectionResults values
- `kindle.net.registerHttpErrorListener(onHttpError)` — callback args in order: `onHttpError(internalCode, uri, httpStatus, responseMessage)` — internalCode: String error description, uri: accessed URI, httpStatus: HTTP status code, responseMessage: HTTP response message
- `kindle.net.deregisterHttpErrorListener()` — no args; removes registered http error handlers

## kindle.todo
`ToDo` = internal Kindle-to-Amazon communication (book downloads, screensavers, store updates, telemetry).
- `kindle.todo.scheduleItems(items)` — items: String in Todo XML format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <total_count>1</total_count>
    <items>
        <item priority="1" type="WISHLIST" action="REFRESH" key="DUMMY" is_incremental="false" sequence="0"></item>
    </items>
</response>
```

- `contentId` = `action.type`, e.g. `REFRESH.WISHLIST`. Item attributes: `priority` (int), `type` (action type), `action` (action to perform), `key` (unique string or `"DUMMY"`). Other attributes arbitrary, passed to handler.

## Enums
String constants used/returned by kindle APIs. Taken from firmware `/opt/var/local/mesquite` (sqsh).

- `connectionPromptLevels`: `all` (prompt for everything), `never` (auto-connect), `nocaptive` (prompt except captive portal)
- `connectionResults`: `success`, `failure-user-canceled`, `failure`, `failure-captive-portal`
- `scrollBarStates`: `auto`, `hidden`, `visible`
- `fileDownloadResults`: `success`, `error`, `canceled`, `rejected` (non-downloadable file type)
- `eInkRefreshModes`: `auto`, `minimal`, `maximal`, `manual` (no refresh unless called directly)
- `connectionTypes`: `wifi`, `wan` (3G), `none` (airplane mode)
- `orientations`: `auto`, `portrait` (auto), `portraitUp`, `portraitDown` (upside down), `landscape` (auto), `landscapeLeft` (clockwise), `landscapeRight` (anticlockwise)
- `direction`: `up`, `down`, `left`, `right`
- `alignment`: `top`, `buttom` (sic — firmware spelling), `center`, `left`, `right`
- `pillow.buttons`: `back`, `store`, `home`, `forward`, `menu`, `refresh`, `cancel`, `discovery`, `KPP_BACK` (Decanter Chrome back), `KPP_CLOSE` (Decanter Chrome close)
- `pillow.buttonStates`: `enabled`, `disabled`, `false` (boolean — button hidden, NOT a string)
- `pillow.buttonHandling`: `system` (handled by Kindle), `notifyapp` (handled by WAF)
- `pillow.contextMenuIDs`: `browserSettings`, `browserBookmarks`, `browserBookmarkPage`, `browserHistory`, `browserArticleOrWebMode` (meanings unknown)
- `pillow.contextMenuStates`: `enabled`, `disabled`
