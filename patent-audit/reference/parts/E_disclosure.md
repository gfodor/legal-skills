# Part E — Specification — disclosure sufficiency

27 items (8 Fatal).

Grounded in 35 U.S.C. § 112; 37 CFR 1.71–1.77, 1.821; MPEP 608, 2161–2173.

## Enablement and full disclosure

### `E01` Verify the specification enables a skilled artisan to make and use the invention
- **Check:** Confirm the specification describes the invention in full, clear, concise, and exact terms sufficient for a person of ordinary skill in the field to build and use a working version without undue experimentation.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Read the detailed description as a skilled artisan trying to build the thing. Functional narration and marketing benefits without construction, connection, or operating sequence fail. "In a conventional manner" standing in for the novel portion is a red flag. If you supply missing engineering from your own head, the draft fails.
- **Why it matters:** Incomplete disclosure is a § 112(a) rejection of the entire application. New matter cannot be added later. A patent that issues anyway can be invalidated when asserted.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 2164; *Wands* factors.

### `E02` Verify critical dimensions, materials, and values are disclosed
- **Check:** Confirm that any dimension, material, or component value that is critical to performance or at all unusual is stated in the specification.
- **Severity:** Fatal
- **Applies to:** all applications (especially chemical, electrical, mechanical)
- **What to look for:** Routine off-the-shelf values may be omitted. Hunt for parameters the invention actually depends on: a tolerance, temperature, ratio, timing, or concentration called important but never given. Details in the specification do not narrow claim scope; claims do. Where in doubt, include the number.
- **Why it matters:** Missing critical parameters are non-enablement and cannot be added after filing.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 2164.01.

### `E03` Verify uncommon materials identify a source or how to make them
- **Check:** Confirm that every uncommon material, component, or manufacturing step is accompanied by a supplier identification or a reference explaining how to obtain or perform it.
- **Severity:** Serious
- **Applies to:** all applications (especially chemical and process inventions)
- **What to look for:** Specialty reagents, alloys, coatings, or process steps ("anneal," "deposit") with no equipment, conditions, or source. A named product plus manufacturer is stronger than a bare website mention.
- **Why it matters:** Without a route to the special component, a skilled artisan cannot practice the invention.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 2164.01(b).

### `E04` Verify trademarked ingredients are also described generically
- **Check:** Confirm that any component identified only by a trademark is also described by its composition or a generic name plus manufacturer, and that the invention does not depend on the trademark alone.
- **Severity:** Serious
- **Applies to:** chemical | all applications using proprietary materials
- **What to look for:** Brand names, ® and ™. Ask whether the specification would still teach the invention if that product were reformulated or discontinued. Give composition or a generic chemical name; offer the brand as a preference.
- **Why it matters:** What a trademark denotes can change. Reliance on the mark alone can destroy enablement and narrow scope to that product.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 608.01(v), 2163–2164.

### `E05` Verify components that do not yet exist are fully designed, described, and drawn
- **Check:** Confirm that every element the invention requires but which cannot be purchased off the shelf is itself designed out in the specification and shown in the drawings.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Compound nouns invented by the drafter and recited as if standard, with no figure and no structure. Functional blocks labeled with the invention's own novel function. Treat each such component as a sub-invention.
- **Why it matters:** A missing novel element is a classic § 112(a) failure and cannot be cured after filing.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 2164, 2181.

### `E06` Verify the disclosure is complete because nothing can be added after filing
- **Check:** Confirm the draft contains every technical detail and ramification the inventor currently knows.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** TODO markers, "details to follow," placeholder figures, a parts list longer than the described parts, or variants deliberately held back. Holding back is not strategic here.
- **Why it matters:** 35 U.S.C. § 132 forbids new matter. An incomplete disclosure is usually unrepairable.
- **Primary source:** 35 U.S.C. §§ 112(a), 132; MPEP 608.04, 2163.06.

