import shlex
from catalog import Catalog
from photo import Photo

def main():
    cat = Catalog()
    print(">>> Fotolog iniciado. Digite os comandos (ou :quit para sair) <<<")

    while True:
        try:
            linha = input("> ").strip()
            if not linha: continue

            partes = shlex.split(linha)
            cmd = partes[0]

            if cmd == ":quit":
                break

            elif cmd == ":import":
                importados = cat.load(partes[1])
                print(f"[OK] {importados} fotos importadas de {partes[1]}")

            elif cmd == ":remove":
                cat.remove(int(partes[1]))
                print("[OK] Foto removida.")

            elif cmd == ":remove-range":
                p1 = Photo(0, partes[1], "")
                p2 = Photo(0, partes[2], "")
                cat.remove_range(p1.ts, p2.ts)
                print("[OK] Fotos no intervalo removidas.")

            elif cmd == ":find-tag":
                fotos = cat.find_by_tag(partes[1])
                if not fotos: print("Nenhuma foto com essa tag.")
                for f in fotos: print(f)

            elif cmd == ":next":
                f = cat.next_of(int(partes[1]))
                if f: print(f"Próxima: {f}")
                else: print("Não há próxima foto.")

            elif cmd == ":prev":
                f = cat.prev_of(int(partes[1]))
                if f: print(f"Anterior: {f}")
                else: print("Não há foto anterior.")

            elif cmd == ":tree":
                cat._index.print_binary_tree()
            
            elif cmd == ":help":
                print("\n--- COMANDOS DISPONÍVEIS ---")
                print(":add <id> <ts> <path> [rating] - Adiciona uma foto manualmente.")
                print(":get <id>                      - Mostra os metadados de uma foto.")
                print(":list                          - Lista todas as fotos em ordem cronológica.")
                print(":range <ts1> <ts2>             - Lista fotos com timestamp no intervalo.")
                print(":nearest <ts>                  - Mostra a foto com timestamp mais próximo.")
                print(":tag <id> <tag>                - Adiciona uma tag a uma foto específica.")
                print(":rate <id> <0..5>              - Atribui uma nota de 0 a 5 para a foto.")
                print(":stats                         - Mostra estatísticas gerais do catálogo.")
                print(":save <arquivo>                - Salva as fotos em um arquivo JSON.")
                print(":load <arquivo>                - Carrega as fotos de um arquivo JSON.")
                print(":quit                          - Encerra o fotolog.")
                print("-------------------------------------------------------------------------------\n")

            elif cmd == ":add":
                id_foto = int(partes[1])
                ts = partes[2] 
                path = partes[3]
                rating = int(partes[4]) if len(partes) > 4 else 0
                cat.add(Photo(id_foto, ts, path, rating=rating))
                print(f"[OK] Foto {id_foto} adicionada.")
                
            elif cmd == ":get":
                f = cat.get_by_id(int(partes[1]))
                print(f"[{f.id}] TS: {f.ts} | Path: {f.path} | Tags: {f.tags} | Rate: {f.rating}")
                
            elif cmd == ":range":
                p1 = Photo(0, partes[1], "")
                p2 = Photo(0, partes[2], "")
                fotos = cat.range(p1.ts, p2.ts)
                for f in fotos: print(f)
                
            elif cmd == ":nearest":
                p_dummy = Photo(0, partes[1], "")
                f = cat.nearest(p_dummy.ts)
                if f: print(f"Mais próxima: {f}")
                else: print("Catálogo vazio.")
                
            elif cmd == ":list":
                fotos = cat._index.in_order()
                if not fotos: print("Catálogo vazio.")
                for f in fotos: print(f.data())
                
            elif cmd == ":tag":
                cat.tag(int(partes[1]), partes[2])
                print("[OK] Tag adicionada.")

            elif cmd == ":rate":
                cat.rate(int(partes[1]), int(partes[2]))
                print(f"[OK] Rating atualizado.")
                
            elif cmd == ":stats":
                s = cat.stats()
                if s: print(s)
                else: print("Sem fotos para calcular estatísticas.")
            
            elif cmd == ":save":
                cat.save(partes[1])
                print(f"[OK] Catálogo salvo com sucesso em {partes[1]}")
                
            elif cmd == ":load":
                importados = cat.load(partes[1])
                print(f"[OK] {importados} fotos carregadas do arquivo {partes[1]}")

            else:
                print("[ERRO] Comando não reconhecido ou parâmetros incorretos.")
                
        except Exception as e:
            print(f"[ERRO DE SINTAXE OU USO] {e}")

if __name__ == "__main__":
    main()