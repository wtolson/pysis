# -*- coding: utf-8 -*-
import os
import pytest
from pysis import labels


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data/')


def test_assignment():
    label = labels.parse_label('foo=bar')
    assert isinstance(label, dict)
    assert label['foo'] == 'bar'


def test_spaceing():
    label = labels.parse_label("""
        foo = bar
        nospace=good
          lots_of_spaceing    =    also good
        End
    """)

    assert isinstance(label, dict)
    assert label['foo'] == 'bar'
    assert label['nospace'] == 'good'
    assert label['lots_of_spaceing'] == 'also good'


def test_integers():
    label = labels.parse_label("""
        integer = 42
        positive_integer = +123
        negitive_integer = -1
        invalid_integer = 1a2
        End
    """)

    assert isinstance(label['integer'], int)
    assert label['integer'] == 42

    assert isinstance(label['integer'], int)
    assert label['positive_integer'] == 123

    assert isinstance(label['negitive_integer'], int)
    assert label['negitive_integer'] == -1

    assert isinstance(label['invalid_integer'], str)
    assert label['invalid_integer'] == '1a2'


def test_floats():
    label = labels.parse_label("""
        float = 1.0
        float_no_whole = .3
        float_leading_zero = 0.5
        positive_float = +2.0
        negative_float = -1.0
        invalid_float = 1.2.3
        End
    """)
    assert isinstance(label['float'], float)
    assert label['float'] == 1.0

    assert isinstance(label['float_no_whole'], float)
    assert label['float_no_whole'] == 0.3

    assert isinstance(label['float_leading_zero'], float)
    assert label['float_leading_zero'] == 0.5

    assert isinstance(label['positive_float'], float)
    assert label['positive_float'] == 2.0

    assert isinstance(label['negative_float'], float)
    assert label['negative_float'] == -1.0

    assert isinstance(label['invalid_float'], str)
    assert label['invalid_float'] == '1.2.3'


def test_objects():
    label = labels.parse_label("""
        Object = test_object
          foo = bar

          Object = embedded_object
            foo = bar
          End_Object

          Group = embedded_group
            foo = bar
          End_Group
        End_Object
        End
    """)
    test_object = label['test_object']
    assert isinstance(test_object, dict)
    assert test_object['__type__'] == 'Object'
    assert test_object['foo'] == 'bar'

    embedded_object = test_object['embedded_object']
    assert isinstance(embedded_object, dict)
    assert embedded_object['__type__'] == 'Object'
    assert embedded_object['foo'] == 'bar'

    embedded_group = test_object['embedded_group']
    assert isinstance(embedded_group, dict)
    assert embedded_group['__type__'] == 'Group'
    assert embedded_group['foo'] == 'bar'


def test_groups():
    label = labels.parse_label("""
        Group = test_group
          foo = bar
          Object = embedded_object
            foo = bar
          End_Object

          Group = embedded_group
            foo = bar
          End_Group
        End_Group
        End
    """)
    test_group = label['test_group']
    assert isinstance(test_group, dict)
    assert test_group['__type__'] == 'Group'
    assert test_group['foo'] == 'bar'

    embedded_object = test_group['embedded_object']
    assert isinstance(embedded_object, dict)
    assert embedded_object['__type__'] == 'Object'
    assert embedded_object['foo'] == 'bar'

    embedded_group = test_group['embedded_group']
    assert isinstance(embedded_group, dict)
    assert embedded_group['__type__'] == 'Group'
    assert embedded_group['foo'] == 'bar'


@pytest.mark.xfail
def test_float_corner_cases():
    label = labels.parse_label("""
        float_no_decimal = 2.
        End
    """)

    assert isinstance(label['float_no_decimal'], float)
    assert label['float_no_decimal'] == 2.0


@pytest.mark.xfail
def test_binary():
    label = labels.parse_label("""
        binary_number = 2#0101#
        End
    """)

    assert isinstance(label['binary_number'], int)
    assert label['binary_number'] == 5


@pytest.mark.xfail
def test_octal():
    label = labels.parse_label("""
        octal_number = 8#0107#
        End
    """)

    assert isinstance(label['octal_number'], int)
    assert label['octal_number'] == 71


@pytest.mark.xfail
def test_hex():
    label = labels.parse_label("""
        hex_number_upper = 16#100A#
        hex_number_lower = 16#100b#
        End
    """)

    assert isinstance(label['hex_number_upper'], int)
    assert label['hex_number_upper'] == 4106

    assert isinstance(label['hex_number_lower'], int)
    assert label['hex_number_lower'] == 4107


@pytest.mark.xfail
def test_quotes():
    label = labels.parse_label("""
        foo = 'bar'
        empty = ''
        space = '  test  '
        double = "double'quotes"
        single = 'single"quotes'
        number = '123'
        date = '1918-05-11'
        End
    """)

    assert isinstance(label['foo'], str)
    assert label['foo'] == 'bar'

    assert isinstance(label['empty'], str)
    assert label['empty'] == ''

    assert isinstance(label['space'], str)
    assert label['space'] == '  test  '

    assert isinstance(label['double'], str)
    assert label['double'] == "double'quotes"

    assert isinstance(label['single'], str)
    assert label['single'] == 'single"quotes'

    assert isinstance(label['number'], str)
    assert label['number'] == '123'

    assert isinstance(label['date'], str)
    assert label['date'] == '1918-05-11'


