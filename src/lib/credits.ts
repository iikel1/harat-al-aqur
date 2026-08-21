/**
 * Who made the book this site is built from.
 *
 * The roles below are the ones the author names himself, in the acknowledgements
 * on the book's closing pages (now content/ar/back-matter/acknowledgements.md).
 * Nobody has been added, and nobody has been left out. The English is a
 * translation of the author's Arabic, written for this site — the printed book
 * has no English edition.
 */
export type Credit = {
  ar: string;
  en: string;
  /** What they did, in the author's own framing. */
  role_ar: string;
  role_en: string;
  /** Extra detail where a source records it. */
  note_ar?: string;
  note_en?: string;
};

export const AUTHOR: Credit = {
  ar: 'سليمان بن محمد السليماني',
  en: 'Suleiman bin Muhammad Al Sulaimani',
  role_ar: 'تأليف',
  role_en: 'Author',
  note_ar: 'من قرية العقر، ويتولى اليوم إدارة أوقاف الحارة.',
  note_en: 'Of the village of Al Aqur; he runs the quarter’s endowment today.'
};

export const CONTRIBUTORS: Credit[] = [
  {
    ar: 'محمد بن عبد الله السيفي',
    en: 'Muhammad bin Abdullah Al Saifi',
    role_ar: 'مراجعة المادة وتصحيحها',
    role_en: 'Review and correction',
    note_ar: 'مؤلف «الحلل السندسية في الكتابات المسجدية».',
    note_en: 'Author of Al-Hulal al-Sundusiyya fi al-Kitabat al-Masjidiyya.'
  },
  {
    ar: 'سامي بن سالم الهنائي',
    en: "Sami bin Salim Al Hina'i",
    role_ar: 'التصوير',
    role_en: 'Photography',
    note_ar: 'تكلّف عناء التصوير عدة أيام. أغلب صور هذا الموقع من عدسته.',
    note_en: 'He took on the labour of photographing over several days. Most of the photographs on this site are his.'
  },
  {
    ar: 'علي بن أحمد القسيمي',
    en: 'Ali bin Ahmed Al Qusaimi',
    role_ar: 'الصور القديمة',
    role_en: 'Archive photographs'
  },
  {
    ar: 'ناصر بن محمد الفرقاني',
    en: 'Nasser bin Muhammad Al Farqani',
    role_ar: 'الصور القديمة',
    role_en: 'Archive photographs'
  },
  {
    ar: 'د. الوليد بن زاهر السالمي',
    en: 'Dr Al Walid bin Zahir Al Salmi',
    role_ar: 'مخطط سور العقر',
    role_en: 'The plan of the Al Aqur Wall',
    note_ar: 'مخططه هو الأساس الذي ستُبنى عليه خريطة السور في هذا الموقع.',
    note_en: 'His plan is what the wall map on this site will be built from.'
  },
  {
    ar: 'راشد بن عبد الله الفارسي',
    en: 'Rashid bin Abdullah Al Farsi',
    role_ar: 'مدير نزل نزوى التراثية',
    role_en: 'Director of the Nizwa Heritage Inn'
  },
  {
    ar: 'خالد بن عيسى السليماني',
    en: 'Khalid bin Issa Al Sulaimani',
    role_ar: 'المراجعة النهائية للكتاب',
    role_en: 'Final review of the book'
  }
];

export const BOOK = {
  ar: {
    title: 'حارة العقر',
    publisher: 'مكتبة خزائن الآثار، بركاء، عُمان',
    year: '١٤٤٢هـ / ٢٠٢١م',
    isbn: '978-9933-29-448-9',
    pages: '٦٥ صفحة، مصوّرة'
  },
  en: {
    title: 'Harat Al Aqur',
    publisher: 'Maktabat Khaza’in al-Athar, Barka, Oman',
    year: '1442 AH / 2021 CE',
    isbn: '978-9933-29-448-9',
    pages: '65 pages, illustrated'
  }
} as const;

/**
 * The author's acknowledgements and afterword, translated. The Arabic is not
 * repeated here — it is read from content/ar/back-matter/, which the extraction
 * pipeline writes, so the book's own words have exactly one source of truth.
 */
export const BACK_MATTER_EN = {
  acknowledgements: {
    title: 'Thanks and appreciation',
    body: 'Heartfelt thanks to the esteemed Muhammad bin Abdullah Al Saifi for reviewing this material and correcting it; to the gifted photographer Sami bin Salim Al Hina’i, who took on the labour of photographing over several days; to the brothers Ali bin Ahmed Al Qusaimi and Nasser bin Muhammad Al Farqani for providing me with the rare old photographs; to Dr Al Walid bin Zahir Al Salmi, who prepared the plan of the Al Aqur Wall for me; to Rashid bin Abdullah Al Farsi, director of the Nizwa Heritage Inn; and to my uncle Khalid bin Issa Al Sulaimani for the final review of the book; and to everyone who helped this work succeed, with a word or with a piece of advice.'
  },
  afterword: {
    title: 'Afterword',
    body: 'By the grace of God and His help, this modest work is complete. What I intended by it is to acquaint the visitor with the history and the remains of Harat Al Aqur, in Nizwa, the city of learning and of scholars, the heartland of Islam, so that it may serve as a guide as they walk through it. Care was taken to keep the material easy, clear and brief, so that it would be simple for anyone to read, and engaging, so that the reader does not tire of it; for to set out the history of this quarter in full would take many volumes. This book is to be translated into several world languages, with some changes and additions in each printing to suit the language and the culture of that country, so that its introduction may carry the most notable historical ties between the two countries. Its first printing, God willing, will be in nine different languages.'
  }
} as const;

export type BackMatterKey = keyof typeof BACK_MATTER_EN;