### `E07` Verify deposit and sequence-listing obligations for biological subject matter
- **Check:** Confirm that any not-widely-available biological material is deposited in an approved depository and that nucleotide or amino acid sequences are provided as a compliant sequence listing.
- **Severity:** Fatal
- **Applies to:** chemical | biotechnology
- **What to look for:** Named strains, cell lines, plasmids, seeds, and sequence data. If a skilled artisan cannot obtain the material, a deposit and a specification reference are required. Sequence listings must satisfy 37 CFR 1.821–1.825 (ST.26 for current filings).
- **Why it matters:** Without the deposit the disclosure is not enabling. Noncompliant listings block examination.
- **Primary source:** 37 CFR 1.801–1.809, 1.821–1.825; MPEP 2400.

## Written description, drawings, and claim support

### `E08` Verify every claim element appears in a figure and in the description
- **Check:** Walk each claim element by element and confirm each recited element is both shown in a drawing figure and described in the specification text.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A two-column table: claim term versus figure and paragraph. Terminology drift ("retaining member" in the claim, "clip" in the spec). Late-added dependent limitations are the most commonly unsupported.
- **Why it matters:** Unsupported elements draw written-description and antecedent-basis rejections. Support cannot be added later.
- **Primary source:** 35 U.S.C. § 112(a)–(b); 37 CFR 1.83; MPEP 2163, 2173.05(e).

### `E09` Verify alternative embodiments are disclosed
- **Check:** Confirm the specification describes alternative materials, sizes, shapes, uses, process variations, and additional embodiments rather than a single implementation.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Exactly one embodiment, one material list, and one use case. Process claims with a fixed step order and no statement that steps are optional or reorderable. Thin variants leave nothing to fall back on if the main embodiment is knocked out, and let a competitor patent the unclaimed variant.
- **Why it matters:** Courts read claims in light of the disclosed embodiments. A single embodiment invites a narrow construction.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 2163, 2164.01(a); *Phillips v. AWH*.

### `E10` Verify a flowchart is provided for every process aspect
- **Check:** Confirm that computer, chemical, or mechanical processes are shown as a flowchart with each separate step in its own labeled block, in addition to the narrative description.
- **Severity:** Serious
- **Applies to:** software/business method | chemical | mechanical process
- **What to look for:** Method claims with no corresponding figure. Blocks that are too coarse. The flowchart should map onto the method steps and the operation narrative.
- **Why it matters:** The Office commonly requires a flowchart for process inventions. An under-detailed chart is the usual vehicle for a non-enablement attack on software and process claims.
- **Primary source:** 37 CFR 1.83; MPEP 608.02; 35 U.S.C. § 112(a).

### `E11` Verify block diagrams explain every nonconventional block
- **Check:** Confirm that each block in a block diagram is either a standard, conventional part or is backed by a schematic, a clear explanation, or a literature reference.
- **Severity:** Serious
- **Applies to:** mechanical | electrical/electronic | software/business method
- **What to look for:** A box labeled with the invention's novel function and no schematic behind it. A programmed processor with no algorithm, listing, or software flowchart. Pair every nonconventional box with a detail figure or a cited publication.
- **Why it matters:** A functional black box in place of the novel element is incomplete disclosure, and computer-implemented blocks lack the algorithm § 112(f) needs.
- **Primary source:** 35 U.S.C. § 112(a), (f); MPEP 2181, 2161.01.

### `E12` Verify drawing formalities: prior-art labeling, separate filing, every novel feature shown
- **Check:** Confirm any prior-art figure is labeled "Prior Art" and described in the Background, the drawings are a separate document from the specification, and enough views exist to show every novel feature.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Unlabeled prior-art figures, drawings bound into the specification text, and claimed features with no view. Formal defects (blurred lines, missing sheet numbers) produce an OPAP notice.
- **Why it matters:** An unlabeled prior-art figure misrepresents the contribution. Missing views leave claimed features unsupported.
- **Primary source:** 37 CFR 1.83–1.84; MPEP 608.02.

## Best mode and embodiments

### `E13` Verify no embodiment is singled out as "best" or "preferred"
- **Check:** Confirm the draft discloses all known modes fully but nowhere designates one as the best mode or the preferred embodiment.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Best mode," "preferred," "preferably," "optimal." Alternatives mentioned in one sentence while another embodiment gets ten pages. Treat every embodiment even-handedly.
- **Why it matters:** Best-mode invalidity is gone, but identifying a preferred embodiment can be used to limit claim construction.
- **Primary source:** 35 U.S.C. § 112(a); 35 U.S.C. § 282(b)(3)(A); *Phillips* claim-construction practice.

