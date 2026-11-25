---
title: "Evolution's Answer Key: Grading Sequencers with Primate Genes"
tags:
  - primate genomics
  - sequencing error
  - benchmarking
  - miniprot
  - reproducibility
author: Gabriel Renaud
member: gabriel-renaud
---

*A lost hard drive, a forgotten project, and a simple idea: where evolution refuses to change a protein, every mismatch a sequencer reports is the sequencer's own mistake.*

---

## A Ruler Made of Conserved Proteins

Every sequencing machine attaches a quality score to every base it reads. A "Q30" base is supposed to be wrong one time in a thousand, a "Q20" base one time in a hundred. But how far should you trust those promises? To find out, you need places in the genome where you already know the right answer.

Pablo Sánchez-Izquierdo Besora, then a student in our group, had a neat way to find such places: ask the primates. If a human protein is letter-for-letter identical in the chimpanzee, bonobo, gorilla, orangutan, gibbon, four Old World monkeys and a tarsier, then evolution has been policing that sequence for tens of millions of years. When we sequence a human at those positions, a mismatch against the reference is much more likely to be the machine's mistake than a real mutation. Count the mismatches at each reported quality and you get a calibration curve for the sequencer, without needing a variant truth set.

He ran the analysis and made the plots, and then the drive they lived on was lost. The scripts and the output tables survived; the figures did not. So we rebuilt them, and the rebuild turned out to be more interesting than a simple redraw.

---

## Step 1: Ask Ten Primate Genomes

