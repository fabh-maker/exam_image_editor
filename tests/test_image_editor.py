import unittest
import inspect
from image_editor.editor import ImageEditor
from image_editor.elements import GraphicalElement, TupleRC
from image_editor.exceptions import ImageEditorException

TEST_IMAGE = "tests/data_test/img_test.txt"


class TestR0(unittest.TestCase):

    def test_abstract(self):
        self.assertTrue(inspect.isabstract(GraphicalElement))


class TestR1(unittest.TestCase):

    def setUp(self):
        self._editor = ImageEditor()

    def test_new_rectangle(self):
        rect = self._editor.new_rectangle("rect1", TupleRC(5, 7), 44)
        self.assertEqual(rect.name, "rect1")
        self.assertEqual(TupleRC(5, 7), rect.dims)

    def test_new_image(self):
        rect = self._editor.new_image("img1", TEST_IMAGE)
        self.assertEqual(rect.name, "img1")
        self.assertEqual(TupleRC(6, 6), rect.dims)

    def test_rectangle_bitmap(self):
        rect = self._editor.new_rectangle("rect1", TupleRC(5, 4), 44)
        bitmap = rect.bitmap
        self.assertEqual(5, len(bitmap))
        for row in bitmap:
            self.assertEqual([44]*4, row)

    def test_image_bitmap(self):
        img = self._editor.new_image("img1", TEST_IMAGE)
        bitmap = img.bitmap
        self.assertEqual(6, len(bitmap))
        for idx, row in enumerate(bitmap):
            self.assertEqual([idx]*6, row)

    def test_duplicate_exception(self):
        self._editor.new_rectangle("e1", TupleRC(5, 7), 44)
        self._editor.new_image("e2", TEST_IMAGE)
        self.assertRaises(ImageEditorException, self._editor.new_rectangle, "e2", TupleRC(3, 3), 11)
        self.assertRaises(ImageEditorException, self._editor.new_image, "e1", TEST_IMAGE)


class TestR2(unittest.TestCase):

    def setUp(self):
        self._editor = ImageEditor()

    def test_layer_exception(self):
        self._editor.new_rectangle("rect1", TupleRC(5, 7), 44)
        self._editor.add_layer("rect1", TupleRC(1, 2))
        self.assertRaises(ImageEditorException, self._editor.add_layer, "rect2", TupleRC(-1, -1))

    def test_layer_content(self):
        self._editor.new_rectangle("rect1", TupleRC(5, 7), 44)
        self._editor.new_image("img1", TEST_IMAGE)

        layer1 = self._editor.add_layer("img1", TupleRC(-4, 7))
        layer2 = self._editor.add_layer("rect1", TupleRC(3, 2))

        self.assertEqual("img1", layer1.elm.name)
        self.assertEqual("rect1", layer2.elm.name)

        self.assertEqual(TupleRC(-4, 7), layer1.pos)
        self.assertEqual(TupleRC(3, 2), layer2.pos)

    def test_layer_chain_top_down(self):
        self._editor.new_rectangle("rect1", TupleRC(5, 7), 44)
        self._editor.new_image("img1", TEST_IMAGE)

        layer1 = self._editor.add_layer("rect1", TupleRC(0, 0))
        layer2 = self._editor.add_layer("img1", TupleRC(3, 2))
        layer3 = self._editor.add_layer("rect1", TupleRC(1, 1))

        self.assertEqual(layer2, layer3.below)
        self.assertEqual(layer1, layer2.below)

    def test_layer_chain_bottom_up(self):
        self._editor.new_rectangle("rect1", TupleRC(5, 7), 44)
        self._editor.new_image("img1", TEST_IMAGE)

        layer1 = self._editor.add_layer("rect1", TupleRC(0, 1))
        layer2 = self._editor.add_layer("img1", TupleRC(3, 2))
        layer3 = self._editor.add_layer("rect1", TupleRC(1, 1))

        self.assertEqual(layer2, layer1.above)
        self.assertEqual(layer3, layer2.above)

    def test_layer_none(self):
        self._editor.new_rectangle("rect1", TupleRC(5, 7), 44)
        self._editor.new_image("img1", TEST_IMAGE)

        layer1 = self._editor.add_layer("rect1", TupleRC(-3, 0))
        layer2 = self._editor.add_layer("img1", TupleRC(3, 2))

        self.assertIsNone(layer2.above)
        self.assertIsNone(layer1.below)
        self.assertIsNotNone(layer1.above)
        self.assertIsNotNone(layer2.below)