## Definiteness and clarity

### `E14` Verify the description is clear, precise, and free of ambiguity
- **Check:** Confirm the specification is written in short, clear sentences with no vague, ambiguous, or unintelligible passages, and that terminology is used consistently.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Pronouns with unclear antecedents, a part called by two names, "connected to" where the mechanism matters. Inconsistent numerals. Grammar that a judge will have to guess at.
- **Why it matters:** Unclear disclosure is construed narrowly. Claims can be rejected for imprecise language, and sloppiness invites attack.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173; *Nautilus v. Biosig*.

## Statements that could narrow or invalidate the patent

### `E15` Verify the draft contains no self-limiting statements
- **Check:** Confirm the application contains no statement a court could use to limit the claims — no "objects," no "the invention is," no essentiality statements, no unearned advantages.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "The present invention," "essential," "must," "critical," "the novelty lies in." Replace invention-level assertions with embodiment-level ones. Keep the summary and abstract broad.
- **Why it matters:** Courts read such statements as disclaimers and construe the claims down to them.
- **Primary source:** *Phillips*; *SciMed Life Sys.*; MPEP 2111.01.

### `E16` Verify no negative, restrictive, or hedged operability statements are present
- **Check:** Confirm the draft never says a novel part resembles something known, that novelty resides solely in one part, that something "might" work, or that anything is always better, necessary, or not done a certain way.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Might," "is believed to," "similar to conventional X," "the device is not constructed with…" State facts affirmatively.
- **Why it matters:** Adversaries use hedges as admissions of inoperability and use comparisons as admitted prior art.
- **Primary source:** 37 CFR 1.56; claim-construction and disclaimer doctrine; MPEP 2129 (admissions).

### `E17` Verify the Background contains no inventive concepts
- **Check:** Confirm the Background section discusses only known problems and genuine prior art, with none of the applicant's own inventive concepts described there.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** If a hostile examiner treated everything in the Background as admitted prior art, what would be lost? "It would be desirable to" followed by the inventive step is the usual leak.
- **Why it matters:** Inventive concepts placed in the Background may be treated as admitted prior art.
- **Primary source:** MPEP 608.01(c), 2129.

### `E18` Verify advantages are factual, verified against the art, and tied to embodiments
- **Check:** Confirm every advantage asserted is a real advantage over the prior art, is exhibited by at least one disclosed embodiment, and is framed as an advantage of embodiments rather than of "the invention."
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Superlatives with no basis; "first to solve" claims a search does not support; advantages only the unclaimed commercial product delivers. Attach advantages to embodiments, not to the invention as a whole.
- **Why it matters:** Mischaracterized art draws Office scrutiny. Advantages attributed to "the invention" become de facto claim limitations.
- **Primary source:** 37 CFR 1.56; MPEP 608.01(a), 2129; *Phillips*.

## Software and computer-related inventions

### `E19` Verify a program listing or an adequately detailed flowchart is included
- **Check:** Confirm any software, firmware, or microprocessor-based invention discloses either a source/object listing or a flowchart detailed enough for an ordinarily skilled programmer to write and debug the program.
- **Severity:** Fatal
- **Applies to:** software/business method
- **What to look for:** Narrative alone is not enough. Apply the building-plans test: would an ordinary programmer have to invent design decisions? Blocks phrased as goals ("determine best route") fail. Length of routine effort is acceptable; required creativity is not.
- **Why it matters:** Computer-implemented inventions are examined strictly for enablement and, under § 112(f), for a disclosed algorithm.
- **Primary source:** 35 U.S.C. § 112(a), (f); MPEP 2161.01, 2181; *Aristocrat*; *WMS Gaming*.

### `E20` Verify the specification ties the process to hardware for eligibility
- **Check:** Confirm the specification describes the machine or apparatus and the relationship between the claimed process and that hardware.
- **Severity:** Fatal
- **Applies to:** software/business method
- **What to look for:** Method claims that are only business steps between unnamed parties. No CPU, memory, sensor, or interface described. The specification must supply the technological practical application the claims will need under *Alice* / MPEP 2106.
- **Why it matters:** Eligibility support has to exist at filing. The specification cannot later be amended to add it.
- **Primary source:** 35 U.S.C. § 101; *Alice*; MPEP 2106.05(b).

