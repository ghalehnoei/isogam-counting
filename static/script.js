const tr = {
  fa: {
    pageTitle: 'شمارشگر هوشمند ایزوگام',
    'nav.brand': 'شمارشگر هوشمند ایزوگام',
    'nav.features': 'امکانات',
    'nav.demo': 'نمایش زنده',
    'nav.cta': 'شروع کنید',
    'hero.badge': 'قدرت‌گرفته از YOLO',
    'hero.title1': 'شمارش اشیا با',
    'hero.title2': 'دقت هوش مصنوعی',
    'hero.subtitle': 'تصویر خود را آپلود کنید و تعداد دقیق اشیا را با استفاده از جدیدترین مدل‌های تشخیص YOLO و حذف هوشمند اشیای تکراری دریافت کنید.',
    'hero.cta1': 'امتحان کنید',
    'hero.cta2': 'مشاهده امکانات',
    'hero.placeholder': 'تصویر خود را بارگذاری کنید تا نتیجه را ببینید',
    'features.label': 'امکانات',
    'features.title': 'همه‌چیز برای شمارش دقیق',
    'feat1.title': 'قدرت YOLO',
    'feat1.desc': 'استفاده از جدیدترین مدل‌های تشخیص YOLO برای شناسایی دقیق و بلادرنگ اشیا.',
    'feat2.title': 'حذف موارد تکراری',
    'feat2.desc': 'تشخیص هوشمند اشیای هم‌پوشان با استفاده از آستانه IoU برای شمارش دقیق‌تر.',
    'feat3.title': 'تشخیص نقاط کلیدی',
    'feat3.desc': 'پشتیبانی از مدل‌های تشخیص حالت (Pose) با نمایش نقاط کلیدی روی تصویر.',
    'feat4.title': 'مقایسه تصویری',
    'feat4.desc': 'مقایسه تصویر اصلی و تصویر تحلیل‌شده با یک اسلایدر کشویی.',
    'feat5.title': 'تنظیم آستانه‌ها',
    'feat5.desc': 'تنظیم دقیق آستانه اطمینان و IoU با اسلایدرهای زنده.',
    'feat6.title': 'خروجی و دانلود',
    'feat6.desc': 'دانلود تصاویر تحلیل‌شده و کپی داده‌های ساختاریافته برای استفاده در pipeline هوش مصنوعی.',
    'demo.label': 'نمایش زنده',
    'demo.title': 'خودتان امتحان کنید',
    'demo.subtitle': 'یک تصویر بارگذاری کنید، تنظیمات را تغییر دهید و دکمه تشخیص را بزنید.',
    'demo.model': 'مدل',
    'demo.imgSize': 'سایز تصویر',
    'demo.confidence': 'اطمینان',
    'demo.iou': 'آستانه IoU',
    'demo.drop': 'تصویر را اینجا رها کنید یا کلیک کنید',
    'demo.dropHint': 'JPG, PNG, WebP و سایر فرمت‌ها',
    'demo.enterHint': 'برای تشخیص دکمه Enter را بزنید',
    'demo.detect': 'تشخیص',
    'demo.again': 'تشخیص مجدد؟',
    'demo.finalCount': 'تعداد نهایی',
    'demo.rawDetections': 'تشخیص اولیه',
    'demo.sliderLeft': 'تشخیص',
    'demo.sliderRight': 'اصلی',
    'demo.llmTitle': 'داده‌های تشخیص',
    'demo.copy': 'کپی',
    'demo.copied': 'کپی شد',
    'demo.dlBbox': 'دانلود با کادر',
    'demo.dlCircle': 'دانلود با دایره',
    error: 'خطا',
    serverError: 'خطا در سرور',
    'footer.text': 'ساخته‌شده با',
  },
  en: {
    pageTitle: 'Isogam Smart Counter',
    'nav.brand': 'Isogam Smart Counter',
    'nav.features': 'Features',
    'nav.demo': 'Demo',
    'nav.cta': 'Try Demo',
    'hero.badge': 'Powered by YOLO',
    'hero.title1': 'Count Objects with',
    'hero.title2': 'AI Precision',
    'hero.subtitle': 'Upload your image and get precise object counts using the latest YOLO detection models with intelligent duplicate removal.',
    'hero.cta1': 'Try It Now',
    'hero.cta2': 'See Features',
    'hero.placeholder': 'Drop your image to see the result',
    'features.label': 'Features',
    'features.title': 'Everything you need for precise counting',
    'feat1.title': 'YOLO Power',
    'feat1.desc': 'Leverages cutting-edge YOLO detection models for accurate, real-time object identification.',
    'feat2.title': 'Duplicate Removal',
    'feat2.desc': 'Intelligent overlap detection using IoU threshold for more accurate counting.',
    'feat3.title': 'Keypoint Detection',
    'feat3.desc': 'Supports Pose estimation models with keypoint visualization on the image.',
    'feat4.title': 'Visual Comparison',
    'feat4.desc': 'Compare original and analyzed images side-by-side with a draggable slider.',
    'feat5.title': 'Adjustable Thresholds',
    'feat5.desc': 'Fine-tune confidence and IoU thresholds with live sliders.',
    'feat6.title': 'Export & Download',
    'feat6.desc': 'Download annotated images and copy structured data for your AI pipeline.',
    'demo.label': 'Live Demo',
    'demo.title': 'Try it yourself',
    'demo.subtitle': 'Upload an image, tweak the settings, and hit detect.',
    'demo.model': 'Model',
    'demo.imgSize': 'Image Size',
    'demo.confidence': 'Confidence',
    'demo.iou': 'IoU Threshold',
    'demo.drop': 'Drop image here or tap to upload',
    'demo.dropHint': 'JPG, PNG, WebP & more',
    'demo.enterHint': 'Press Enter to detect',
    'demo.detect': 'Detect',
    'demo.again': 'Another detection?',
    'demo.finalCount': 'Final Count',
    'demo.rawDetections': 'Raw Detections',
    'demo.sliderLeft': 'Detected',
    'demo.sliderRight': 'Original',
    'demo.llmTitle': 'Detection Data',
    'demo.copy': 'Copy',
    'demo.copied': 'Copied',
    'demo.dlBbox': 'Download Bounding Box',
    'demo.dlCircle': 'Download Center Circle',
    error: 'Error',
    serverError: 'Server error',
    'footer.text': 'Built with',
  },
};

