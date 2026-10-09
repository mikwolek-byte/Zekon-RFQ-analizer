import io,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
import openpyxl
import zekon_rfq as app

class EngineTests(unittest.TestCase):
    def test_multilingual(self):
        text='NELSON Kopfbolzen\nÜberhöhung 25 mm / camber / contre-flèche\nGewinde M24 / taraudage\nEntwässerung drainage\nEdelstahl A4\nPRS 550 / HWS\nS460NL / S690QL\nKreuzstützen cruciform columns\nFräsen milling fraisage\nKontaktflächen'
        topics={x.topic for x in app.scan(text,'test')}
        self.assertTrue({'Bolce NELSON','Przeciwstrzałka','Gwinty','Odwodnienie / otwory technologiczne','Stal nierdzewna','Blachownica / profil spawany','Słup krzyżowy','Frezowanie','Powierzchnie kontaktowe / docisk'}.issubset(topics))
    def test_no_default_confirmation(self):
        s=app.Session(evidence=app.scan('☐ EXC3\n☑ EXC2\nWorkshop splices not permitted','test'))
        self.assertTrue(all(e.status=='Do weryfikacji' for e in s.evidence))
        self.assertTrue(any('Formularz' in e.note for e in s.evidence))
        self.assertTrue(all('brak potwierdzonego' in row[1] for row in app.card(s)))
    def test_bom_mm_and_decimal_comma(self):
        rows=[['Profil','Ilość szt','Długość','Jednostka długości','kg/m','Masa kg','Gatunek'],['HEA100',2,'12000','mm','16,7','400,8','S235JR']]
        out=app.parse_bom(rows,'test');self.assertEqual(out[0][8],400.8);self.assertNotIn('rozbieżność',out[0][9])
    def test_bom_missing_unit_and_formula(self):
        rows=[['Profil','Ilość szt','Długość','kg/m'],['HEA100',2,12000,16.7],['HEA100','=1+1',12,16.7]]
        out=app.parse_bom(rows,'test');self.assertEqual(out[0][8],'');self.assertIn('jednostka',out[0][9]);self.assertIn('qty:',out[1][9])
    def test_mass_difference(self):
        rows=[['Profil','Ilość szt','Długość','Jednostka długości','kg/m','Masa kg'],['IPE',2,5,'m',20,300]]
        self.assertIn('rozbieżność',app.parse_bom(rows,'test')[0][9])
    def test_zip_duplicate_and_unsupported(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'batch.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('../a.txt','EXC2\nS355J2');z.writestr('b.txt','EXC2\nS355J2');z.writestr('a.dwg',b'xxx')
            s=app.analyse([p]);self.assertTrue(any(i.status=='Duplikat' for i in s.inventory));self.assertTrue(any(i.status=='Nie przeanalizowano' for i in s.inventory));self.assertFalse((Path(td).parent/'a.txt').exists())
    def test_corrupt_file_does_not_stop_batch(self):
        with tempfile.TemporaryDirectory() as td:
            a=Path(td)/'bad.pdf';a.write_bytes(b'bad');b=Path(td)/'good.txt';b.write_text('EXC2 / NELSON')
            s=app.analyse([a,b]);self.assertEqual(s.inventory[0].status,'Błąd');self.assertTrue(s.evidence)
    def test_export_session_and_injection(self):
        s=app.Session(project='Test',evidence=[app.Evidence(app.AREAS[2],'EXC','EXC2','s. 1','Potwierdzone'),app.Evidence('Materiały','test','=HYPERLINK("x")','source')])
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'r.xlsx';app.export_xlsx(s,p);app.export_html(s,Path(td)/'r.html');app.save_session(s,Path(td)/'s.json')
            restored=app.open_session(Path(td)/'s.json');self.assertEqual(restored.evidence[0].status,'Potwierdzone')
            w=openpyxl.load_workbook(p);self.assertEqual(w['Wszystkie ustalenia']['C3'].data_type,'s');self.assertTrue(w['Wszystkie ustalenia']['C3'].value.startswith("'="));w.close()
            self.assertIn('EXC2',(Path(td)/'r.html').read_text())
    def test_zip_limit(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:z.writestr('test.txt','abc')
        with patch.object(app,'MAX_BATCH',2):
            with self.assertRaises(ValueError):app.checked_zip(b.getvalue())
    def test_empty_bom_and_invalid_qty(self):
        with self.assertRaises(ValueError):app.parse_bom([],'test')
        row=app.parse_bom([['Profil','Ilość szt'],['IPE',2.5]],'test')[0]
        self.assertIn('całkowitą',row[9]);self.assertEqual(row[8],'')

if __name__=='__main__':unittest.main()