The first ingredient is [miniprot](https://github.com/lh3/miniprot), which aligns protein sequences directly to genomes. It lets us ask, for every human protein: is it present in the chimpanzee genome, and how many amino acids differ? Pablo ran this for all 122,676 human protein records in Ensembl (every isoform) against ten primate assemblies.

{% include figure.html
  image="images/posts/primate-conserved-exons/primate-conservation.png"
  link="images/posts/primate-conserved-exons/primate-conservation.pdf"
  width="100%"
  caption="**Figure 1. Conservation of the human proteome across ten primate genomes.** **a**, share of human proteins with an alignment, for any coverage and for alignments covering at least 90 %, 95 % or 100 % of the protein. **b**, amino-acid divergence of the aligned proteins. **c**, in how many of the ten species a protein is identical over its full length; the blue bar marks the 1,919 proteins that are identical in all ten. **d**, alignment yield against assembly size. Click for the vector PDF."
%}

Almost everything aligns: 99.3 % of human proteins have an alignment in the chimpanzee genome and 94.7 % in the tarsier, the most distant relative in the set. Divergence climbs the way the family tree says it should.

The interesting part is panel c. If we insist that the alignment covers the whole protein with zero differences, 85,711 proteins (70 %) are not identical in *any* of the ten species. Yet 1,919 proteins (1.6 %) are letter-for-letter identical in all ten. That club reads like a greatest-hits list of cell biology: histones H3.3 and H4, calmodulin, ubiquitin, PCNA, the GTPase RAN and the tumour suppressor PTEN.

---

## Step 2: From Proteins to Base Pairs

A protein is not a position in the genome, so the next step is to turn the club into coordinates. For 1,439 of the 1,919 proteins Pablo had exon coordinates in the GRCh37 reference build, which is the build of the HG002 alignments (the other 480 are absent from Ensembl's GRCh37 annotation). Those proteins have 7,071 exons, which merge into 3,983 intervals covering 889 kb, about 0.03 % of the genome. We call this the "no-mutation zone".

{% include figure.html
  image="images/posts/primate-conserved-exons/region-funnel.png"
  link="images/posts/primate-conserved-exons/region-funnel.pdf"
  width="100%"
  caption="**Figure 2. Building the no-mutation zone.** Bars are drawn to scale. The last card shows what is inside the 889 kb; we come back to it below. Click for the vector PDF."
%}

Hold on to that last card. It will matter.

---

## Step 3: What a Sequencing Error Looks Like

Before any statistics, it helps to see the raw material. Here are real reads from the BGISEQ-500 run of HG002 piled up over two of these exons, one from the ubiquitin gene *UBB* and one from the GTPase *RAN*. Every grey bar is a read, every coloured tick is a place where the read disagrees with the reference, and the colour tells you how confident the machine claimed to be.

{% include figure.html
  image="images/posts/primate-conserved-exons/exon-pileup.png"
  link="images/posts/primate-conserved-exons/exon-pileup.pdf"
  width="100%"
  caption="**Figure 3. Mismatches in two conserved exons.** BGISEQ-500 reads (HG002) over one exon of UBB (181 reads) and one of RAN (386 reads), coloured by reported base quality. The two exons were chosen to illustrate the idea, not at random. Click for the vector PDF."
%}

In *UBB*, 47 of the 48 mismatches are low-quality calls (below Q20), and none reaches Q30. In *RAN* it is the same story, with one exception: a perfectly vertical stripe, where 19 of the 46 reads show the same C→T change at the same position. That is not noise. It is most likely a heterozygous variant in HG002, a genuine difference between this person and the reference, and our method would happily count it as a sequencing error. Set that column aside, and the other 103 mismatches in the exon include 99 below Q20 and none at Q30 or above.

The picture contains the whole idea in miniature: sequencing errors are scattered and mostly low-quality, while real variants line up.

---

## Step 4: Grading Five Sequencers

Pablo repeated this over the 889 kb for HG002 data from five technologies: Illumina 2×150 and 2×250, BGISEQ-500, BGI stLFR and Oxford Nanopore ultra-long reads. For each reported quality he counted how often the base disagreed with the reference. If a machine is honest, a Q30 base should disagree about once in a thousand.

{% include figure.html
  image="images/posts/primate-conserved-exons/sequencer-calibration.png"
  link="images/posts/primate-conserved-exons/sequencer-calibration.pdf"
  width="100%"
  caption="**Figure 4. Reported versus empirical base quality.** **a**, measured quality, −10 log₁₀ of the mismatch rate, against the quality the machine reported; the table gives the base-weighted RMSE between the two. **b**, how many bases carry each reported quality. **c**, mismatch rate over all bases (filled) and over bases of at least Q30 (open); the number at the right is the share of bases at or above Q30. Counts are the original ones from Pablo's scripts. Click for the vector PDF."
%}

Three things stand out.

**Illumina 2×150 and BGISEQ-500 are close to honest.** Up to about Q28 their curves sit slightly *above* the diagonal, meaning the data are a little cleaner than the score claims. Above Q30 the curves flatten at a measured quality of about 33.

**A single number for calibration.** To summarise a curve we use the base-weighted root-mean-square error: how far, in Phred units, the reported quality of a typical base is from its measured quality, with each quality level weighted by how many bases carry it. It is 3.4 for BGISEQ-500, 3.5 for Illumina 2×150, 5.2 for stLFR, 7.3 for Illumina 2×250 and 10.1 for Nanopore. As a rule of thumb, three Phred units is a factor of two in error rate.

**Nanopore's scores say little about its errors in this dataset.** Measured quality climbs only from 13 to 18 while the reported quality goes from 1 to 40. This is a 2019-era basecaller (Guppy 3.2.4) on ultra-long reads, so it is not a verdict on the technology today, and the analysis counts substitutions only, whereas Nanopore errors are typically dominated by insertions and deletions.

Both Illumina 2×250 and Nanopore come from incomplete runs (12 and 10 of 20 chunks of the interval list), so we would treat those two with extra caution.

### Does Filtering Help?

The same counts answer a practical question: what do you gain by throwing away low-quality bases?

{% include figure.html
  image="images/posts/primate-conserved-exons/quality-filtering.png"
  link="images/posts/primate-conserved-exons/quality-filtering.pdf"
  width="100%"
  caption="**Figure 5. What a quality filter buys.** **a**, fraction of bases kept as the minimum reported quality rises. **b**, mismatch rate of the bases that are kept. **c**, share of all bases (open) and of all mismatches (filled) that lie below Q30. Markers in a and b are Q10, Q20 and Q30. Click for the vector PDF."
%}

In all four short-read datasets, the 9–16 % of bases below Q30 carry 81–87 % of the mismatches. A Q30 filter is a bargain there. For Nanopore the same filter removes 76 % of the bases to get rid of 84 % of the mismatches, and what is left is still wrong about 1.7 % of the time.

---

## The Plot Twist: Auditing the Audit

When you rebuild an analysis from scratch you re-derive every number, and a few of them did not survive. We want to be clear that Pablo's work did the heavy lifting, from aligning ten genomes to pulling five technologies through the same pipeline. What follows is the kind of thing that only shows up when someone re-computes everything, which is a good argument for keeping code, data and figures together.

**1. Bases were counted about 91 times too often.** The counting script re-scored an entire read at every position the read covered, so for BGISEQ-500 it tallied 3.2 billion bases for the 35 million that actually lie inside the intervals, and sequence flanking the exons crept into the counts. We recounted that dataset base by base. The shape of the curves is unchanged, but the original error rates are 5–32 % too high, and the BGISEQ-500 RMSE drops from 3.4 to 2.7. (BGISEQ-500 is the only dataset still on disk; the others stream from public servers.)

<details>
<summary><strong>Supplementary figure: original counting versus recount</strong></summary>

{% include figure.html
  image="images/posts/primate-conserved-exons/counting-validation.png"
  link="images/posts/primate-conserved-exons/counting-validation.pdf"
  width="100%"
  caption="**Supplementary Figure 1.** BGISEQ-500 with the original counting and with a per-base recount over the same intervals. **a**, calibration with weighted RMSE. **b**, ratio of the two mismatch rates. **c**, bases counted versus bases that exist in the target intervals."
%}

</details>

**2. The "no-mutation zone" is mostly not coding sequence.** This is the last card of Figure 2. The intervals are whole exons, and exons include their untranslated regions (UTRs). Knowing that a *protein* is identical in ten primates says nothing about its UTRs. Of the 889 kb, only 252 kb (28 %) is protein-coding; 637 kb (72 %) is UTR. When we split the BGISEQ-500 recount into the two parts, the picture changes.

{% include figure.html
  image="images/posts/primate-conserved-exons/coding-vs-utr.png"
  link="images/posts/primate-conserved-exons/coding-vs-utr.pdf"
  width="100%"
  caption="**Figure 6. The plateau comes largely from the UTRs.** BGISEQ-500, per-base recount, inside the coding part and the UTR part of the interval set. **a**, measured versus reported quality with the weighted RMSE. **b**, reported minus measured quality; positive values mean the machine is over-confident. Click for the vector PDF."
%}

Below about Q28 the two parts agree. Above it they part ways: in coding sequence the mismatch rate at Q30 and above is 0.024 %, in UTR it is 0.052 %, and the RMSE falls from 3.3 to 1.5. Pooled over reported Q36–38, the measured quality is 36.8 in coding sequence, almost exactly what the machine claims, against 33.2 in UTRs. So the flat plateau in Figure 4 is not a speed limit of the sequencer. It is, to a large extent, a property of the regions. We do not yet know how much of the UTR excess is real human variation, which UTRs tolerate, and how much is sequence that is harder to map; the next step is to separate the two.

**3. Some data are missing.** The Nanopore and Illumina 2×250 runs are partial, the PacBio run produced only zeros and is not shown, and we give no confidence intervals because the counts are not independent. The numbers for the technologies other than BGISEQ-500 are therefore best read as a first sketch.

---

## What We Take From This

- **The idea works.** Primate-conserved coding sequence gives clean, smooth calibration curves, and in the one dataset we could redo carefully, the sequencer's quality scores are honest to within about a Phred unit or two.
- **Define "conserved" carefully.** Protein identity constrains coding sequence, not the UTRs that come with the exons. Restricting to coding sequence was the largest improvement we measured.
- **Real variants are the enemy of this method.** The vertical stripe in Figure 3 would be removed by masking the GIAB truth-set variants, which is not yet done.
- **Keep the figures with the code.** A project whose plots cannot be regenerated cannot be audited, and a lot of what we found above was only visible because we rebuilt it.

## Where This Could Go

- Redo all five technologies on the coding-only intervals. The GIAB alignments are public, so this is mostly compute.
- Mask HG002 truth-set variants and add confidence intervals by resampling whole exons.
- Add PacBio HiFi and current Nanopore chemistry, and use the interval set to grade new instruments as they appear.

If you have data that deserves a grade, get in touch.

---

## Methods in Brief

Human protein sequences (Ensembl, GRCh38) were aligned to ten primate assemblies with miniprot, requiring 100 % protein coverage for the conserved set. The merged exon coordinates (GRCh37) were intersected with HG002 sequencing data from Genome in a Bottle, aligned to hs37d5. For each aligned base, a mismatch is a difference from the reference (substitutions only), and counts were tallied by reported base quality. The weighted RMSE is √(Σ w<sub>q</sub> (Q<sub>q</sub> − Q̂<sub>q</sub>)²), where Q<sub>q</sub> is the reported quality, Q̂<sub>q</sub> = −10 log₁₀(mismatches / bases) is the measured quality at that level, and w<sub>q</sub> is the share of bases carrying quality q. The coding/UTR split uses the Ensembl GRCh37.87 annotation. Figures 4 and 5 use the original counts from Pablo's scripts, Figure 6 and the supplementary figure use the per-base recount of the BGISEQ-500 alignment, and Figure 3 shows individual reads.

Vector PDFs of all figures can be reached by clicking on them, and the numbers behind every panel are in a single [source-data archive]({{ "images/posts/primate-conserved-exons/source-data.zip" | relative_url }}).

## Credits

**The project is Pablo Sánchez-Izquierdo Besora's.** He designed and ran the analysis: the miniprot alignments of the human proteome to ten primate genomes, the conserved-region set, and the error-rate analysis of five sequencing technologies on Genome in a Bottle data. Everything in this post rests on that work.

**The figures were made by Claude** (Anthropic's AI model, working in Claude Code). It rebuilt them from the scripts and output tables that survived, drew the figures that were lost, designed the additional ones, and recomputed the numbers quoted here, including the audit.

---

## References

Li H. (2023). Protein-to-genome alignment with miniprot. *Bioinformatics* 39(1): btad014. <https://doi.org/10.1093/bioinformatics/btad014>

Zook JM, Catoe D, McDaniel J, et al. (2016). Extensive sequencing of seven human genomes to characterize benchmark reference materials. *Scientific Data* 3: 160025. <https://doi.org/10.1038/sdata.2016.25>
