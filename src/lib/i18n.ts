export const LANGS = ['ar', 'en'] as const;
export type Lang = (typeof LANGS)[number];

export const DEFAULT_LANG: Lang = 'ar'; // Arabic is primary; English is the secondary view.

export const dirOf = (lang: Lang) => (lang === 'ar' ? 'rtl' : 'ltr');
export const otherLang = (lang: Lang): Lang => (lang === 'ar' ? 'en' : 'ar');

/** Build an in-site URL. Every link goes through here so a future `base` is a one-line change. */
export const href = (lang: Lang, path = '') => `/${lang}${path ? `/${path.replace(/^\//, '')}` : ''}`;

export const isLang = (v: unknown): v is Lang => LANGS.includes(v as Lang);

export const ui = {
  ar: {
    siteName: 'حارة العقر',
    siteQualifier: 'نــزوى',
    tagline: 'الحارة المسوّرة في قلب نزوى',
    nav: { discover: 'اكتشف', map: 'الخريطة', route: 'الجولة', visit: 'أكل وإقامة', credits: 'الكتاب' },
    toggleLabel: 'English',
    toggleTitle: 'اعرض هذه الصفحة بالإنجليزية',
    skipToContent: 'تخطَّ إلى المحتوى',
    readMore: 'اقرأ المدخل',
    backToDiscover: 'كل المداخل',
    entriesTitle: 'اكتشف الحارة',
    entriesLead: 'واحدٌ وثلاثون مدخلاً عن مساجد الحارة وأبراجها وأفلاجها وبيوتها، منقولة من الكتاب نفسه.',
    mapTitle: 'مخطط السور',
    routeTitle: 'الجولة',
    routeLead: 'تسع محطات، تتبع الأرض لا ترتيب الكتاب: تبدأ من الصِباح الذي يحمل المتحف، وتمشي على السور المرمَّم، ثم تدخل الحارة وتنتهي في السوق.',
    routeOrderNote: 'الترتيب اقتراحٌ منّا، لا حكمٌ على الأرض. أمّا الكلام في كل محطة فمن الكتاب نفسه.',
    routeNoTimes: 'لا أوقات ولا مسافات',
    routeNoTimesBody: 'لم يقس أحدٌ زمن المشي بين المحطات ولا الأطوال بينها، فلن تجد هنا «نحو ساعتين» ولا «ست دقائق». المسافة الوحيدة المذكورة في الكتاب هي طول السور: نحو كيلومترين.',
    routeStop: 'محطة',
    routeGone: 'اندثرت، وبقي مكانها',
    routeStart: 'تبدأ من',
    routeOnPlan: 'على المخطط',
    routeReadEntry: 'اقرأ المدخل',
    visitTitle: 'أكل وإقامة',
    sourceNoteTitle: 'المصادر تختلف هنا',
    fromTheBook: 'من الكتاب',
    lastChecked: 'آخر تحقّق',
    figuresTitle: 'الحارة بالأرقام',
    photoCredit: 'من صور الكتاب',
    prevEntry: 'السابق',
    nextEntry: 'التالي',
    onThisPage: 'في هذه الصفحة',
    estimate: 'تقدير',
    notMeasured: 'غير مقيس'
  },
  en: {
    siteName: 'Harat Al Aqur',
    siteQualifier: 'NIZWA',
    tagline: 'The walled quarter at the heart of Nizwa',
    nav: { discover: 'Discover', map: 'Wall map', route: 'The walk', visit: 'Eat & stay', credits: 'The book' },
    toggleLabel: 'العربية',
    toggleTitle: 'View this page in Arabic',
    skipToContent: 'Skip to content',
    readMore: 'Read the entry',
    backToDiscover: 'All entries',
    entriesTitle: 'Discover the quarter',
    entriesLead: "Thirty-one entries on the quarter's mosques, towers, aflaj and houses, carried over from the book itself.",
    mapTitle: 'The wall map',
    routeTitle: 'The walk',
    routeLead: 'Nine stops that follow the ground rather than the book’s order: start at the gate that carries the museum, walk the restored wall, then work inward and finish in the souq.',
    routeOrderNote: 'The order is our suggestion, not a claim about the ground. What each stop says is the book’s own text.',
    routeNoTimes: 'No times, no distances',
    routeNoTimesBody: 'Nobody has measured how long the walk takes or how far it is between stops, so you will find no “about two hours” and no “six minutes” here. The one length the book gives is the wall itself: about two kilometres.',
    routeStop: 'Stop',
    routeGone: 'gone; only its place remains',
    routeStart: 'Starts at',
    routeOnPlan: 'on the plan',
    routeReadEntry: 'Read the entry',
    visitTitle: 'Eat & stay',
    sourceNoteTitle: 'Sources disagree here',
    fromTheBook: 'From the book',
    lastChecked: 'Last checked',
    figuresTitle: 'The quarter in figures',
    photoCredit: "From the book's photographs",
    prevEntry: 'Previous',
    nextEntry: 'Next',
    onThisPage: 'On this page',
    estimate: 'estimate',
    notMeasured: 'not measured'
  }
} as const;

export type UI = (typeof ui)['ar'];
