# Lab 9: MapReduce Log Analyzer
## CS 411: Computing Paradigms (Fall 2026)

### ⚡ The Mission
Marketing just ran a flash sale, and the CDN dumped a 1GB `access.log` in your lap two hours before the post-mortem meeting. Nobody can `grep` their way through a gigabyte fast enough to answer "which endpoints nearly fell over?" You're going to do what Google did in 2004: stop treating this as one big sequential scan, and instead split it into independent **Map** tasks that each emit small key-value facts, funnel those through a **Shuffle** (sort-and-group), and let a **Reduce** phase collapse them into the answer.

---

### Part A: The Systems Analyst (50 Points)
**Instructions:** Answer the following questions in a separate document (PDF or Markdown). Show calculations and concise explanations tied to the requested cases; no essay is required.

1. **Shuffle volume.** A 1GB access log is split evenly across N=8 mapper tasks. Each mapper emits one intermediate key-value pair per log line in the form `(endpoint, 1)`, and the average serialized size of an intermediate pair (key + value + framing) is 40 bytes. The log has roughly 12 million lines total. If the intermediate output is partitioned evenly across M=4 reducers, compute (a) the total volume of intermediate data written to local disk by all mappers combined, and (b) the volume that must cross the network during the shuffle phase (i.e., excluding pairs that happen to land on the same machine that produced them, assuming mappers and reducers run on 4 shared machines with 2 mapper slots each).
2. **Failure and re-execution.** Mapper task 3 (of the 8) crashes after emitting half its intermediate output. Under classic MapReduce's fault-tolerance model, describe exactly what the master/scheduler does: which task(s) re-run, from what input, and whether any reducer that already started reading mapper 3's *partial* output is affected. Now contrast this with Spark: if the equivalent partition's RDD computation fails, what does Spark recompute using RDD lineage, and why can it typically recover faster than re-running mapper 3's task from scratch when the input logs are cached in memory across an interactive session?
3. **Systems reasoning.** MapReduce enforces a hard barrier — no reducer may begin its reduce phase until *every* mapper has finished (because any mapper could still emit a key destined for that reducer). What is the throughput cost of this barrier when 7 of 8 mappers finish in 10 seconds but 1 straggler takes 90 seconds? Name one mechanism real MapReduce clusters use to mitigate stragglers.
4. **Key skew.** Now suppose that instead of a straggler, one reducer receives 78% of all intermediate keys due to a skewed key distribution (a classic "hot key" problem — e.g., one status code dominating the log). If the other 3 reducers finish in 12 seconds but the hot reducer takes 95 seconds, what is the overall job's wall-clock time? Explain why this is a *distinct* failure mode from Problem 3's straggler (a slow machine vs. an inherently imbalanced key distribution), and name one practical mitigation (e.g., salting keys, combiners) that would reduce this skew.

---

### Part B: The Implementation (50 Points)
**Instructions:** Write a `mapper.py` and `reducer.py` that together compute, from a 1GB (simulated locally with a provided sample) nginx-style `access.log`, the top-10 most-requested endpoints and each endpoint's total hit count — so the team knows which routes to scale before the next sale.

**Requirements:**
1. `mapper.py` reads `access.log` line by line, extracts the request path (e.g., `/checkout`), and writes one line per request to stdout in the form `<endpoint>\t1`.
2. `reducer.py` reads tab-separated `<endpoint>\t1` pairs from stdin (already grouped by `sort`), accumulates a running count per endpoint as the sorted stream advances, and on a key change prints `<endpoint>\t<total_count>`. It must not load the entire input into memory at once — this is the whole point of relying on `sort` to pre-group keys for the shuffle.
3. After the reduce phase, the output must be sorted descending by count and truncated to the top 10 lines (either inside `reducer.py` or in a small `topk.py` you pipe the output through).
4. **Verification:** Run `python mapper.py < logs.txt | sort | python reducer.py > output.txt`. Then run the provided grading script: `python check_logs.py output.txt`. It independently recomputes the top-10 endpoints and diffs against your output. On a match it prints the **Success Token** `MAPREDUCE_SHUFFLE_VERIFIED`. The token supports the behavior checked by that script.

---

### 🚀 Submission
1. `Lab9_Theory.pdf` (or `.md`)
2. Your student-owned GitHub repository URL and full commit SHA in Blackboard Ultra. Use the public instructor template at `https://github.com/cwillpinto/cs411-lab09-mapreduce-log-analyzer` as the starter. Your repository must contain your completed `mapper.py` and `reducer.py`; do not upload separate code files or push to the instructor starter.
3. The **Success Token** (`MAPREDUCE_SHUFFLE_VERIFIED`) output from `check_logs.py`, with terminal output or screenshot.

See `README.md` for template and safe direct-clone instructions. The due date is October 26, 2026; use the Blackboard assignment for the verified deadline time.
