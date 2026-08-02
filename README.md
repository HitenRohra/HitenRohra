<div align="center">

<img src="./ascii.svg" width="460" alt="Hiten Rohra"/>

<img src="./stats.svg" width="620" alt="Contributions in the last year"/>

[hitenraju.com](https://hitenraju.com) &nbsp;·&nbsp;
[linkedin](https://linkedin.com/in/hiten-rohra) &nbsp;·&nbsp;
[email](mailto:hraju@usc.edu)

</div>

<img src="./hd-about.svg" width="620" alt="about"/>

> Software engineer. MS CS at USC, in Los Angeles.<br>
> I like the part of the problem where the latency budget stops being polite.

Two years shipping production backends — five monoliths pulled apart into<br>
twelve services, a monitoring platform that a hundred-odd engineers now open<br>
before they open the logs, 99.9% uptime carried across enterprise accounts.<br>
At USC through May 2027 for AI/ML and distributed systems, which in practice<br>
means retrieval pipelines fast enough that nobody notices them.

<img src="./hd-stack.svg" width="620" alt="stack"/>

<samp>python &nbsp; typescript &nbsp; javascript &nbsp; java &nbsp; c++ &nbsp; sql</samp><br>
<samp>fastapi &nbsp; node &nbsp; spring boot &nbsp; django &nbsp; grpc &nbsp; graphql</samp><br>
<samp>postgres &nbsp; redis &nbsp; kafka &nbsp; dynamodb &nbsp; supabase</samp><br>
<samp>aws &nbsp; gcp &nbsp; kubernetes &nbsp; docker &nbsp; terraform</samp><br>
<samp>tensorflow &nbsp; langchain &nbsp; rag &nbsp; vector search &nbsp; opencv</samp>

<img src="./hd-projects.svg" width="620" alt="projects"/>

**[DaySays](https://github.com/HitenRohra/DaySays)** &nbsp;·&nbsp; <samp>typescript, rag</samp><br>
AI journaling app. A retrieval pipeline held to a sub-100ms p99, which is most<br>
of why 7-day retention moved 30%. First place at TechWeek, out of 40+ teams.

**[AI_Interview](https://github.com/HitenRohra/AI_Interview)** &nbsp;·&nbsp; <samp>python, rag</samp><br>
Automated screening: reads the résumé, asks questions that follow from it,<br>
scores the answers. 35% better answer precision and 60% fewer hallucinations<br>
than the first cut, with latency taken from 4.2s down to 1.1s.

**[AnomalyDetector](https://github.com/HitenRohra/AnomalyDetector)** &nbsp;·&nbsp; <samp>python, opencv</samp><br>
Spots explosions, accidents and theft in video footage. 90%+ accuracy at<br>
24 FPS on 45% less compute, which is what made it deployable at the edge.<br>
Published at IRCICD'23.

**[AI_Coding_Assistant](https://github.com/HitenRohra/AI_Coding_Assistant)** &nbsp;·&nbsp; <samp>python</samp><br>
A Cursor-shaped coding assistant that never leaves the terminal.

<img src="./hd-stats.svg" width="620" alt="stats"/>

<div align="center">

<img src="./streak.svg" width="620" alt="Current and longest streak"/>

<img src="./langs.svg" width="620" alt="Top languages by bytes and by repo"/>

<img src="./year.svg" width="620" alt="The last year, one character per day"/>

</div>

<img src="./hd-colophon.svg" width="620" alt="colophon"/>

Nothing on this page loads from anyone else's server. `ascii.svg` is a photo<br>
pushed through a 13-character ramp by<br>
[`scripts/make_portrait.py`](scripts/make_portrait.py); the stat graphics and<br>
these section headings are drawn straight from the GitHub GraphQL API by<br>
[a scheduled action](.github/workflows/stats.yml), once a day, committing only<br>
the files that actually changed.

Everything animates with SMIL from inside the SVG, because GitHub strips<br>
`<script>` from READMEs. The headings are images for the same reason — GitHub<br>
also strips CSS, so an image is the only way to put this page's own typeface<br>
on a heading. Since no third party is involved, nothing here can rate-limit,<br>
break, or quietly go dark.

The face is [JetBrains Mono](scripts/fonts), subset to just the characters<br>
each graphic draws and inlined as base64 — about 12 KB across the page rather<br>
than 4.5 MB. That isn't only for looks: the portrait's grid assumes an advance<br>
width of exactly 0.600 em, and a viewer whose default monospace is narrower<br>
would otherwise see the whole thing squeezed.

Language totals cover public repositories only, so the numbers don't depend on<br>
whose token ran the script. `year.svg` reuses the portrait's own ramp —<br>
`:` `+` `#` `@`, quiet to loud.

<sub>Built by following <a href="https://agreeable-credit-859.notion.site/A-GitHub-profile-that-generates-itself-3abedfe9a65a81e4afc9daed90cb4e7e">A GitHub profile that generates itself</a> by <a href="https://github.com/andriidrok1">Andrii Drok</a>.</sub>