let currentLang = 'fa';
const langToggle = document.getElementById('langToggle');
const appBody = document.getElementById('appBody');
const htmlEl = document.documentElement;

function t(key) {
  return tr[currentLang][key] || key;
}

function applyLang(lang) {
  currentLang = lang;
  localStorage.setItem('isogam_lang', lang);
  langToggle.textContent = lang === 'fa' ? 'EN' : 'FA';
  htmlEl.lang = lang;
  htmlEl.dir = lang === 'fa' ? 'rtl' : 'ltr';
  appBody.style.fontFamily = lang === 'fa' ? "'Vazirmatn', sans-serif" : "'Inter', sans-serif";
  document.querySelectorAll('h1,h2,h3').forEach(el => {
    el.style.fontFamily = lang === 'en' ? "'Outfit', sans-serif" : '';
  });

  const sliderLabels = document.getElementById('sliderLabels');
  if (sliderLabels) {
    sliderLabels.style.flexDirection = lang === 'fa' ? 'row-reverse' : 'row';
  }

  const sel = document.getElementById('modelSelect');
  if (sel) {
    sel.style.backgroundPosition = lang === 'fa' ? 'right 8px center' : 'left 8px center';
  }

  const side = lang === 'en' ? 'left' : 'right';
  let ds = document.getElementById('i18n-style');
  if (!ds) { ds = document.createElement('style'); ds.id = 'i18n-style'; document.head.appendChild(ds); }
  ds.textContent = `#statsDivider::before{content:"";position:absolute;${side}:0;top:20%;height:60%;width:1px;background:var(--divider)}@media(max-width:639px){#statsDivider::before{display:none}}`;

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (tr[lang][key]) el.textContent = tr[lang][key];
  });

  document.title = t('pageTitle');

  const abt = document.getElementById('actionBarText');
  if (abt && !abt.hasAttribute('data-i18n-alt-switched')) {
    abt.textContent = t('demo.enterHint');
  }
}

langToggle.addEventListener('click', () => {
  applyLang(currentLang === 'fa' ? 'en' : 'fa');
});