@pytest.mark.xfail
def test_comments():
    label = labels.parse_label("""
        /* comment on line */
        foo = bar /* comment at end of line */
        End
    """)

    assert isinstance(label['foo'], str)
    assert label['octal_number'] == 'bar'


def test_dates():
    pytest.xfail('unimplemented')


@pytest.mark.xfail
def test_set():
    label = labels.parse_label("""
        strings = {a, b, c}
        nospace={a,b,c}
        numbers = {1, 2, 3}
        mixed = {a, 1, 2.5}
        multiline = {a,
                     b,
                     c}
        empty = {}
        End
    """)

    assert isinstance(label['strings'], set)
    assert len(label['strings']) == 3
    assert 'a' in label['strings']
    assert 'b' in label['strings']
    assert 'c' in label['strings']

    assert isinstance(label['nospace'], set)
    assert len(label['nospace']) == 3
    assert 'a' in label['nospace']
    assert 'b' in label['nospace']
    assert 'c' in label['nospace']

    assert isinstance(label['numbers'], set)
    assert len(label['numbers']) == 3
    assert 1 in label['numbers']
    assert 2 in label['numbers']
    assert 3 in label['numbers']

    assert isinstance(label['mixed'], set)
    assert len(label['mixed']) == 3
    assert 'a' in label['mixed']
    assert 1 in label['mixed']
    assert 2.5 in label['mixed']

    assert isinstance(label['multiline'], set)
    assert len(label['multiline']) == 3
    assert 'a' in label['multiline']
    assert 'b' in label['multiline']
    assert 'c' in label['multiline']

    assert isinstance(label['empty'], set)
    assert len(label['empty']) == 0


def test_sequence():
    label = labels.parse_label("""
        strings = (a, b, c)
        nospace=(a,b,c)
        numbers = (1, 2, 3)
        mixed = (a, 1, 2.5)
        multiline = (a,
                     b,
                     c)
        End
    """)

    assert isinstance(label['strings'], list)
    assert len(label['strings']) == 3
    assert label['strings'][0] == 'a'
    assert label['strings'][1] == 'b'
    assert label['strings'][2] == 'c'

    assert isinstance(label['nospace'], list)
    assert len(label['nospace']) == 3
    assert label['nospace'][0] == 'a'
    assert label['nospace'][1] == 'b'
    assert label['nospace'][2] == 'c'

    assert isinstance(label['numbers'], list)
    assert len(label['numbers']) == 3
    assert label['numbers'][0] == 1
    assert label['numbers'][1] == 2
    assert label['numbers'][2] == 3

    assert isinstance(label['mixed'], list)
    assert len(label['mixed']) == 3
    assert label['mixed'][0] == 'a'
    assert label['mixed'][1] == 1
    assert label['mixed'][2] == 2.5

    assert isinstance(label['multiline'], list)
    assert len(label['multiline']) == 3
    assert label['multiline'][0] == 'a'
    assert label['multiline'][1] == 'b'
    assert label['multiline'][2] == 'c'


@pytest.mark.xfail
def test_sequence_corner_cases():
    label = labels.parse_label("""
        empty = ()
        End
    """)
    assert isinstance(label['empty'], list)
    assert len(label['empty']) == 0


def test_units():
    label = labels.parse_label("""
        foo = 42 <beards>
        g = 9.8 <m/s>
        End
    """)
    assert isinstance(label['foo'], dict)
    assert label['foo']['value'] == 42
    assert label['foo']['units'] == 'beards'

    assert isinstance(label['g'], dict)
    assert label['g']['value'] == 9.8
    assert label['g']['units'] == 'm/s'


def test_cube_label():
    with open(os.path.join(DATA_DIR, 'pattern.cub')) as fp:
        label = labels.parse_file_label(fp)

    assert isinstance(label['Label'], dict)
    assert label['Label']['Bytes'] == 65536

    assert isinstance(label['IsisCube'], dict)
    assert isinstance(label['IsisCube']['Core'], dict)
    assert label['IsisCube']['Core']['StartByte'] == 65537
    assert label['IsisCube']['Core']['Format'] == 'Tile'
    assert label['IsisCube']['Core']['TileSamples'] == 128
    assert label['IsisCube']['Core']['TileLines'] == 128

    assert isinstance(label['IsisCube']['Core']['Dimensions'], dict)
    assert label['IsisCube']['Core']['Dimensions']['Samples'] == 90
    assert label['IsisCube']['Core']['Dimensions']['Lines'] == 90
    assert label['IsisCube']['Core']['Dimensions']['Bands'] == 1

    assert isinstance(label['IsisCube']['Core']['Pixels'], dict)
    assert label['IsisCube']['Core']['Pixels']['Type'] == 'Real'
    assert label['IsisCube']['Core']['Pixels']['ByteOrder'] == 'Lsb'
    assert label['IsisCube']['Core']['Pixels']['Base'] == 0.0
    assert label['IsisCube']['Core']['Pixels']['Multiplier'] == 1.0
