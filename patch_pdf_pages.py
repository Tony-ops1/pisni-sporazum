from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = """    const documentEl = document.querySelector('.document');
    if(!documentEl) throw new Error('Dokument ni najden.');

    const blob = await window.html2pdf()
      .set({
        margin: 0,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, backgroundColor: '#ffffff', logging: false },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['css', 'legacy'] }
      })
      .from(documentEl)
      .outputPdf('blob');"""

new = """    const pages = Array.from(document.querySelectorAll('.document .page'));
    if(!pages.length) throw new Error('Dokument ni najden.');

    const jsPDF = window.jspdf && window.jspdf.jsPDF;
    if(!jsPDF || !window.html2canvas) throw new Error('PDF knjižnica ni pripravljena.');

    const pdf = new jsPDF({ unit:'mm', format:'a4', orientation:'portrait' });

    for(let i=0; i<pages.length; i++) {
      const canvas = await window.html2canvas(pages[i], {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff',
        logging: false,
        width: pages[i].scrollWidth,
        height: pages[i].scrollHeight,
        windowWidth: pages[i].scrollWidth,
        windowHeight: pages[i].scrollHeight
      });

      const imgData = canvas.toDataURL('image/jpeg', 0.98);
      if(i > 0) pdf.addPage('a4', 'portrait');
      pdf.addImage(imgData, 'JPEG', 0, 0, 210, 297, undefined, 'FAST');
    }

    const blob = pdf.output('blob');"""

if old not in s:
    raise SystemExit('PDF blok ni bil najden; nič ni spremenjeno.')

p.write_text(s.replace(old, new, 1), encoding='utf-8')
