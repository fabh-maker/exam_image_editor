from typing import List
from image_editor.editor import ImageEditor
from image_editor.elements import TupleRC
from image_editor.exceptions import ImageEditorException


IMG_PATH = "data/img.txt"


def bitmap_str(bitmap: List[List[int]]):
    return "\n".join([" ".join(["{:3}".format(p) for p in row]) for row in bitmap])


def main():
    print("----------------- R1 -----------------")
    editor = ImageEditor()

    r1 = editor.new_rectangle("r1", TupleRC(3, 5), 9)
    print(r1.name)                      # r1
    print((r1.dims.r, r1.dims.c))       # (3, 5)
    print(bitmap_str(r1.bitmap))
    #   9   9   9   9   9
    #   9   9   9   9   9
    #   9   9   9   9   9
        
    im1 = editor.new_image("im1", IMG_PATH) 
    print(im1.name)                     # im1
    print((im1.dims.r, im1.dims.c))     # (5, 6)
    print(bitmap_str(im1.bitmap))
    #   1   2   3   4   5   6
    #   1   2   3   4   5   6
    #   1   2   3   4   5   6
    #   1   2   3   4   5   6
    #   1   2   3   4   5   6

    try:
        editor.new_rectangle("im1", TupleRC(3, 5), 9)
        print("[Error] Duplicated graphical element not detected")
    except ImageEditorException:
        print("Duplicated graphical element correctly identified")   # Duplicate graphical element correctly identified

    print("----------------- R2 -----------------")
    try:
        editor.add_layer("im2", TupleRC(1, 1))
        print("[Error] Missing graphical element not detected")
    except ImageEditorException:
        print("Correctly detected: Missing graphical element")  # Correctly detected: Missing graphical element

    l1 = editor.add_layer("im1", TupleRC(0, 0))
    l2 = editor.add_layer("r1", TupleRC(2, 3))
    l3 = editor.add_layer("r1", TupleRC(0, -1))

    print([
        l1.elm.name,
        l2.elm.name,
        l3.elm.name
    ])  # ['im1', 'r1', 'r1']

    print([
        (l1.pos.r, l1.pos.c),
        (l2.pos.r, l2.pos.c),
        (l3.pos.r, l3.pos.c)
    ])  # [(0, 0), (2, 3), (0, -1)]

    print([
        l1.below is None,
        l2.below == l1,
        l3.below == l2
    ])  # [True, True, True]

    print([
        l1.above == l2,
        l2.above == l3,
        l3.above is None
    ])  # [True, True, True]

    print("----------------- R3 -----------------")
    editor.move_below(l3)
    editor.move_below(l3)
    editor.move_below(l3)
    editor.move_below(l2)

    print([
        l3.below is None,
        l2.below == l3,
        l1.below == l2
    ])  # [True, True, True]

    print([
        l3.above == l2,
        l2.above == l1,
        l1.above is None
    ])  # [True, True, True]

    print("----------------- R4 -----------------")
    r_test = editor.new_rectangle("r_test", TupleRC(4, 5), 111)
    img_test = editor.new_image("img_test", IMG_PATH)
    r_test.overlay(img_test, TupleRC(-2, -3))
    print(bitmap_str(r_test.bitmap))
    #   4   5   6 111 111
    #   4   5   6 111 111
    #   4   5   6 111 111
    # 111 111 111 111 111
    
    editor = ImageEditor()
    editor.new_rectangle("r1", TupleRC(3, 5), 9)
    editor.new_image("im1", IMG_PATH)

    l1 = editor.add_layer("im1", TupleRC(0, 0))
    l2 = editor.add_layer("r1", TupleRC(2, 3))
    l3 = editor.add_layer("r1", TupleRC(0, -1))

    print()
    print(bitmap_str(l3.render(TupleRC(6, 7)).bitmap))
    #   9   9   9   9   5   6   0
    #   9   9   9   9   5   6   0
    #   9   9   9   9   9   9   9
    #   1   2   3   9   9   9   9
    #   1   2   3   9   9   9   9
    #   0   0   0   0   0   0   0

    print()
    print(bitmap_str(l2.render(TupleRC(4, 5)).bitmap))
    #   1   2   3   4   5
    #   1   2   3   4   5
    #   1   2   3   9   9
    #   1   2   3   9   9    

    # check if graphical elements in layers have changed
    print(l1.elm.bitmap == [[i for i in range(1, 7)] for _ in range(5)])  # True
    print(l2.elm.bitmap == [[9]*5 for _ in range(3)])                    # True
    print(l3.elm.bitmap == [[9]*5 for _ in range(3)])                    # True


if __name__ == "__main__":
    main()
