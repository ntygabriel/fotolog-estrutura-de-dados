import json
from photo import Photo
from photo_bst import PhotoBST

class Catalog:
    def __init__(self):
        self._index = PhotoBST()
        self.sec_index = {} 

    def add(self, photo: Photo):
        if photo.id in self.sec_index:
            raise ValueError(f"ID duplicado: {photo.id}")
        self._index.insert(photo)
        self.sec_index[photo.id] = photo

    def remove(self, id: int):
        if id not in self.sec_index:
            raise ValueError(f"Foto com id {id} não existe.")
        p = self.sec_index[id]
        self._index.delete(p)
        del self.sec_index[id]

    def get_by_id(self, id: int):
        if id not in self.sec_index:
            raise ValueError(f"Foto {id} não encontrada no catálogo.")
        return self.sec_index[id]

    def range(self, ts1: int, ts2: int):
        return self._index.range(ts1, ts2)

    def nearest(self, ts: int):
        return self._index.nearest(ts)

    def next_of(self, id: int):
        p = self.get_by_id(id)
        _, node = self._index.search(p)
        if node:
            succ = self._index.successor(node)
            return succ.data() if succ else None
        return None

    def prev_of(self, id: int):
        p = self.get_by_id(id)
        _, node = self._index.search(p)
        if node:
            pred = self._index.predecessor(node)
            return pred.data() if pred else None
        return None

    def remove_range(self, ts1: int, ts2: int):
        fotos_remover = self.range(ts1, ts2)
        for f in fotos_remover:
            self.remove(f.id)

    def tag(self, id: int, t: str):
        p = self.get_by_id(id)
        if t not in p.tags:
            p.tags.append(t)

    def rate(self, id: int, r: int):
        if 0 <= r <= 5:
            self.get_by_id(id).rating = r
        else:
            raise ValueError("Rating deve ser entre 0 e 5.")

    def find_by_tag(self, tag: str):
        return [node.data() for node in self._index.in_order() if tag in node.data().tags]

    def stats(self):
        fotos = [node.data() for node in self._index.in_order()]
        total = len(fotos)
        if total == 0: return None
        
        ratings = [f.rating for f in fotos if f.rating is not None]
        media = sum(ratings) / len(ratings) if ratings else 0

        ratings_sorted = sorted(ratings)
        n = len(ratings_sorted)
        mediana = 0
        if n > 0:
            if n % 2 == 0:
                mediana = (ratings_sorted[n//2 - 1] + ratings_sorted[n//2]) / 2
            else:
                mediana = ratings_sorted[n//2]

        return {
            "total": total,
            "mais_antiga": fotos[0],
            "mais_recente": fotos[-1],
            "rating_medio": media,
            "rating_mediano": mediana
        }

    def save(self, path: str):
        dados = [{
            "id": n.data().id, "ts": n.data().ts, "path": n.data().path, 
            "tags": n.data().tags, "rating": n.data().rating
        } for n in self._index.in_order()]
        
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)

    def load(self, path: str):
        with open(path, 'r', encoding='utf-8') as file:
            dados = json.load(file)
            importados = 0
            for item in dados:
                try:
                    f = Photo(item["id"], item["ts"], item["path"], 
                              item.get("tags", []), item.get("rating", 0))
                    self.add(f)
                    importados += 1
                except Exception:
                    continue 
            return importados