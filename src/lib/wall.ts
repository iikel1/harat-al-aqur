/**
 * The towers and gates of the Al Aqur Wall, as the book names them
 * (content/{ar,en}/sections/08-al-aqur-wall.md).
 *
 * IMPORTANT — nothing here is surveyed. The book names fourteen towers while
 * saying the wall carries "fifteen"; recent official coverage says sixteen after
 * restoration; and Dr Al Salmi's plan, traced into content/data/wall-plan.json,
 * draws seventeen. The sides recorded below are the book's own words, never
 * inferred. Coordinates live in the traced plan, not here.
 */
export type Side =
  | 'north' | 'north-east' | 'east' | 'south-east'
  | 'south' | 'south-west' | 'west' | 'north-west'
  | null;

export type WallFeature = {
  id: string;
  ar: string;
  en: string;
  side: Side;
  /** What the book says about where it sits, verbatim in substance. */
  ar_note?: string;
  en_note?: string;
  /** False where the book records the structure as demolished. */
  standing?: boolean;
};

export const TOWERS: WallFeature[] = [
  {
    id: 'al-mathbaha',
    ar: 'برج المذبحة',
    en: 'Al Mathbaha Tower',
    side: 'north',
    ar_note: 'في الزاوية الشمالية على الجانب الغربي من السور.',
    en_note: 'In the northern corner, on the western side of the wall.'
  },
  {
    id: 'mirza',
    ar: 'برج ميرزة',
    en: 'Mirza Tower',
    side: 'south',
    ar_note: 'على الجانب الجنوبي من مسجد الشجبي، ويسميه بعضهم برج بستان قسام.',
    en_note: 'On the southern side of Al Shajbi Mosque; some call it Bustan Qassam Tower.'
  },
  {
    id: 'balj',
    ar: 'برج بلج',
    en: 'Balj Tower',
    side: 'east',
    ar_note: 'على الجانب الشرقي، إلى الغرب من سوق نزوى.',
    en_note: 'On the eastern side, to the west of Nizwa Souq.'
  },
  {
    id: 'al-aliya',
    ar: 'برج العلياء',
    en: 'Al Aliya Tower',
    side: 'east',
    ar_note: 'يقع أعلى من برج بلج.',
    en_note: 'Situated above Balj Tower.'
  },
  {
    id: 'ghuwair',
    ar: 'برج غوير',
    en: 'Ghuwair Tower',
    side: 'north-east',
    ar_note: 'في السوق أمام بوابة السوق الشرقي المعروف بالصنصرة. وكان السور متصلاً بهذا البرج، لا مستقلاً عنه كما يظهر حديثاً.',
    en_note: 'In the souq, facing the gate of the eastern souq known as Al Sansara. The wall used to be joined to this tower, and not free-standing as it appears today.'
  },
  { id: 'al-souq', ar: 'برج السوق', en: 'Al Souq Tower', side: 'north-east' },
  { id: 'al-qala', ar: 'برج القلعة', en: "Al Qal'a Tower", side: null },
  { id: 'bustan-al-aqur-1', ar: 'برج بستان العقر الأول', en: 'Bustan Al Aqur Tower (first)', side: null },
  { id: 'bustan-al-aqur-2', ar: 'برج بستان العقر الثاني', en: 'Bustan Al Aqur Tower (second)', side: null },
  {
    id: 'al-sabkha',
    ar: 'برج الصبخة',
    en: 'Al Sabkha Tower',
    side: 'east',
    ar_note: 'يقع بجانب صباح الصبخة.',
    en_note: 'Beside Sabah Al Sabkha.'
  },
  { id: 'qatat-al-tawi', ar: 'برج قطعة الطوي', en: "Qat'at Al Tawi Tower", side: null },
  { id: 'harat-al-zama', ar: 'برج حارة الزامة', en: 'Harat Al Zama Tower', side: null },
  { id: 'sikkat-al-qabr', ar: 'برج سكة القبر', en: 'Sikkat Al Qabr Tower', side: null },
  { id: 'kharis-balj', ar: 'برج خريص بلج', en: 'Kharis Balj Tower', side: null }
];

