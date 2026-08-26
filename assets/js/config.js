/*
  Cleaned By Pressure — site configuration
  Fill in the placeholder values below once you have them. Nothing else in
  the codebase needs to change — every page reads from this file.
*/
window.SITE_CONFIG = {
  businessName: "Cleaned By Pressure",
  phoneDisplay: "(623) 692-1436",
  phoneHref: "tel:+16236921436",
  smsHref: "sms:+16236921436",
  emailAddress: "info@cleanedbypressure.com",
  domain: "https://cleanedbypressure.com",

  // City/region shown in copy + schema. Update if you serve a different area.
  serviceAreaCities: [
    "Glendale", "Peoria", "Surprise", "Avondale",
    "Goodyear", "Buckeye", "El Mirage", "Litchfield Park", "Sun City"
  ],
  serviceAreaRegion: "West Valley Phoenix, AZ",
  serviceAreaStateAbbr: "AZ",

  // TODO: paste your real Google Place ID here (Place ID Finder:
  // https://developers.google.com/maps/documentation/places/web-service/place-id)
  googlePlaceId: "PASTE_GOOGLE_PLACE_ID_HERE",
  googleBusinessProfileUrl: "https://share.google/0c6fOx63fVCieapQo",

  // TODO: paste the numeric widget ID from your Elfsight "Google Reviews"
  // widget dashboard (elfsight.com) after you create a free account.
  elfsightWidgetId: "", // e.g. "abcd1234-5678-90ef-ghij-klmnopqrstuv"

  // TODO: paste your Tawk.to property ID + widget ID after creating a free
  // account at tawk.to (Admin > Channels > Chat Widget > "Widget Code").
  tawkToPropertyId: "",
  tawkToWidgetId: "",

  // Star rating + review count shown in the static fallback / schema until
  // the live widget is wired up. Update to match your real Google rating.
  aggregateRating: {
    ratingValue: "5.0",
    reviewCount: "1"
  }
};
