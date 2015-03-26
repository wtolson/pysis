# -*- coding: utf-8 -*-
from pysis.util import (
    file_variations,
    ImageName,
)


def test_file_variations():
    result = file_variations('image.IMG', ['.cub', '.cal.cub'])
    assert len(result) == 2
    assert result[0] == 'image.cub'
    assert result[1] == 'image.cal.cub'

    result = file_variations('foo/image', ['.TIFF'])
    assert len(result) == 1
    assert result[0] == 'foo/image.TIFF'


def test_image_name():
    assert ImageName('test') == 'test'
    assert ImageName('image').IMG == 'image.IMG'
    assert ImageName('image').cal.cub == 'image.cal.cub'
    assert ImageName('foo/image.bar').baz == 'foo/image.bar.baz'