export const GATES: WallFeature[] = [
  {
    id: 'abi-al-muthir',
    ar: 'صباح أبي المؤثر',
    en: "Sabah Abi Al Mu'thir",
    side: 'south',
    ar_note: 'في الجهة الجنوبية. وفوقه اليوم متحف أبي المؤثر.',
    en_note: 'On the southern side. The Abu Al Mu’thir Museum stands above it today.',
    standing: true
  },
  {
    id: 'al-shajbi',
    ar: 'صباح الشجبي',
    en: 'Sabah Al Shajbi',
    side: 'west',
    ar_note: 'في الجهة الغربية.',
    en_note: 'On the western side.',
    standing: true
  },
  {
    id: 'al-souq',
    ar: 'صباح السوق',
    en: 'Sabah Al Souq',
    side: 'north-east',
    ar_note: 'في جهة الشمال الشرقي. هُدم أثناء ترميم القلعة والسوق، ولم يبق منه إلا بعض الصور.',
    en_note: 'To the north-east. Demolished during the restoration works on the fort and the souq; nothing remains of it but some photographs.',
    standing: false
  },
  {
    id: 'al-sabkha',
    ar: 'صباح الصبخة',
    en: 'Sabah Al Sabkha',
    side: 'east',
    ar_note: 'في الجهة الشرقية.',
    en_note: 'On the eastern side.',
    standing: true
  }
];

/**
 * Which mark on the traced plan is which named feature.
 *
 * Only entries the book's own words pin down are listed. Everything else on the
 * plan stays unnamed: the plan draws 17 towers, the book names 14 and gives a
 * position for only 6 of them, so most dots cannot honestly be given a name.
 * `basis` records why each match holds — if you cannot write that sentence, do
 * not add the row.
 */
export type PlanMatch = { plan: string; feature: string; ar: string; en: string };

export const TOWER_MATCHES: PlanMatch[] = [
  {
    plan: 't2',
    feature: 'al-mathbaha',
    ar: 'الكتاب يضعه «في الزاوية الشمالية على الجانب الغربي من السور»، وهو البرج الوحيد في الزاوية الشمالية الغربية من المخطط.',
    en: 'The book puts it “in the northern corner, on the western side of the wall”, and it is the only tower in the plan’s north-west corner.'
  },
  {
    plan: 't14',
    feature: 'al-sabkha',
    ar: 'الكتاب يقول إنه «يقع بجانب صباح الصبخة»، وهذا البرج ملاصق للبوابة الشرقية في المخطط.',
    en: 'The book says it stands “beside Sabah Al Sabkha”, and this tower sits immediately beside the eastern gate on the plan.'
  }
];

export const GATE_MATCHES: PlanMatch[] = [
  {
    plan: 'g1',
    feature: 'al-souq',
    ar: 'البوابة الوحيدة في الشمال، والكتاب يضع صباح السوق «في جهة الشمال الشرقي».',
    en: 'The only gate on the northern side; the book places Sabah Al Souq “to the north-east”.'
  },
  {
    plan: 'g2',
    feature: 'al-shajbi',
    ar: 'البوابة الوحيدة في الغرب، والكتاب يضع صباح الشجبي «في الجهة الغربية».',
    en: 'The only gate on the western side; the book places Sabah Al Shajbi “on the western side”.'
  },
  {
    plan: 'g3',
    feature: 'al-sabkha',
    ar: 'في الجهة الشرقية كما يقول الكتاب، ويؤيده أن البرج الملاصق لها هو برج الصبخة نفسه.',
    en: 'On the eastern side, as the book states, supported by the fact that the tower touching it is Al Sabkha Tower itself.'
  },
  {
    plan: 'g4',
    feature: 'abi-al-muthir',
    ar: 'البوابة الرابعة، وهي أقرب البوابتين الباقيتين إلى الجنوب، والكتاب يضع صباح أبي المؤثر «في الجهة الجنوبية». هذا استنتاج بالاستبعاد لا نصٌّ صريح.',
    en: 'The fourth gate, and the more southerly of the two that remain; the book places Sabah Abi Al Mu’thir “on the southern side”. This one is reached by elimination rather than stated outright.'
  }
];

export const matchForPlan = (planId: string) =>
  [...TOWER_MATCHES, ...GATE_MATCHES].find((m) => m.plan === planId);

export const SIDE_LABELS = {
  ar: {
    north: 'شمالاً', 'north-east': 'شمالاً شرقياً', east: 'شرقاً', 'south-east': 'جنوباً شرقياً',
    south: 'جنوباً', 'south-west': 'جنوباً غربياً', west: 'غرباً', 'north-west': 'شمالاً غربياً'
  },
  en: {
    north: 'north', 'north-east': 'north-east', east: 'east', 'south-east': 'south-east',
    south: 'south', 'south-west': 'south-west', west: 'west', 'north-west': 'north-west'
  }
} as const;
