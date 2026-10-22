# Lab 9: MapReduce Log Analyzer
## CS 411: Computing Paradigms (Fall 2026)

**Instructor starter repository:** https://github.com/cwillpinto/cs411-lab09-mapreduce-log-analyzer

### ⚡ The Mission
Marketing just ran a flash sale, and the CDN dumped a 1GB `access.log` in your lap two hours before the post-mortem meeting. Nobody can `grep` their way through a gigabyte fast enough to answer "which endpoints nearly fell over?" You're going to do what Google did in 2004: stop treating this as one big sequential scan, and instead split it into independent **Map** tasks that each emit small key-value facts, funnel those through a **Shuffle** (sort-and-group), and let a **Reduce** phase collapse them into the answer.

---

### Part A: Applied systems checks (20 Points)
**Instructions:** Use a small table or a few sentences for each check. Submit `Lab9_Theory.pdf` or `.md`; no essay is required.

1. **Shuffle bytes (6 points).** Twelve million log lines each emit one 40-byte `(endpoint, 1)` pair. Show the total mapper output in decimal MB. With four shared machines and even placement, estimate the bytes crossing the network and state the local-pair assumption.
2. **Lost work (6 points).** Mapper task 3 fails halfway through its input split. In 2–3 sentences, say what the scheduler reruns, what happens to its partial output, and how Spark lineage could rebuild the equivalent lost partition when a usable parent is cached.
3. **Find the bottleneck (8 points).** Fill two rows in a table: (a) seven mappers take 10 seconds and one takes 90 seconds; (b) three reducers take 12 seconds and one receives 78% of keys and takes 95 seconds. For each row, give the earliest stage finish time, identify a slow task or hot key, and name one measurement and one practical mitigation. Keep each explanation to 1–3 sentences.

---

### Part B: Build and verify the analyzer (80 Points)
**Instructions:** Complete `mapper.py` and `reducer.py` against the supplied `logs.txt` sample. The 1 GB scenario is conceptual; this local run does not use a cluster.

**Requirements:**
1. **Mapper (20 points):** Read `logs.txt` from standard input, extract each valid request path, and emit `<endpoint>\t1`. Skip malformed records.
2. **Streaming reducer (30 points):** Read the sorted tab-separated pairs from standard input. Count one endpoint at a time, save a group when its key changes, and flush the final group at end of input. Do not load the full pair stream into memory.
3. **Top 10 (20 points):** Sort completed endpoint totals by descending count, then endpoint name ascending for ties. Print at most ten `<endpoint>\t<count>` lines.
4. **Verification (10 points):** Run `python mapper.py < logs.txt | sort | python reducer.py > output.txt`, then `python check_logs.py output.txt`. Record the output and `MAPREDUCE_SHUFFLE_VERIFIED` token. Also inspect the empty-input, final-group, and tie cases; the sample token alone does not prove every case.

---

### 🚀 Submission
1. `Lab9_Theory.pdf` (or `.md`) with the three short applied checks
2. Your student-owned GitHub repository URL and full commit SHA in Blackboard Ultra. Use the public instructor template at `https://github.com/cwillpinto/cs411-lab09-mapreduce-log-analyzer` as the starter. Your repository must contain your completed `mapper.py` and `reducer.py`; do not upload separate code files or push to the instructor starter.
3. The **Success Token** (`MAPREDUCE_SHUFFLE_VERIFIED`) output from `check_logs.py`, with terminal output or screenshot.

See `README.md` for template and safe direct-clone instructions. The instructor-approved due time is Wednesday, October 28, 2026, 11:59 PM America/Chicago. The live Blackboard setting remains unverified.
