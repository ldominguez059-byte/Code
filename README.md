# Cleaned By Pressure — Website

Static site (no build step) for cleanedbypressure.com, ready to deploy on Netlify.

## Structure
- `index.html`, `services.html`, `service-areas.html`, `about.html`, `contact.html`, `thank-you.html`
- `assets/css/style.css` — all styling
- `assets/js/config.js` — **single place to edit business info + widget IDs**
- `assets/js/main.js` — nav, reviews widget loader, chat widget loader, FAQ schema

## Finish setup (3 things)

1. **Google Reviews widget** — sign up free at [elfsight.com](https://elfsight.com), add a "Google Reviews" widget pointed at your business, then paste the widget ID into `elfsightWidgetId` in `assets/js/config.js`. Until then, the site shows a static reviews section with a link straight to your real Google reviews.
2. **Live chat widget** — sign up free at [tawk.to](https://tawk.to), create a property, and paste your Property ID + Widget ID into `tawkToPropertyId` / `tawkToWidgetId` in `assets/js/config.js`.
3. **Google Place ID** — use the [Place ID Finder](https://developers.google.com/maps/documentation/places/web-service/place-id) to look up "Cleaned By Pressure" and paste it into `googlePlaceId` in `assets/js/config.js`. Also update the `aggregateRating` (real star rating + review count) in the same file and in the JSON-LD block at the top of `index.html`.

## Netlify Forms

The quote form on `contact.html` uses [Netlify Forms](https://docs.netlify.com/forms/setup/) — no backend needed. Once deployed on Netlify, submissions show up under **Site settings → Forms**. Turn on email notifications there to get texted/emailed on each new lead.

## Deploying

This repo is already meant to connect to your existing Netlify site (linked to your GoDaddy domain). Point that Netlify site at this repo/branch, or drag-and-drop the folder into Netlify's deploy UI. No build command is needed — publish directory is `.`.

## Content to double-check

Everything is written for a **West Valley, AZ (Glendale/Peoria/Surprise/Avondale/Goodyear/Buckeye)** service area based on your 623 area code — update `serviceAreaCities` in `config.js` and the matching text in `service-areas.html` if that's not accurate. Sample star testimonials on the homepage are placeholders — swap for real quotes once you have some, or remove them once the live reviews widget is connected.
