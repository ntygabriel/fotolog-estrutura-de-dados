import unittest
import random
import os
import json
from io import StringIO
from unittest.mock import patch

from photo import Photo
from catalog import Catalog
import repl

class TestFotologCompleto(unittest.TestCase):

    def setUp(self):
        self.cat = Catalog()
        self.arquivo_teste = "manifest_teste.json"

    def tearDown(self):
        if os.path.exists(self.arquivo_teste):
            os.remove(self.arquivo_teste)

    def test_carga_em_massa_e_ordenacao(self):
        for i in range(1, 1001):
            ts = random.randint(1600000000, 1700000000)
            self.cat.add(Photo(i, ts, f"/foto_{i}.jpg"))
        
        fotos = [n.data() for n in self.cat._index.in_order()]
        self.assertEqual(len(fotos), 1000)
        
        # valida se a lista final ta crescendo direitinho
        is_sorted = all(fotos[i] < fotos[i+1] for i in range(len(fotos)-1))
        self.assertTrue(is_sorted)

    def test_performance_range_vs_varredura_linear(self):
        for i in range(1, 101):
            ts = 1000 + (i * 10)
            self.cat.add(Photo(i, ts, f"/p_{i}.jpg"))
            
        ts_start, ts_end = 1200, 1800
        
        # jeito lento O(N) so pra servir de gabarito
        todas = [n.data() for n in self.cat._index.in_order()]
        baseline = [f for f in todas if ts_start <= f.ts <= ts_end]
        baseline.sort()
        
        resultado = self.cat.range(ts_start, ts_end)
        self.assertEqual(resultado, baseline)

    def test_busca_aproximada_nearest(self):
        self.cat.add(Photo(1, 1000, "/1.jpg"))
        self.cat.add(Photo(2, 2000, "/2.jpg"))
        self.cat.add(Photo(3, 3000, "/3.jpg"))
        
        self.assertEqual(self.cat.nearest(500).id, 1)   
        self.assertEqual(self.cat.nearest(4000).id, 3)  
        self.assertEqual(self.cat.nearest(2000).id, 2)  
        # empate na distancia, tem q puxar pelo menor ID
        self.assertEqual(self.cat.nearest(1500).id, 1)  

    def test_remocao_em_lote_mantem_invariantes(self):
        for i in range(1, 11):
            self.cat.add(Photo(i, i*100, f"/f_{i}.jpg"))
            
        self.cat.remove_range(400, 600)
        
        fotos_arvore = [n.data().id for n in self.cat._index.in_order()]
        fotos_dict = list(self.cat.sec_index.keys())
        
        self.assertEqual(len(fotos_arvore), 7)
        self.assertEqual(len(fotos_dict), 7)
        self.assertNotIn(5, fotos_arvore)
        # garante que a arvore e o dict nao dessincronizaram
        self.assertEqual(sorted(fotos_arvore), sorted(fotos_dict)) 

    def test_sucessor_sem_filho_direito(self):
        # montando na mao pra AVL nao rotacionar
        self.cat.add(Photo(2, 2000, "/2.jpg"))
        self.cat.add(Photo(1, 1000, "/1.jpg"))
        self.cat.add(Photo(3, 3000, "/3.jpg"))
        
        # como o 1000 nao tem filho na direita, tem que subir de volta pro pai
        prox = self.cat.next_of(1)
        self.assertIsNotNone(prox)
        self.assertEqual(prox.id, 2)

    def test_remocao_casos_classicos_bst(self):
        self.cat.add(Photo(20, 2000, "/20.jpg"))
        self.cat.add(Photo(10, 1000, "/10.jpg"))
        self.cat.add(Photo(30, 3000, "/30.jpg"))
        self.cat.add(Photo(5, 500, "/5.jpg"))
        self.cat.add(Photo(25, 2500, "/25.jpg"))
        self.cat.add(Photo(35, 3500, "/35.jpg"))
        self.cat.add(Photo(40, 4000, "/40.jpg")) # gambiarra pro 35 ter 1 filho so
        
        self.cat.remove(5)
        self.assertFalse(self.cat._index.search(Photo(5, 500, ""))[0])
        
        self.cat.remove(35)
        self.assertFalse(self.cat._index.search(Photo(35, 3500, ""))[0])
        
        self.cat.remove(20)
        self.assertFalse(self.cat._index.search(Photo(20, 2000, ""))[0])
        
        self.assertEqual(len(self.cat.sec_index), 4)

    def test_persistencia_save_load(self):
        self.cat.add(Photo(1, 1500, "/teste1.jpg", ["sol"], 5))
        self.cat.save(self.arquivo_teste)
        
        novo_cat = Catalog()
        novo_cat.load(self.arquivo_teste)
        
        f = novo_cat.get_by_id(1)
        self.assertEqual(f.path, "/teste1.jpg")
        self.assertIn("sol", f.tags)
        self.assertEqual(f.rating, 5)

    @patch('builtins.input', side_effect=[':add 99 2000 /repl.jpg 4', ':get 99', ':quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_repl(self, mock_stdout, mock_input):
        repl.main()
        output = mock_stdout.getvalue()
        self.assertIn("Foto 99 adicionada", output)
        self.assertIn("repl.jpg", output)

    def test_atualizacao_de_metadados(self):
        self.cat.add(Photo(1, 1000, "/1.jpg"))
        self.cat.tag(1, "paisagem")
        self.cat.rate(1, 5)
        
        f = self.cat.get_by_id(1)
        self.assertIn("paisagem", f.tags)
        self.assertEqual(f.rating, 5)

    def test_busca_por_tag_retorna_ordenado(self):
        self.cat.add(Photo(3, 3000, "/3.jpg", ["festa"]))
        self.cat.add(Photo(1, 1000, "/1.jpg", ["festa"]))
        self.cat.add(Photo(2, 2000, "/2.jpg", ["trabalho"]))
        
        fotos = self.cat.find_by_tag("festa")
        self.assertEqual(len(fotos), 2)
        # 1000 vem antes do 3000
        self.assertEqual(fotos[0].id, 1)
        self.assertEqual(fotos[1].id, 3)

    def test_chave_composta_timestamp_igual(self):
        self.cat.add(Photo(2, 5000, "/a.jpg"))
        self.cat.add(Photo(1, 5000, "/b.jpg")) 
        
        fotos = [n.data() for n in self.cat._index.in_order()]
        self.assertEqual(fotos[0].id, 1)
        self.assertEqual(fotos[1].id, 2)

    def test_excecoes_de_dominio(self):
        self.cat.add(Photo(1, 1000, "/1.jpg"))
        
        with self.assertRaises(ValueError):
            self.cat.add(Photo(1, 2000, "/dup.jpg"))
            
        with self.assertRaises(ValueError):
            self.cat.remove(99)
            
        with self.assertRaises(ValueError):
            self.cat.rate(1, 10)

    def test_calculo_de_estatisticas(self):
        self.cat.add(Photo(1, 1000, "/1.jpg", rating=2))
        self.cat.add(Photo(2, 2000, "/2.jpg", rating=4))
        self.cat.add(Photo(3, 3000, "/3.jpg", rating=5))
        
        st = self.cat.stats()
        self.assertEqual(st["total"], 3)
        self.assertEqual(st["mais_antiga"].id, 1)
        self.assertEqual(st["mais_recente"].id, 3)
        self.assertAlmostEqual(st["rating_medio"], 3.666, places=2)
        self.assertEqual(st["rating_mediano"], 4.0)

    def test_navegacao_nas_bordas(self):
        self.cat.add(Photo(1, 1000, "/1.jpg"))
        self.cat.add(Photo(2, 2000, "/2.jpg"))
        
        self.assertIsNone(self.cat.prev_of(1))
        self.assertIsNone(self.cat.next_of(2))

    def test_import_via_manifesto_json(self):
        dados = [
            {"id": 10, "ts": 1000, "path": "/10.jpg"},
            {"id": 20, "ts": "2024-05-10", "path": "/20.jpg"}
        ]
        with open(self.arquivo_teste, 'w') as f:
            json.dump(dados, f)
            
        importados = self.cat.load(self.arquivo_teste)
        self.assertEqual(importados, 2)
        self.assertEqual(len(self.cat.sec_index), 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)