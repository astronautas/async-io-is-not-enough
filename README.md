Goal: illustrate that the more app becomes CPU heavy vs I/O heavy, the more Go has an advantage over Python, because of its true parallelism, unlike Python's GIL. Why? Because Go can run multiple goroutines in parallel, while Python can't run multiple threads in parallel due to the GIL, even if you use asyncio. Multiprocessing is an option, but it's not as easy to use as goroutines.

Idea - the more CPU heavy the app is, the more Python struggles and needs tricks to parallelize, while Go is just easier to parallelize. Show that asyncio is not a silver bullet, because of GIL, and multiprocessing is not as easy to use as goroutines.

Also explore Python 3.13 new features - no GIl, and how it compares to Go.

1. Python serial vs Go serial, IO dominated:
```bash
cd python
PYTHON_GIL=1 uv run benchmark.py --serial --io  

cd go
GOMAXPROCS=1 go run benchmark.go --serial --io
```

1. Python GIL threaded vs Go goroutines, IO dominated:
```bash
cd python
PYTHON_GIL=1 uv run benchmark.py

cd go
go run benchmark.go
```




Comparisons:
* Python serial vs Go serial, IO dominated. Go is bit faster because of compiled nature, but scales similarly.
* Python GIL threaded vs Go goroutines, IO dominated. Show async-io way of doing. Go is bit faster because of compiled nature, but scales similarly.
* Python GIL threaded vs Go goroutines, CPU heavy (Python is slower because of GIL). Also show async-io does not solve the problem.
* Python GIL multiprocess vs Go goroutines, CPU heavy (Python is slower because of GIL, but kind of near Go because of multiprocess).
* Python NO GIL threaded vs Go goroutines, CPU heavy (Python is faster because of no GIL).
* Python NO GIL async-io discussion (show links to potential discussions).

idea - show that Go is just easier to parallelize than Python, Python needs tricks, asyncio is not a silver bullet (because of GIL), multiprocessing is not as easy to use as goroutines. But Python 3.13 is coming with no GIL, so promising!

next - compare overhead of goroutines vs asyncio, multiprocessing.

TODO:
- [x] Benchmark serial vs goroutines, IO dominated
- [x] Benchmark adding goroutines to Go, IO dominated
- [x] Benchmark GIL threaded vs. asyncio vs goroutines, IO dominated
- [ ] Benchmark GIL threaded vs asyncio vs. goroutines, CPU heavy
- [ ] Benchmark GIL multiprocess vs goroutines, CPU heavy
- [ ] Benchmark NO GIL threaded vs goroutines, CPU heavy
- [ ] Section on async-io
- [ ] Blog post