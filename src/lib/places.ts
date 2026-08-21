import raw from '../../content/data/places.json';

/**
 * places.json carries its own display_policy: ratings, review counts and prices
 * are held for reference and must never reach the page, because they go stale
 * and a wrong price is worse than no price.
 *
 * That policy is enforced here rather than left to each template: `rating`,
 * `reviews` and `rate_omr` are dropped at this boundary, so a page cannot render
 * them even by accident. Read the raw file if you need them for research.
 */
export type PlaceCategory = 'heritage' | 'stay' | 'eat' | 'shop' | 'services';

export type Place = {
  category: PlaceCategory;
  name_ar: string;
  name_en: string;
  coords?: string;
  plus_code?: string;
  hours?: string;
  phone?: string;
  note?: string;
  maps_url: string;
};

type RawPlace = Place & { rating?: number; reviews?: number; rate_omr?: unknown };

const file = raw as { checked: string; source: string; display_policy: string; places: RawPlace[] };

/** The date the listings were last verified. Rendered on every page that shows them. */
export const CHECKED = file.checked;
export const SOURCE = file.source;

const strip = ({ rating, reviews, rate_omr, ...rest }: RawPlace): Place => rest;

export const PLACES: Place[] = file.places.map(strip);

export const placesIn = (category: PlaceCategory) => PLACES.filter((p) => p.category === category);

export const placeName = (p: Place, lang: 'ar' | 'en') => (lang === 'ar' ? p.name_ar : p.name_en);

/**
 * Entries that have a real, mapped counterpart in places.json. Deliberately
 * explicit rather than fuzzy-matched on the title: a wrong pin sends a visitor
 * to the wrong building. Entries absent from this map simply show no location
 * card.
 */
const ENTRY_PLACE: Record<string, string> = {
  'harat-al-aqur': 'حارة العقر القديمة',
  'al-aqur-wall': 'سور حارة العقر',
  'abu-al-muthir-museum': 'متحف أبي المؤثر',
  'falaj-dawt': 'فلج ضوت',
  'shawadhna-mosque': 'مسجد الشواذنة',
  'mazaraa-mosque': 'مسجد مزارعة',
  'nizwa-fort': 'قلعة نزوى',
  'nizwa-castle': 'حصن نزوى',
  'nizwa-souq': 'سوق نزوى',
  'bait-al-sarooj': 'بيت الصاروج'
};

export const placeForEntry = (slug: string): Place | undefined => {
  const name = ENTRY_PLACE[slug];
  return name ? PLACES.find((p) => p.name_ar === name) : undefined;
};

/** Category labels, both languages. */
export const CATEGORY_LABELS = {
  ar: { heritage: 'مواقع تاريخية', stay: 'نُزُل وإقامة', eat: 'مطاعم ومقاهٍ', shop: 'متاجر', services: 'خدمات' },
  en: { heritage: 'Heritage sites', stay: 'Places to stay', eat: 'Food and coffee', shop: 'Shops', services: 'Services' }
} as const;
