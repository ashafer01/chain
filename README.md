# Python function chaining

Replace ugly nested function calls with a chained expression.

Note that this tends to actually make them take up more space, but vastly
improves readability. Code golfers look elsewhere.

Basic usage:

```python
from chain import chain, args

def multiply(a, b):
    return a * b

x = chain(args(2, 3) | multiply)
y = multiply(2, 3)

assert x == y
```

We'll call the part inside the `chain()` call a "pipeline expression".

A pipeline expression must begin with an `args()` instance. Further, it is not
technically required that any piped objects exist, and so a "pipeline
expression" can consist of just an `args()`.

As the example above demonstrates, `args()` represents anonymous arguments to
be passed into the next piped object.

As the pipeline progresses, the return of the previous function is used as the
argument to the next:

```python
# continued from previous example

def negate(a):
    return -a

x = chain(args(2, 3) | multiply | negate)
y = negate(multiply(2, 3))

assert x == y
```

If you need to *append* additional positional arguments or update keyword
arguments, then you can add a new `args()` into the pipeline:

```python
# continued from previous example

x = chain(args(2, 3) | multiply | negate | args(-3) | multiply)
y = multiply(negate(multiply(2, 3)), -3)

assert x == y
```

If you need to put the return value into arbitrary positions in a completely
new argument set, you can define a function accepting the single return value
from the pipeline and returning a new `args()`:

```python
# continued from previous example

def day_to_dt(day):
    return args(year=2019, month=8, day=day)

from datetime import datetime

x = chain(args(2, 3) | multiply | negate | args(-3) | multiply | day_to_dt | datetime)
y = datetime(year=2019, day=multiply(negate(multiply(2, 3)), -3), month=8)

assert x == y
```

In this example it would be equivalent to have the `day_to_dt()` function just
return a new `datetime()` directly; however, this demonstrates the ability to
completely and arbitrarily change the argument set of the pipeline.

Note that if a pipeline ends with a function similar to the example above, then
the pipeline's return value will be `None`. In order to manipulate the return
value of the pipeline, set a vaue to the `value` attribute on your `args()`
instance before returning. This value will not be used if the pipeline
does not end with such a function.


## Alternative Uses

1. You can replace `chain(<pipeline>)` with `(<pipeline>).value`.

2. If you already have a sequence of callables that you use in a similar manner,
you can append them to a pipeline by passing them as arguments to `chain()`:

```python
# ...

from chain import chain, args

my_funcs = (transform, mogrify, vectorize, app.render)
render_successful = chain(args('hello', 'world'), *my_funcs, check_result)
```

Note that you can pass an arbitrary pipeline expression as the first argument,
but passing additional pipeline expressions beyond single new `args()` will
treat that as an isolated pipeline and it will get processed *before* the
`chain()` call is made, in accordance with normal Python behavior. This will
likely appear to work unexpectedly and thus is not recommended, but the
behavior is consistent:

### Embedded secondary pipelines in a `chain()` call

*Not recommended*

The embedded pipeline will always emit its final `args()` instance as an
argument to `chain()` which would get treated as if it were a part of the
existing (outer) pipeline.

How this works varies with whether or not the outer pipeline ends with the
embedded pipeline, or has other piped elements after it.

If the embedded pipeline is the 2nd through 2nd to last argument:
* If the embedded pipeline ended with a normal callable, then that return
  value will become a 2nd argument on the pipeline, with the return value
  before the embedded pipeline as the 1st argument.
* If the embedded pipeline itself ended with an `args()` or a function
  returning an `args()` then that will become the state of the outer pipeline
  entirely. Any arguments it carries will be passed to the next object, and
  any return value it carries will be abandoned.

If the outer pipeline ends with an embedded pipeline:
* any arguments it is carrying will be abandonded (as with any pipeline)
* Any prior return value of the outer pipeline will be abandoned and the return
  value of the pipeline will become the return value of the embedded pipeline

Note that starting a pipeline expression with a callable is not possible even
as secondary arguments to `chain()`. Pipeline expressions must always start
with an `args()`.