const savedLang = localStorage.getItem('isogam_lang');
if (savedLang && (savedLang === 'fa' || savedLang === 'en')) {
  applyLang(savedLang);
}

const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
let darkMode = localStorage.getItem('isogam_theme') === 'dark';
if (darkMode === undefined || darkMode === null) {
  darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
}
function applyTheme(dark) {
  darkMode = dark;
  htmlEl.classList.toggle('dark', dark);
  localStorage.setItem('isogam_theme', dark ? 'dark' : 'light');
  const sun = themeIcon.querySelector('.sun');
  const moon = themeIcon.querySelector('.moon');
  if (dark) {
    sun.classList.add('hidden');
    moon.classList.remove('hidden');
  } else {
    sun.classList.remove('hidden');
    moon.classList.add('hidden');
  }
}
applyTheme(darkMode);
themeToggle.addEventListener('click', () => applyTheme(!darkMode));

const modelSelect = document.getElementById('modelSelect');
const confSlider = document.getElementById('confSlider');
const confVal = document.getElementById('confVal');
const iouSlider = document.getElementById('iouSlider');
const iouVal = document.getElementById('iouVal');
const imgszSlider = document.getElementById('imgszSlider');
const imgszVal = document.getElementById('imgszVal');
const dropZone = document.getElementById('dropZone');
const actionBar = document.getElementById('actionBar');
const detectBtn = document.getElementById('detectBtn');

let lastFile = null;
let busy = false;
let lastBboxB64 = '';
let lastCircleB64 = '';

fetch('/models/').then(r => r.json()).then(data => {
  data.models.forEach(name => {
    const opt = document.createElement('option');
    opt.value = name;
    opt.textContent = name;
    modelSelect.appendChild(opt);
  });
});

const fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.accept = 'image/*';

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('!border-[#F97316]', '!bg-[#F97316]/[0.03]'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('!border-[#F97316]', '!bg-[#F97316]/[0.03]'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('!border-[#F97316]', '!bg-[#F97316]/[0.03]');
  if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => {
  if (fileInput.files.length) handleFile(fileInput.files[0]);
});

confSlider.addEventListener('input', () => { confVal.textContent = (confSlider.value / 100).toFixed(2); });
iouSlider.addEventListener('input', () => { iouVal.textContent = (iouSlider.value / 100).toFixed(2); });
imgszSlider.addEventListener('input', () => { imgszVal.textContent = imgszSlider.value === '0' ? 'auto' : imgszSlider.value; });

function show(el) { el.classList.remove('hidden'); }
function hide(el) { el.classList.add('hidden'); }

function handleFile(file) {
  lastFile = file;
  show(actionBar);
  hide(document.getElementById('stats'));
  hide(document.getElementById('sliderWrap'));
  hide(document.getElementById('llmOutput'));
  hide(document.getElementById('error'));
  hide(document.getElementById('dlRow'));
  detectBtn.textContent = t('demo.detect');
  document.getElementById('actionBarText').textContent = t('demo.enterHint');
  document.getElementById('actionBarText').removeAttribute('data-i18n-alt-switched');
}

function popNum(el) {
  el.style.animation = 'none';
  void el.offsetWidth;
  el.style.animation = 'count-pop 0.35s ease';
}

async function predict() {
  if (!lastFile || busy) return;
  busy = true;

  show(document.getElementById('spinnerWrap'));
  hide(actionBar);

  const formData = new FormData();
  formData.append('file', lastFile);
  formData.append('conf', confSlider.value / 100);
  formData.append('iou', iouSlider.value / 100);
  formData.append('imgsz', imgszSlider.value);
  formData.append('model_name', modelSelect.value);

  try {
    const res = await fetch('/predict/', { method: 'POST', body: formData });
    if (!res.ok) throw new Error(t('serverError'));
    const data = await res.json();

    const dedupEl = document.getElementById('dedupText');
    const countEl = document.getElementById('countText');
    dedupEl.textContent = data.dedup_count;
    countEl.textContent = data.count;
    popNum(dedupEl);

    lastBboxB64 = data.bbox_b64;
    lastCircleB64 = data.circle_b64;
    document.getElementById('sliderBaseImg').src = 'data:image/jpeg;base64,' + data.original_b64;
    document.getElementById('annotatedImg').src = 'data:image/jpeg;base64,' + data.circle_b64;

    const statsEl = document.getElementById('stats');
    show(statsEl);
    statsEl.style.animation = 'none';
    void statsEl.offsetWidth;
    statsEl.style.animation = 'success-pulse 0.8s ease-out';
    show(document.getElementById('sliderWrap'));
    initSlider();
    show(actionBar);
    document.getElementById('actionBarText').textContent = t('demo.again');
    document.getElementById('actionBarText').setAttribute('data-i18n-alt-switched', '1');
    detectBtn.textContent = t('demo.detect');

    const lines = data.detections.map((d, i) => {
      const b = d.bbox.map(v => Math.round(v));
      return `#${i + 1}: bbox [${b[0]}, ${b[1]}, ${b[2]}, ${b[3]}]  conf ${d.confidence}${d.keypoints.length ? `  keypoints: ${JSON.stringify(d.keypoints)}` : ''}`;
    });
    const total = data.dedup_count;
    const raw = data.count;
    document.getElementById('llmText').value =
      `${t('demo.finalCount')}: ${total}\n${t('demo.rawDetections')}: ${raw}\n\n${t('demo.llmTitle')}:\n${lines.join('\n')}`;
    show(document.getElementById('llmOutput'));
    show(document.getElementById('dlRow'));
  } catch (err) {
    document.getElementById('error').textContent = t('error') + ': ' + err.message;
    show(document.getElementById('error'));
    show(actionBar);
  } finally {
    hide(document.getElementById('spinnerWrap'));
    busy = false;
  }
}

document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !busy && lastFile) { e.preventDefault(); predict(); }
});

