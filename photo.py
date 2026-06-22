from datetime import datetime

class Photo:
    def __init__(self, id: int, ts, path: str, tags: list = None, rating: int = 0):
        self.id = id
        
        if isinstance(ts, int):
            self.ts = ts
        elif isinstance(ts, str):
            if ts.isdigit(): 
                self.ts = int(ts)
            else:
                try:
                    if len(ts) == 10:
                        dt = datetime.strptime(ts, "%Y-%m-%d")
                    elif len(ts) == 16:
                        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
                    else:
                        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                    self.ts = int(dt.timestamp())
                except ValueError:
                    self.ts = 0 
                    
            self.ts = int(ts)

        self.path = path
        self.tags = tags if tags is not None else []
        self.rating = rating

    def __lt__(self, other):
        if not isinstance(other, Photo): return False
        return (self.ts, self.id) < (other.ts, other.id)

    def __le__(self, other):
        if not isinstance(other, Photo): return False
        return (self.ts, self.id) <= (other.ts, other.id)

    def __gt__(self, other):
        if not isinstance(other, Photo): return False
        return (self.ts, self.id) > (other.ts, other.id)

    def __ge__(self, other):
        if not isinstance(other, Photo): return False
        return (self.ts, self.id) >= (other.ts, other.id)

    def __eq__(self, other):
        if not isinstance(other, Photo): return False
        return (self.ts, self.id) == (other.ts, other.id)

    def __repr__(self):
        return f"Photo(id={self.id}, ts={self.ts}, path='{self.path}')"

    def __str__(self):
        return f"{self.ts} {self.path}"