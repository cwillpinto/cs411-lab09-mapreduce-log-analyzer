# CS411 Lab 9 — MapReduce Log Analyzer

Read `Lab_09_MapReduce_Log_Analyzer.md` for the 100-point assignment and its October 26, 2026 due date. Check Blackboard Ultra for the exact deadline time. Python 3.11 or newer and the standard library are required; no third-party packages are needed.

## Student workflow

If the instructor starter is a template, select **Use this template** on GitHub, create a repository under your own account, and clone it locally. For a direct clone, create an empty repository under your account first:

```sh
git clone https://github.com/cwillpinto/cs411-lab09-mapreduce-log-analyzer.git
cd cs411-lab09-mapreduce-log-analyzer
git remote rename origin upstream
git remote add origin <your-repository-url>
git remote -v
git push -u origin <your-branch>
```

Check that `origin` points to your repository before pushing. Do not push to the instructor repository. Commit your code and copy its full SHA with `git rev-parse HEAD`.

## Work and verification

Implement the TODOs in `mapper.py` and `reducer.py`. Keep `check_logs.py` unchanged. Send raw logs to the mapper:

```sh
python mapper.py < logs.txt | sort | python reducer.py > output.txt
python check_logs.py output.txt
```

Expected token on a matching sample: `MAPREDUCE_SHUFFLE_VERIFIED`. The starter intentionally raises `NotImplementedError` until completed. `logs.txt` is a 300-line sample, not a 1 GB file or a local cluster.

## Submission

Submit your student-owned repository URL and full commit SHA, `Lab9_Theory.pdf` or `.md` with concise calculations and case explanations, and terminal output or a screenshot showing the success token. Your completed code lives in your repository; separate code-file uploads are not required. Disclose AI tool use as required by the syllabus.