### `E21` Verify implementation instructions for the program are in the specification
- **Check:** Confirm the specification explains how to implement the listing — language, target processor, how the program controls the machine, and the input/output hardware.
- **Severity:** Serious
- **Applies to:** software/business method
- **What to look for:** A listing dropped in without explanatory text. Unnamed language, unnamed machine, unnamed peripherals. A programmer with the listing and the specification alone should be able to bring the system up without undue experimentation.
- **Why it matters:** Undue experimentation to implement the disclosed program is non-enablement.
- **Primary source:** 35 U.S.C. § 112(a); MPEP 2164.06(c), 2161.01.

### `E22` Verify the disclosed program works and is submitted in the required format
- **Check:** Confirm any included program listing is free of serious bugs and complies with the PTO's submission format rules for its length and filing route.
- **Severity:** Serious
- **Applies to:** software/business method
- **What to look for:** Has the listing been run against the behavior the specification claims? Check current 37 CFR 1.96 for listing placement and format (ASCII for electronic filing). Consider whether a detailed flowchart is preferable to publishing source.
- **Why it matters:** A nonfunctional listing undermines enablement. Format noncompliance produces formal objections.
- **Primary source:** 37 CFR 1.96; MPEP 608.05.

## Specification structure and formal papers

### `E23` Verify the specification follows Rule 77 section order and headings
- **Check:** Confirm the specification's sections appear in the PTO's prescribed order with capitalized headings, and that inapplicable sections are either omitted or marked "not applicable."
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Title; Cross-Reference; Federally Sponsored Research; Sequence Listing or Program; Background; Summary; Brief Description of Drawings; Detailed Description; Claims; Abstract. Claims begin on a new page. Do not include data the Office adds at printing (references cited, field of search).
- **Why it matters:** Deviations draw informality objections. A missing Cross-Reference can forfeit a benefit claim.
- **Primary source:** 37 CFR 1.77; MPEP 608.01(a).

### `E24` Verify the title, Summary, and Abstract meet content and length limits
- **Check:** Confirm the title is meaningful and within 500 characters, the Summary paraphrases the claimed embodiments, and the Abstract is 150 words or less and summarizes the technical content.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Count abstract words. A title that is a bare category, or that is narrower than the embodiments. A summary that tracks only claim 1 or recites "objects of the invention."
- **Why it matters:** Over-length abstracts and empty titles draw objections. Over-specific summary/abstract text hands a court limiting language.
- **Primary source:** 37 CFR 1.72, 1.73; MPEP 608.01(b), (d).

### `E25` Verify the Conclusion includes a broadening paragraph
- **Check:** Confirm the specification ends with a conclusion that restates advantages, describes alternative forms and uses, and adds an express statement that scope is determined by the claims.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Drafts that stop after the last embodiment. A sentence telling a later reader the illustrated forms are not limiting.
- **Why it matters:** Without a broadening close, courts are more likely to read the claims onto the particular embodiments shown.
- **Primary source:** *Phillips*; MPEP 608.01(d).

### `E26` Verify the filing packet is complete and signed
- **Check:** Confirm all required formal papers accompany the specification — transmittal or EFS equivalents, fee payment, signed declaration, ADS, IDS, drawings, and an NPR if applicable.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Inventory against 37 CFR 1.51. Unsigned declaration; IDS without required copies; NPR despite planned foreign filing; no ADS on an electronic filing.
- **Why it matters:** An incomplete packet draws a Notice to File Missing Parts. A defective IDS implicates the duty of candor.
- **Primary source:** 37 CFR 1.51, 1.63, 1.76, 1.97–1.98; MPEP 601.

### `E27` Verify the application does not combine unrelated inventions or inventors
- **Check:** Confirm that any multiple inventions covered in the one application are genuinely related and share the same inventive entity.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Independent claims aimed at separate products that merely appear together. Inventors who contributed to only one claimed subject. Restriction is still possible even for related inventions; each divisional carries its own fees and still expires 20 years from the original date.
- **Why it matters:** Unrelated inventions or different inventive entities invite restriction, extra fees, and inventorship defects.
- **Primary source:** 35 U.S.C. §§ 116, 121; 37 CFR 1.141–1.146; MPEP 803.
