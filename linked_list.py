# ============================================================
#  linked_list.py  –  Singly-linked list for decayed atoms
# ============================================================

class DecayNode:
    """A single node recording which atom decayed and when."""
    __slots__ = ("atom_id", "time_step", "next")

    def __init__(self, atom_id: int, time_step: int) -> None:
        self.atom_id   = atom_id
        self.time_step = time_step
        self.next: "DecayNode | None" = None


class DecayList:
    """Append-only singly-linked list of DecayNode objects."""

    def __init__(self) -> None:
        self.head: DecayNode | None = None
        self.tail: DecayNode | None = None
        self.size: int = 0

    def append(self, atom_id: int, time_step: int) -> None:
        node = DecayNode(atom_id, time_step)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def clear(self) -> None:
        self.head = self.tail = None
        self.size = 0

    def __len__(self) -> int:
        return self.size
