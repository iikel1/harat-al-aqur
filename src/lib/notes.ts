import type { Lang } from './i18n';

// Where the sources disagree, the page says so out loud instead of picking a
// winner. Drawn from docs/AL-AQR.md section 5. `kind: 'dispute'` = two or more
// sources give different figures; `kind: 'unverified'` = the book is the only
// voice and nothing independent was found.
export type SourceNote = {
  slug: string;
  kind: 'dispute' | 'unverified';
  ar: { heading: string; body: string };
  en: { heading: string; body: string };
};

export const SOURCE_NOTES: SourceNote[] = [
  {
    slug: 'shawadhna-mosque',
    kind: 'dispute',
    ar: {
      heading: 'سنة التأسيس',
      body: 'يذكر الكتاب أن المسجد بُني سنة ٩ﻫ. وتذكر ويكيبيديا العربية وجريدة عُمان سنة ٧ﻫ، بينما تذكر الوطن سنة ٨ﻫ. وتتفق المصادر كلها على محراب سنة ٩٣٦ﻫ / ١٥٢٩م وعلى ترميم ٢٠٠٣م. أما وصفه بأنه ثاني مسجد بُني في عُمان فلم نجد له مصدراً خارج الكتاب.'
    },
    en: {
      heading: 'The founding date',
      body: 'The book gives 9 AH. Arabic Wikipedia and Oman Daily give 7 AH; Al-Watan gives 8 AH. All the sources agree on the 936 AH / 1529 CE mihrab and on the 2003 restoration. The claim that it is the second mosque built in Oman has no source outside the book.'
    }
  },
  {
    slug: 'harat-al-aqur',
    kind: 'dispute',
    ar: {
      heading: 'عمر الحارة',
      body: 'يفهم من الكتاب أن الموضع كان مسكوناً قبل الإسلام. وتتفاوت الأرقام في الصحافة تفاوتاً كبيراً: ١٢٠٠ سنة، و١٥٠٠ سنة، و٤٠٠٠ سنة. لا يتفق رقمان منها، ولم نجد دراسة أثرية منشورة تحسم المسألة.'
    },
    en: {
      heading: 'The age of the quarter',
      body: 'The book implies the site was settled before Islam. Press figures vary widely: 1,200 years, 1,500 years and 4,000 years. No two agree, and we found no published archaeological study that settles it.'
    }
  },
  {
    slug: 'al-aqur-wall',
    kind: 'dispute',
    ar: {
      heading: 'طول السور وعدد الأبراج والبوابات',
      body: 'يقول الكتاب: السور نحو كيلومترين، وعليه خمسة عشر برجاً وأربع بوابات. وتذكر التغطية الرسمية الحديثة ١٩٥٠ م أو ٢٠٠٠ م للطول، و١٦ برجاً وثلاث بوابات، وهو ما يتسق مع إشارة الكتاب نفسه إلى هدم صباح السوق، غير أن عدد الأبراج يبقى مختلفاً. وذكر تقرير لجريدة عُمان سنة ٢٠٢١م سبعة عشر برجاً.'
    },
    en: {
      heading: 'The length of the wall, and the count of towers and gates',
      body: 'The book says the wall runs to about two kilometres and carries fifteen towers and four gates. Recent official coverage gives 1,950 m or 2,000 m for the length, and 16 towers with 3 gates, consistent with the book’s own note that Sabah Al Souq was demolished, though the tower count still differs. A 2021 Oman Daily piece says seventeen.'
    }
  },
  {
    slug: 'nizwa-castle',
    kind: 'dispute',
    ar: {
      heading: 'من بدأ بناء الحصن',
      body: 'ينسب الكتاب بداية الحصن إلى الإمام محمد بن عبدالله بن أبي عفان في القرن الثاني الهجري. وتنسبها أغلب المراجع إلى الإمام الصلت بن مالك الخروصي في القرن الثالث الهجري / التاسع الميلادي، ولا ترى في الأول إلا موسِّعاً. وفي شأن السور تؤرخ السحوة بناء الصلت الأول بسنة ٢٣٧ﻫ وإعادة البناء اليعربية بسنة ١٠٥٠ﻫ، وهو ما لا يعارض رواية الكتاب.'
    },
    en: {
      heading: 'Who began the castle',
      body: 'The book attributes the start of the castle to Imam Muhammad bin Abdullah bin Abi Affan in the 2nd century AH. Most reference works attribute it to Imam Al Salt bin Malik Al Kharusi in the 3rd century AH / 9th CE, casting the former only as an extender. For the wall, Al-Sahwa dates Al Salt’s original to 237 AH and the Ya’rubi rebuild to 1050 AH, which is compatible with the book.'
    }
  },
  {
    slug: 'nizwa-fort',
    kind: 'dispute',
    ar: {
      heading: 'تاريخ بناء القلعة',
      body: 'يقول الكتاب إن بناءها استغرق اثنتي عشرة سنة بعد جلاء البرتغاليين سنة ١٦٥٠م. وتذكر ويكيبيديا العربية وغيرها أن البناء بدأ سنة ١٦٥٦م وانتهى سنة ١٦٦٨م.'
    },
    en: {
      heading: 'When the fort was built',
      body: 'The book says construction took twelve years following the expulsion of the Portuguese in 1650. Arabic Wikipedia and others give a start of 1656 and a completion of 1668.'
    }
  },
  {
    slug: 'persians-graveyard',
    kind: 'unverified',
    ar: { heading: 'لم نجد مصدراً مستقلاً', body: 'رواية مقبرة الفرس ومذبحة سنة ١١٥٠ﻫ لم نجد لها مصدراً خارج الكتاب.' },
    en: { heading: 'No independent source found', body: 'The account of the Persians’ graveyard and the massacre of 1150 AH appears in the book and nowhere else we could find.' }
  },
  {
    slug: 'sheikh-al-asamm',
    kind: 'unverified',
    ar: { heading: 'لم نجد مصدراً مستقلاً', body: 'خبر قبر الشيخ الأصم وحكاية «الشيخ الأصم» مرويّان في الكتاب وحده.' },
    en: { heading: 'No independent source found', body: 'The grave of Sheikh Al Asamm and the anecdote of the deaf sheikh rest on the book alone.' }
  },
  {
    slug: 'thoms-hospital',
    kind: 'unverified',
    ar: { heading: 'اسم الطبيب يحتاج تثبيتاً', body: 'الطبيب المذكور هو على الأرجح الدكتور ولز تومس من الإرسالية العربية الأمريكية، غير أن ذلك يحتاج إلى تأكيد، ورسم الاسم يحتاج إلى تصحيح.' },
    en: { heading: 'The doctor’s name needs confirming', body: 'The American mission doctor is almost certainly Dr Wells Thoms of the Arabian Mission, but this needs confirming and the spelling fixing.' }
  },
  {
    slug: 'nizwa-souq',
    kind: 'unverified',
    ar: { heading: 'جائزة ١٩٩٢م', body: 'لم نجد إشارة إلى الجهة المانحة لجائزة العمارة المذكورة سنة ١٩٩٢م ولا مصدراً يوثّقها.' },
    en: { heading: 'The 1992 award', body: 'We found no citation for the architecture award said to date from 1992, and the awarding body is unnamed.' }
  },
  {
    slug: 'saat-al-mudda',
    kind: 'unverified',
    ar: { heading: 'لا توجد صورة معروفة', body: 'يذكر الكتاب أنه لا توجد صورة لساعة المدة. ويذكر أن أمثلة منها باقية في ولايات أخرى، فيحسن التحقق مما إذا كانت صورة قد ظهرت منذ صدور الكتاب.' },
    en: { heading: 'No known photograph', body: 'The book says no photograph of the sundial exists. It also says examples survive in other wilayats, so it is worth checking whether one has surfaced since the book was published.' }
  }
];

export const notesFor = (slug: string) => SOURCE_NOTES.filter((n) => n.slug === slug);
export const noteText = (n: SourceNote, lang: Lang) => n[lang];
