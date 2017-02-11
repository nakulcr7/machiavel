from models.note import Note


def test_note_class():
    note1 = Note("A", "major")
    note2 = Note("D", "major")
    assert note1.is_mixable(note2) is True

    note1 = Note("A", "major")
    note2 = Note("F", "major")
    assert note1.is_mixable(note2) is False


def main():
    test_note_class()


if __name__ == '__main__':
    main()