detectBtn.addEventListener('click', () => { if (!busy && lastFile) predict(); });

let dragActive = false;

function initSlider() {
  const comp = document.getElementById('imgComp');
  const annotated = document.getElementById('annotatedImg');
  const slider = document.getElementById('slider');

  function setPos(x) {
    const rect = comp.getBoundingClientRect();
    let pct = ((x - rect.left) / rect.width) * 100;
    pct = Math.max(0, Math.min(100, pct));
    annotated.style.clipPath = `inset(0 ${100 - pct}% 0 0)`;
    slider.style.left = pct + '%';
  }

  setPos(comp.getBoundingClientRect().width / 2 + comp.getBoundingClientRect().left);

  comp.addEventListener('mousedown', e => { dragActive = true; setPos(e.clientX); });
  document.addEventListener('mousemove', e => { if (dragActive) setPos(e.clientX); });
  document.addEventListener('mouseup', () => { dragActive = false; });

  comp.addEventListener('touchstart', e => { dragActive = true; setPos(e.touches[0].clientX); });
  document.addEventListener('touchmove', e => { if (dragActive) setPos(e.touches[0].clientX); });
  document.addEventListener('touchend', () => { dragActive = false; });

  comp.addEventListener('click', () => {
    const modal = document.getElementById('zoomModal');
    document.getElementById('zoomImg').src = document.getElementById('annotatedImg').src;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    modal.onclick = () => { modal.classList.add('hidden'); modal.classList.remove('flex'); };
  });
}

document.getElementById('llmToggle').addEventListener('click', () => {
  document.getElementById('llmBody').classList.toggle('hidden');
  document.getElementById('llmArrow').classList.toggle('rotate-180');
});

document.getElementById('copyBtn').addEventListener('click', () => {
  const ta = document.getElementById('llmText');
  ta.select();
  navigator.clipboard.writeText(ta.value).then(() => {
    const btn = document.getElementById('copyBtn');
    btn.textContent = t('demo.copied');
    btn.classList.add('!text-[#22D3EE]', '!border-[#22D3EE]');
    setTimeout(() => {
      btn.textContent = t('demo.copy');
      btn.classList.remove('!text-[#22D3EE]', '!border-[#22D3EE]');
    }, 1500);
  });
});

function downloadB64(b64, name) {
  const a = document.createElement('a');
  a.href = 'data:image/jpeg;base64,' + b64;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

document.getElementById('downloadBboxBtn').addEventListener('click', () => downloadB64(lastBboxB64, 'bbox-annotated.jpg'));
document.getElementById('downloadCircleBtn').addEventListener('click', () => downloadB64(lastCircleB64, 'circle-annotated.jpg'));