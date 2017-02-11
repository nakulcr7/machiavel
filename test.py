from models.key import Key


def test_note_class():
    note1 = Key("A", "major")
    note2 = Key("D", "major")
    assert note1.is_mixable(note2) is True

    note1 = Key("A", "major")
    note2 = Key("F", "major")
    assert note1.is_mixable(note2) is False


def main():
    test_note_class()


if __name__ == '__main__':
    main()
