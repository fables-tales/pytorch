import sys

from benchmark_base import BenchmarkBase

import torch


class Benchmark(BenchmarkBase):
    N = 1000

    def name(self):
        return "symint_sum"

    def description(self):
        return "see https://docs.google.com/document/d/11xJXl1etSmefUxPiVyk885e0Dl-4o7QwxYcPiMIo2iY/edit"

    def _prepare_once(self):
        torch._dynamo.config.capture_scalar_outputs = True
        torch.manual_seed(0)

        self.splits = torch.randint(10, (self.N,))

    def _prepare(self):
        torch._dynamo.reset()

    def _work(self):
        @torch.compile(fullgraph=True)
        def f(a):
            xs = a.tolist()
            y = sum(xs)
            return torch.tensor(y)

        f(self.splits)


def main():
    result_path = sys.argv[1]
    Benchmark().enable_compile_time_instruction_count().collect_all().append_results(
        result_path
    )


if __name__ == "__main__":
    main()
