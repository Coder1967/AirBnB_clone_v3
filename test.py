from models import storage
from models.state import State

for s in storage.all(State).values():
    print(s.to_dict())