class TestR3(unittest.TestCase):

    def check_layer_order(self, layer, *layers):
        layers = [layer, *layers]
        self.assertIsNone(layers[0].below)
        self.assertIsNone(layers[-1].above)
        for i in range(len(layers)-1):
            self.assertEqual(layers[i+1], layers[i].above)
            self.assertEqual(layers[i], layers[i+1].below)

    def setUp(self):
        self._editor = ImageEditor()
        self._editor.new_rectangle("rect1", TupleRC(5, 4), 1)
        self._layer1 = self._editor.add_layer("rect1", TupleRC(0, 0))
        self._layer2 = self._editor.add_layer("rect1", TupleRC(2, 2))
        self._layer3 = self._editor.add_layer("rect1", TupleRC(-1, -1))
    
    def test_move_below_bottom(self):
        self.check_layer_order(self._layer1, self._layer2, self._layer3)
        self._editor.move_below(self._layer1)
        self.check_layer_order(self._layer1, self._layer2, self._layer3)

    def test_move_below_top(self):
        self.check_layer_order(self._layer1, self._layer2, self._layer3)
        self._editor.move_below(self._layer3)
        self.check_layer_order(self._layer1, self._layer3, self._layer2)

    def test_move_middle_to_middle(self):
        self.check_layer_order(self._layer1, self._layer2, self._layer3)
        self._editor.move_below(self._layer2)
        self.check_layer_order(self._layer2, self._layer1, self._layer3)

    def test_move_middle_to_bottom(self):
        self._layer4 = self._editor.add_layer("rect1", TupleRC(1, 1))
        self.check_layer_order(self._layer1, self._layer2, self._layer3, self._layer4)
        self._editor.move_below(self._layer3)
        self.check_layer_order(self._layer1, self._layer3, self._layer2, self._layer4)


class TestR4(unittest.TestCase):

    def setUp(self):
        self._editor = ImageEditor()

    def test_overlay_simple(self):        
        rect1 = self._editor.new_rectangle("rect1", TupleRC(3, 4), 9)
        img1 = self._editor.new_image("img1", TEST_IMAGE)
        img1.overlay(rect1, TupleRC(2, 2))
        expected = [
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [2, 2, 9, 9, 9, 9],
            [3, 3, 9, 9, 9, 9],
            [4, 4, 9, 9, 9, 9],
            [5, 5, 5, 5, 5, 5]
        ]
        self.assertEqual(expected, img1.bitmap)        

    def test_overlay_complex(self):
        rect1 = self._editor.new_rectangle("rect1", TupleRC(5, 5), 9)
        img1 = self._editor.new_image("img1", TEST_IMAGE)
        rect1.overlay(img1, TupleRC(1, 1))
        expected = [
            [9, 9, 9, 9, 9],
            [9, 0, 0, 0, 0],
            [9, 1, 1, 1, 1],
            [9, 2, 2, 2, 2],
            [9, 3, 3, 3, 3]
        ]
        self.assertEqual(expected, rect1.bitmap)

    def test_render_top(self):
        self._editor.new_rectangle("rect1", TupleRC(6, 5), 7)
        self._editor.new_image("img1", TEST_IMAGE)
        self._editor.new_rectangle("rect2", TupleRC(3, 4), 9)
        self._editor.add_layer("rect1", TupleRC(0, 0))
        self._editor.add_layer("img1", TupleRC(-2, -2))
        layer = self._editor.add_layer("rect2", TupleRC(2, 2))        

        expected = [
            [2, 2, 2, 2, 7, 0, 0],
            [3, 3, 3, 3, 7, 0, 0],
            [4, 4, 9, 9, 9, 9, 0],
            [5, 5, 9, 9, 9, 9, 0],
            [7, 7, 9, 9, 9, 9, 0],
            [7, 7, 7, 7, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

        self.assertEqual(expected, layer.render(TupleRC(7, 7)).bitmap)

    def test_render_middle_unchanged(self):
        rect1 = self._editor.new_rectangle("rect1", TupleRC(5, 5), 7)
        img1 = self._editor.new_image("img1", TEST_IMAGE)
        rect2 = self._editor.new_rectangle("rect2", TupleRC(3, 4), 9)
        self._editor.add_layer("rect1", TupleRC(0, 0))
        layer = self._editor.add_layer("img1", TupleRC(-2, -2))
        self._editor.add_layer("rect2", TupleRC(2, 2))        
        expected = [
            [2, 2, 2, 2, 7],
            [3, 3, 3, 3, 7],
            [4, 4, 4, 4, 7],
            [5, 5, 5, 5, 7],
        ]
        self.assertEqual(expected, layer.render(TupleRC(4, 5)).bitmap)
        self.assertEqual([[7]*5 for _ in range(5)], rect1.bitmap)
        self.assertEqual([[i]*6 for i in range(6)], img1.bitmap)
        self.assertEqual([[9]*4 for _ in range(3)], rect2.bitmap)
