**DISCLAIMER**: Questa è una traduzione del file README.md in cinese effettuata tramite uno strumento automatico (ChatGPT), su richiesta di uno/a studente/essa.
Non ci assumiamo responsabilità sulla correttezza ed equivalenza del contenuto.

# 图像编辑器

编写一个 Python 程序，用于组合图像。

模块和类应在 *image\_editor* 包中开发。
不要移动或重命名现有的模块和类，也不要修改方法的签名。

在 *main.py* 中提供了简单的测试代码，你可以修改它，用于测试基本功能。
它展示了对所需控件主要方法的使用示例。

除非另有说明，所有异常均为模块 *exceptions* 中定义的 *ImageEditorException* 类型。

## R1: 图形元素（5/18）

已经实现的 *TupleRC* 数据类表示一个行 (r) 和列 (c) 值的元组。

模块 *elements* 中定义的抽象类 *GraphicalElement* 表示一个图形元素。
图形元素本质上是一个二维像素矩阵。
每个像素由一个范围在 \[0, 255] 的整数表示，表示其灰度颜色（0->黑色，255->白色）。

该类包含以下属性：

* `name(self) -> str` 图形元素的名称。
* `dims(self) -> TupleRC` 图形元素的尺寸，以像素矩阵的行数和列数表示，封装为一个 *TupleRC*（r = 行，c = 列）。
* `bitmap(self) -> List[List[int]]` 图形元素的像素矩阵（**抽象属性**）。

模块 *image\_editor* 中定义的 *ImageEditor* 类允许创建两种类型的图形元素。

方法

```python
new_rectangle(self, name: str, dims: TupleRC, color: int) -> GraphicalElement
```

返回一个单色矩形图形元素（所有像素具有相同颜色），其名称、尺寸和颜色由参数指定。

方法

```python
new_image(self, name: str, fname: str) -> GraphicalElement
```

返回从文件加载的图像所表示的图形元素。
该方法接受图形元素名称和文件名作为参数。图像以文本格式保存。
文件中的每一行表示像素矩阵的一行，每个像素的颜色用空格分隔的整数表示。
示例图像文件为 *data/img.txt*。

如果尝试定义一个已存在名称的图形元素（无论类型如何），方法 `new_rectangle` 和 `new_image` 都会抛出异常。

**注意**：当方法的返回类型为 **GraphicalElement** 时，也包括其子类（**GraphicalElement** 是抽象类）。

## R2: 图层（5/18）

模块 *elements* 中定义的 *Layer* 类表示通过程序组合图像时使用的图层。
每个图层包含一个图形元素，在最终合成图像中，该图形元素将覆盖在下方图层的元素之上。
图形元素在图层中的位置通过其左上角像素的行列坐标（r, c）定义。

该类具有以下属性：

* `elm(self) -> GraphicalElement` 图层中的图形元素。
* `pos(self) -> TupleRC` 图形元素的位置。
* `below(self) -> Optional["Layer"]` 下方图层，如果是最底层则为 **None**。
* `above(self) -> Optional["Layer"]` 上方图层，如果是最顶层则为 **None**。

类 *ImageEditor* 的方法

```python
add_layer(self, elm_name: str, pos: TupleRC) -> Layer
```

允许创建一个新图层，并将其添加到现有图层的顶部。
该方法接收要插入图层的图形元素名称及其位置。
**同一个图形元素** 可以被插入到 **多个图层中**。
如果指定的图形元素尚未定义，该方法会抛出异常。

**注意**：图层中图形元素的位置坐标 (r, c) 可以是负数。

**提示**：图层之间的连接（**above** 和 **below** 属性）形成一个双向链表。

## R3: 图层重新排序（4/18）

类 *ImageEditor* 的方法

```python
move_below(self, layer: Layer) -> None
```

允许将指定图层下移一层。
所有受影响图层的 *below* 和 *above* 链接都必须更新。
如果指定图层已经是最底层，则不应进行任何更改。

## R4: 渲染（4/18）

类 *GraphicalElement* 的方法

```python
overlay(self, layer: "GraphicalElement", pos: TupleRC) -> None
```

允许在当前图形元素上叠加另一个图形元素。
该方法接收要叠加的图形元素及其位置 (r, c) 作为参数。
假设要修改的图形元素位于 (0, 0)。

被修改的图形元素 **不应改变其尺寸**，但其像素颜色在重叠区域内应取覆盖元素的颜色。

被叠加的图形元素 **不应被修改**。

类 *Layer* 的方法

```python
render(self, dims: TupleRC) -> GraphicalElement
```

允许对图层进行渲染，**创建一个图形元素**，它是该图层及其下方所有图层中图形元素的叠加结果。
从最底层图层开始，将每个图层中的图形元素依次叠加到一个新的矩形图形元素上，该元素作为背景。
背景图形元素的位置为 (0, 0)，其尺寸为方法参数指定的值，即最终图像的尺寸。
背景矩形应为黑色（0）。

**不得修改任何图层中包含的图形元素。**

**提示**：为实现渲染，可先创建一个背景图形元素，并对其多次调用 **overlay** 方法，逐个叠加各图层中的图形元素。
这样可以保证图层中的原始图形元素不会被修改。
