# Part A — Threshold: is this patentable at all?

37 items (18 Fatal).

Guidance in this part is grounded in 35 U.S.C. §§ 100–103, 37 CFR Part 1, the current MPEP, and controlling Supreme Court / Federal Circuit eligibility and obviousness doctrine. Re-verify every cite against the official text in force on the planned filing date.

## Statutory class and judicial exceptions (§101)

### `A01` Confirm the invention lands in a statutory class
- **Check:** Verify the draft's claimed subject matter can be reasonably classified as a process/method (including a new use), machine, article of manufacture, or composition of matter.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Read the independent claims, not the marketing language in the summary. Map each independent claim to a category in 35 U.S.C. § 101. A claim that recites only a result, a goal, or a desired economic outcome with no process steps or no physical thing is the failure mode. The applicant need not pick a single class; at least one independent claim must unambiguously be a process, machine, manufacture, or composition.
- **Why it matters:** Subject matter outside § 101 is rejected as non-statutory. Later amendment cannot create a statutory class the disclosure does not support.
- **Primary source:** 35 U.S.C. § 101; MPEP 2106.

### `A02` Screen the claims against the judicial exceptions
- **Check:** Verify no independent claim, read as a whole, amounts to a law of nature, a natural phenomenon, or an abstract idea.
- **Severity:** Fatal
- **Applies to:** all applications; especially software, business method, diagnostic, chemical/biotech
- **What to look for:** Apply the current USPTO Step 2A framework (MPEP 2106). Strip conventional extra-solution activity and ask what remains. Tells include preambles like "a method of determining," bodies made only of receiving / calculating / outputting, and specifications that describe the advance solely as an algorithm, correlation, or economic practice. A passing draft ties the claimed advance to a concrete technological improvement and recites that improvement in the claim.
- **Why it matters:** Claims directed to a judicial exception without significantly more are ineligible under § 101 and are routinely invalidated after grant.
- **Primary source:** 35 U.S.C. § 101; *Alice Corp. v. CLS Bank*; *Mayo v. Prometheus*; MPEP 2106; current USPTO subject-matter-eligibility guidance.

### `A03` Software: verify the draft shows a technological improvement, not generic computerization
- **Check:** Verify the specification and claims identify a technological problem in the computer or network that the software solves, rather than a conventional computerized implementation of a known task.
- **Severity:** Fatal
- **Applies to:** software / Internet / business method
- **What to look for:** Ask whether the claimed advance improves how a computer or network functions (memory handling, security, routing, rendering, resource allocation) or merely uses a general-purpose processor as a tool for an otherwise abstract task. Failure modes: an offline method with "implemented on a computer" tacked on; advantages limited to speed or cost of a conventional calculation; no description of a technical constraint that was overcome.
- **Why it matters:** Under *Alice* and MPEP 2106.05, generic computer implementation of an abstract idea is not eligible. The eligibility story must exist at filing.
- **Primary source:** 35 U.S.C. § 101; *Alice*; MPEP 2106.04–2106.05.

### `A04` Make the claims recite the unconventional nature of the process or machine
- **Check:** Verify that where eligibility rests on unconventionality (special-purpose or embedded computer, non-conventional process rules), the *claims* — not just the specification — call that unconventionality out.
- **Severity:** Serious
- **Applies to:** software / business method / computer-implemented
- **What to look for:** Compare the eligibility narrative in the specification with the claim language. A specification that describes a special-purpose device or an unconventional ordered combination, while the claims recite only "a processor and a memory," will be examined as a generic computer. Recite the particular machine, the unconventional steps, or the specific data/control arrangement that is the inventive concept.
- **Why it matters:** Eligibility is judged on the claim as written. Unclaimed technical detail does not supply "significantly more."
- **Primary source:** 35 U.S.C. § 101; MPEP 2106.05(a)–(b); *Enfish*; *Bascom*.

### `A05` Business methods: frame a technological problem, not an economic practice
- **Check:** Verify a business-derived invention is framed in terms of technological hurdles overcome, not as a fundamental economic practice or a method of organizing human activity.
- **Severity:** Serious
- **Applies to:** business method / fintech / marketplace software
- **What to look for:** Scan the background and summary for hedging, insurance, payment processing, advertising, contract compliance, or marketplace matching as the stated invention. If the problem and solution are both business rules, the draft is in the routinely rejected zone. A passing draft identifies a concrete technical obstacle (latency, integrity, authorization, data consistency) and organizes the claims around that obstacle.
- **Why it matters:** Methods of organizing human activity are a named abstract-idea grouping. Mis-framed claims fail Step 2A regardless of novelty.
- **Primary source:** 35 U.S.C. § 101; MPEP 2106.04(a)(2); *Bilski v. Kappos*; *Alice*.

### `A06` Rule out classic non-statutory categories
- **Check:** Verify the claimed subject matter is not a purely mental process, printed matter without an instrumentality, a naturally occurring thing, an idea per se, a bare algorithm, or a transitory signal.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Mental processes: could every step be performed in the human mind? Printed matter: is novelty carried only by text or symbols with no functional relationship to a substrate? Signals: any claim to a carrier wave or transitory transmission. Ideas per se: no tangible process or product. A passing draft claims a manufacture, machine, composition, or a process that cannot be performed entirely mentally.
- **Why it matters:** These categories are treated as outside § 101 or as judicial exceptions. A sole independent claim in any of them cannot issue.
- **Primary source:** 35 U.S.C. § 101; *In re Nuijten*; MPEP 2106.03; printed-matter doctrine (MPEP 2111.05).

### `A07` Naturally occurring subject matter: require a human-made distinction
- **Check:** Verify that any claim reading on a natural product, gene, plant, or organism recites human-made structure, a purified/synthetic form, or a new use, rather than the natural thing itself.
- **Severity:** Fatal
- **Applies to:** chemical / biotech / agricultural
- **What to look for:** Isolation or discovery is not enough after *Myriad*. Claims that read on a sequence or substance as it exists in nature fail. Markedly different characteristics, a new use process, or a genetically engineered organism are the usual passing patterns. Confirm the specification describes the human-made distinction, not merely "discovering" the material.
- **Why it matters:** Products of nature are a judicial exception. If every independent claim reads on the natural form, the application fails § 101.
- **Primary source:** 35 U.S.C. § 101; *Ass'n for Molecular Pathology v. Myriad*; *Diamond v. Chakrabarty*; MPEP 2106.04(b)–(c).

## Utility (§101)

### `A08` Verify the specification states a specific, substantial, and credible use
- **Check:** Verify the specification affirmatively recites at least one functional (not aesthetic) use for the claimed invention, stated concretely enough to be proved if challenged.
- **Severity:** Serious
- **Applies to:** all applications; critical for chemical and pharmaceutical
- **What to look for:** Search for a sentence that says what the invention is *for*. The classic failure is a new compound with no disclosed use. Intermediate products used to make a useful item count. A passing draft states a specific, substantial, and credible utility, not a speculative or throw-away use.
- **Why it matters:** 35 U.S.C. § 101 requires utility. MPEP 2107 rejects claims lacking a specific, substantial, and credible utility. Missing utility usually cannot be repaired after filing without new matter.
- **Primary source:** 35 U.S.C. § 101; MPEP 2107; *Brenner v. Manson*.

### `A09` Aesthetic-only inventions: add a functional purpose or redirect to design
- **Check:** Verify the invention's asserted advantage is not purely aesthetic; if it is, confirm a utility application is the right vehicle at all.
- **Severity:** Fatal
- **Applies to:** all applications; industrial design, housings, screen graphics
- **What to look for:** Advantages that are only visual or ornamental belong in a design application under 35 U.S.C. § 171. If a shape also changes function, cost, handling, or performance, state that functional effect in the utility specification and claims. If there is no functional effect, this is the wrong filing type.
- **Why it matters:** A purely ornamental article lacks statutory utility for a utility patent and will be rejected under § 101.
- **Primary source:** 35 U.S.C. §§ 101, 171; MPEP 2107; MPEP 1502.

### `A10` Operability: verify the draft will not read as inoperative
- **Check:** Verify the disclosure describes a mechanism that a technically trained examiner will accept as workable and that does not appear to violate an accepted physical law.
- **Severity:** Fatal
- **Applies to:** all applications; energy, perpetual motion, esoteric physics, medical claims
- **What to look for:** Claimed efficiency over 100%, energy from nothing, unexplained "field" effects, and mechanisms that skip the step where the result is produced. Filing is clerical; operability is examined. If operability would reasonably be questioned, the draft needs technical explanation or data in the specification at filing.
- **Why it matters:** An inoperative invention lacks utility. The applicant then bears the burden to prove operability, and missing technical support cannot be added as new matter.
- **Primary source:** 35 U.S.C. § 101; MPEP 2107.01; *In re Swartz*.

### `A11` Scientific principles: claim a practical application, not the principle
- **Check:** Verify the draft claims a practical, realistic application rather than the underlying discovered phenomenon or principle.
- **Severity:** Fatal
- **Applies to:** all applications; physics, materials, mathematics
- **What to look for:** Specifications that read like a discovery paper, with claims tracking the phenomenon rather than an apparatus or process using it. Test each independent claim: does infringement require making or doing something? Convert every discovery into at least one described embodiment and a claim to that application.
- **Why it matters:** Laws of nature and abstract scientific principles are not patentable. Only a practical application can satisfy § 101.
- **Primary source:** 35 U.S.C. § 101; *Mayo*; *Funk Brothers*; MPEP 2106.04(b).

### `A12` Statutory exclusions and unlawful-use utility
- **Check:** Verify the invention is not solely useful for illegal purposes, is not an unsafe drug with no disclosed safety basis, is not a nuclear weapon, is not a tax-avoidance strategy used to differentiate the claim, and is not a human organism — and that any legitimate use is the one the draft describes.
- **Severity:** Fatal
- **Applies to:** all applications; pharmaceutical, security, financial
- **What to look for:** Purpose statements that frame the invention as evading law enforcement. Claims that read on a human organism (AIA § 33). Tax strategies used as the point of novelty (AIA § 14). Unsafe drugs with no disclosed basis for safety. Reframe around a lawful, useful application if one exists and is supported.
- **Why it matters:** These are statutory or settled utility bars. A poorly framed purpose can create a bar the underlying technology did not require.
- **Primary source:** 35 U.S.C. § 101; AIA § 14 (tax strategies); AIA § 33 (human organisms); Atomic Energy Act limitations; MPEP 2107.

## Novelty (§102)

### `A13` Identify at least one structural or step difference over the closest art
- **Check:** Verify the file contains an explicit statement of what the claimed invention has that the closest prior-art references do not.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** For each independent claim, point to a limitation absent from the closest reference. Novelty can be a new element, a new arrangement, or a new process step. A claim set that has never been mapped against a reference is not ready to file. Record the mapping in the audit file.
- **Why it matters:** Anticipation under § 102 cannot be argued around. Without a novelty analysis, the § 103 argument has nothing to attach to.
- **Primary source:** 35 U.S.C. § 102; MPEP 2131.

### `A14` Do not mistake new results for novelty
- **Check:** Verify the asserted novelty is an actual hardware or method-step difference, not merely an advantage such as lighter, faster, safer, or cheaper.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Answers phrased only as benefits. If the claim's only departure from a reference is an asserted advantage of the same structure, the claim is anticipated. Legitimate differences include different structure, materials, ranges, omitted elements, or different operating conditions actually recited as limitations. Advantages belong in the obviousness analysis.
- **Why it matters:** A claim distinguished only by a result is anticipated under § 102 and argued under the wrong statute.
- **Primary source:** 35 U.S.C. § 102; MPEP 2131; MPEP 2112 (inherency).

### `A15` Apply the single-reference rule and look for a complete anticipating disclosure
- **Check:** Verify no single prior-art reference shows all of the claimed features arranged as claimed.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** For each independent claim, try to read every limitation onto one reference. Anticipation requires one enabled disclosure of the claimed arrangement. If two documents are needed, the claim is novel under § 102 (it may still be obvious under § 103). The failure to catch is a single reference that already teaches the whole claim.
- **Why it matters:** A fully anticipating reference means the claim lacks novelty. Filing it as drafted spends the fee on a certain rejection.
- **Primary source:** 35 U.S.C. § 102; MPEP 2131; *Verdegaal Bros.*

### `A16` Verify the prior-art search covered the statutory universe
- **Check:** Verify the search was not limited to in-force U.S. patents, English-language sources, or patent literature.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Prior art includes patents, published applications, printed publications, public uses, and sales, from anywhere, in any language, including expired patents. A file that shows only a USPTO full-text keyword query is incomplete. Look for NPL, foreign documents, and web publications with verifiable dates.
- **Why it matters:** Art missed before filing surfaces as a § 102/§ 103 rejection or as invalidity after issuance, after the disclosure is locked.
- **Primary source:** 35 U.S.C. § 102; MPEP 2126–2128; MPEP 2152 (AIA).

### `A17` Account for secret prior art in the risk assessment
- **Check:** Verify the applicant has been told that a clean search does not guarantee clean prior art, because unpublished pending applications are already prior art as of their effective filing dates.
- **Severity:** Quality
- **Applies to:** all applications; crowded and fast-moving fields
- **What to look for:** Under AIA 35 U.S.C. § 102(a)(2), an earlier-filed later-published U.S. application is prior art as of its effective filing date. A recent search in a crowded field is not dispositive. The conservative response is prompt filing, not delay in reliance on a clear search.
- **Why it matters:** Secret prior art can appear after filing and defeat claims that looked allowable when drafted.
- **Primary source:** 35 U.S.C. § 102(a)(2), (d); MPEP 2154.

### `A18` Check derivation risk and common-ownership / joint-research exceptions
- **Check:** Verify whether anyone else may have filed first on the same invention and, if so, whether derivation or the common-assignee/joint-research-agreement exception applies.
- **Severity:** Serious
- **Applies to:** all applications; collaborations, employers, consortia
- **What to look for:** Who else had access, and when. An earlier-filed application by another inventor is prior art unless derivation is proved or 35 U.S.C. § 102(b)(2)(C) / § 102(c) applies. For a joint research agreement, the application must disclose the parties. Confirm that disclosure is actually in the draft.
- **Why it matters:** Losing the race to file forfeits the patent. Failing to invoke an available exception leaves an avoidable reference standing.
- **Primary source:** 35 U.S.C. §§ 102(b)(2)(C), 102(c), 135; MPEP 2155–2156.

### `A19` Check for abandonment of the invention
- **Check:** Verify the inventor did not consciously give up on the invention at some point before deciding to file.
- **Severity:** Serious
- **Applies to:** all applications; long-dormant projects
- **What to look for:** Under pre-AIA § 102(c), abandonment could bar a patent. Post-AIA the statutory abandonment bar is gone, but long dormancy still matters for corroboration, inventorship disputes, and whether intervening art or public use occurred. Ask for the chronology whenever conception is years before the planned filing.
- **Why it matters:** Unexplained years of inactivity often hide a public use, sale, or third-party filing that is the real bar.
- **Primary source:** pre-AIA 35 U.S.C. § 102(c); AIA 35 U.S.C. § 102; MPEP 2134 (historical); duty to develop the actual timeline.

## Statutory bars and the grace period

### `A20` Date every inventor-originated disclosure and confirm the one-year grace period
- **Check:** Verify the intended filing date is within one year of the earliest disclosure of the invention by the inventor or by anyone who obtained the details from the inventor.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Build a dated list: papers, talks, demos, web pages, crowdfunding, customer showings, collaborator publications. Under 35 U.S.C. § 102(b)(1), only inventor-originated disclosures within one year are excepted. A provisional or nonprovisional stops the clock. An unknown first-disclosure date is a failing file.
- **Why it matters:** Missing the one-year window converts the inventor's own disclosure into a bar. The U.S. right is then gone.
- **Primary source:** 35 U.S.C. § 102(b)(1); MPEP 2153.

### `A21` Confirm no independent third-party disclosure predates the filing date
- **Check:** Verify that no public disclosure, use, sale, or knowledge originating from anyone other than the inventor occurred before the intended filing date.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** The grace period does not cover independent third-party disclosures. Separate the disclosure list into inventor-originated and third-party. Anything in the second bucket that predates filing is prior art. One day is enough.
- **Why it matters:** A third-party pre-filing disclosure is unexcepted § 102(a)(1) art and typically surfaces in litigation, not in the Office search.
- **Primary source:** 35 U.S.C. § 102(a)(1), (b)(1); MPEP 2152–2153.

### `A22` Date any public use or unrestricted showing
- **Check:** Verify whether the invention has been used or shown publicly without restriction, and when.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Public use is broader than publication. Unrestricted demos, trade-show use, installed prototypes visible to the public, and beta use without confidentiality can all count. Ask specifically about those events and record dates.
- **Why it matters:** Public use is prior art under § 102(a)(1). Inventor-originated public use starts the one-year clock; third-party public use bars immediately.
- **Primary source:** 35 U.S.C. § 102(a)(1); MPEP 2133.03(a) (public use); *Egbert v. Lippmann* line of cases as applied under current § 102.

### `A23` Date any offer to sell, sale, or commercial use
- **Check:** Verify whether the invention or a product embodying it has been offered for sale, sold, or commercially used, and confirm the filing date beats the applicable bar.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A commercial offer for sale can start the bar even if the invention is not yet built, if it is ready for patenting (*Pfaff*). Quotes, purchase orders, and commercial deployments count. Licensing the patent rights is different from selling embodiments. Third-party sales bar immediately; inventor sales start the one-year clock.
- **Why it matters:** An on-sale event that predates the grace period is a complete bar.
- **Primary source:** 35 U.S.C. § 102(a)(1); *Pfaff v. Wells Electronics*; *Helsinn v. Teva*; MPEP 2133.03(b), 2152.02(d).

### `A24` Confirm foreign-filing rights have not already been destroyed
- **Check:** Verify whether any marketing, use, sale, or showing occurred before filing, and record that foreign-filing rights may already be gone.
- **Severity:** Serious
- **Applies to:** all applications where non-U.S. protection is wanted
- **What to look for:** Most foreign systems apply absolute novelty with no grace period. A U.S. grace period does not preserve Paris-priority rights after a public disclosure. If foreign protection matters, the first U.S. filing must precede public disclosure.
- **Why it matters:** Foreign rights lost on first disclosure cannot be revived. The U.S. case may still be fileable while every other market is gone.
- **Primary source:** Paris Convention Art. 4; 35 U.S.C. § 119; PCT Art. 11; national absolute-novelty statutes.

### `A25` Experimental use: confirm the exception actually applies
- **Check:** Verify that any pre-filing public use claimed as experimental was bona fide experimental, and that no nonexperimental use has begun.
- **Severity:** Serious
- **Applies to:** all applications; field-tested and outdoor-installed inventions
- **What to look for:** Experimental use is a narrow, evidence-dependent exception. Look for contemporaneous records of the variable being tested, the measurements, and inventor control. Revenue, marketing, or customer use dressed up as a "beta" usually fails. File before nonexperimental use starts.
- **Why it matters:** If the experimental characterization fails, the activity is a public use that either bars the application or started the one-year clock on an untracked date.
- **Primary source:** *City of Elizabeth v. Pavement Co.*; MPEP 2133.03(e); apply cautiously under AIA § 102.

### `A26` Check the inventor's earlier foreign filings and priority chain
- **Check:** Verify whether the inventor has an earlier foreign application or patent, and confirm the U.S. filing date is set to preserve both validity and priority.
- **Severity:** Fatal
- **Applies to:** applications with foreign-origin inventors or earlier foreign filings
- **What to look for:** Paris priority for a utility application is one year from the first foreign filing (35 U.S.C. § 119). An inventor's own earlier foreign patent can also be prior art if priority is not properly claimed. Confirm the U.S. draft actually contains the priority claim and that the foreign document supports the claims.
- **Why it matters:** Missing the year loses the foreign date. A defective claim can convert the inventor's own foreign patent into invalidating art.
- **Primary source:** 35 U.S.C. § 119; 37 CFR 1.55; MPEP 213–216.

## Nonobviousness (§103)

### `A27` Confirm the difference would not have been obvious to a person of ordinary skill
- **Check:** Verify that the difference between the claimed invention and the prior art produces a result that would be unexpected or surprising to a person having ordinary skill in the art, or is otherwise nonobvious under *Graham* / *KSR*.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Difference alone is not enough. Identify the PHOSITA, the scope of the art, the differences, and the level of skill (*Graham*). Ask whether a skilled artisan would have had a reason to make the change with a reasonable expectation of success. Do not treat the inventor's sense that the idea is "simple" as legal obviousness.
- **Why it matters:** Most rejections that kill applications are § 103 rejections. Filing without this analysis is filing into the highest-probability failure mode.
- **Primary source:** 35 U.S.C. § 103; *Graham v. John Deere*; *KSR v. Teleflex*; MPEP 2141–2143.

### `A28` Screen the claims for predictable substitutions and changes in degree
- **Check:** Verify the claimed advance is not a mere substitution of equivalents, a change in form, size, material, or degree, a duplication of parts, or the addition of modern electronics, without an unexpected result or other nonobviousness showing.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Predictable uses of known techniques, simple substitution of one known element for another, and "obvious to try" finite options (*KSR*). Each such feature is saved only by a reasoned unexpected result or another *Graham* secondary consideration that the draft actually supports.
- **Why it matters:** A claim set built only from predictable modifications has no answer once the examiner cites the base reference plus common sense.
- **Primary source:** 35 U.S.C. § 103; *KSR*; MPEP 2143, 2144.04–2144.07.

### `A29` Combination inventions: require more than a parts list
- **Check:** Verify a combination of individually old elements produces results greater than the independent operation of the parts, or otherwise would not have been obvious to combine.
- **Severity:** Serious
- **Applies to:** all applications; combination and kit inventions, chemical mixtures, recipes
- **What to look for:** Elements that sit side-by-side and do not interact are easy § 103 targets. Passing combinations change how the elements function together. For compositions, look for a cooperative effect beyond the known function of each ingredient. The specification must describe that interaction.
- **Why it matters:** A non-cooperating combination is the classic obvious assemblage even when novel and useful.
- **Primary source:** 35 U.S.C. § 103; *KSR*; MPEP 2143.01; MPEP 2144.06.

### `A30` Pre-build the reason-to-combine response
- **Check:** Verify the draft supports an argument that the prior-art references would not have been combined, given that *KSR* requires only some apparent reason to combine.
- **Severity:** Serious
- **Applies to:** all applications; combination inventions
- **What to look for:** After *KSR*, the Office need not find an explicit teaching-suggestion-motivation. Put in the specification, if true: a different problem, new functions in the combination, unpredictability, teaching away, incompatibility, or a different field. Do not leave the entire combination defense for the first Office Action.
- **Why it matters:** A silent specification hands the examiner an unopposed obviousness rejection.
- **Primary source:** *KSR*; MPEP 2143, 2145.

### `A31` Inventory objective indicia of nonobviousness before filing
- **Check:** Verify the applicant has worked through the secondary considerations and identified every one that applies.
- **Severity:** Quality
- **Applies to:** all applications; essential where the technical difference is modest
- **What to look for:** Long-felt need, failure of others, unexpected results, commercial success (nexus required), copying, skepticism, and teaching away. Commercial success is rarely available pre-filing because a public sale can itself be a bar. Record each factor that can later be supported with evidence.
- **Why it matters:** When the technical difference is thin, objective indicia are often what carries the case. An unrecorded factor will not be argued when the rejection arrives.
- **Primary source:** *Graham*; *Fox Factory* nexus cases; MPEP 716, 2145.

## Setting up the patentability case in the draft

### `A32` Make the specification state unexpected results or the technical improvement explicitly
- **Check:** Verify the specification tells the examiner, in words, what unexpected result or technical improvement the novel feature produces — not just what the invention is.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A passage that names the distinguishing feature, names the result, and says why a skilled worker would not have predicted it. Avoid hindsight framing that treats the solution as obvious once stated. Structure and function without an articulated improvement invite a first-action § 103.
- **Why it matters:** Examiners decide obviousness on the written record. A specification silent on results forces the applicant to build the argument under time pressure.
- **Primary source:** 35 U.S.C. § 103; MPEP 716.02; MPEP 2141.

### `A33` New-use inventions: claim a process and show a nonobvious use
- **Check:** Verify that an invention presented as a new use of old hardware is claimed as a process and is supported by a genuinely different use that would not have been obvious.
- **Severity:** Serious
- **Applies to:** process / new-use applications
- **What to look for:** 35 U.S.C. § 100(b) treats a new use of a known process, machine, manufacture, or composition as a process. Confirm process claiming, and confirm the use is not a predictable new job for the old thing. If any new hardware exists, claim that hardware as well.
- **Why it matters:** A new-use invention claimed as apparatus, or a predictable new use, fails either claiming practice or § 103.
- **Primary source:** 35 U.S.C. §§ 100(b), 101, 103; MPEP 2112.02.

### `A34` Test claim breadth for design-around before filing
- **Check:** Verify the claims are not so narrow or so easy to design around that a granted patent would be commercially worthless.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Change a numeric value, swap a named material, omit a recited step, relocate a component. Independent claims loaded with preferred-embodiment detail are the usual defect. At least one independent claim should sit at the level of the actual inventive contribution.
- **Why it matters:** A patent that is trivial to avoid confers no meaningful exclusive right. That is a commercial failure even if the claim is valid.
- **Primary source:** 35 U.S.C. § 112(b) (scope must be clear); claim-drafting practice in MPEP 2173; infringement is later determined under 35 U.S.C. § 271.

### `A35` Strip inventor-status and manner-of-invention arguments from the draft
- **Check:** Verify the draft does not rest any patentability argument on who the inventor is, their credentials, or how much effort the invention took.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Background passages about years of research, degrees, or persistence offered as reasons to grant. 35 U.S.C. § 103 says patentability is not negated by the manner of invention; equally, manner does not establish patentability. What must be verified is true inventorship, not inventor merit.
- **Why it matters:** Effort and credentials carry no weight. Space spent on them is space not spent establishing differences and results.
- **Primary source:** 35 U.S.C. § 103 (manner of invention); 35 U.S.C. § 115–116 (inventorship).

### `A36` Resolve open legal questions rather than assuming
- **Check:** Verify that no step in the draft or the filing plan rests on an untested assumption about patent law or PTO practice.
- **Severity:** Quality
- **Applies to:** all applications; self-prepared and first-time filings
- **What to look for:** Confident assertions with no cited basis, novel procedural maneuvers, and marketing copy about "patent pending" status that does not match the papers. The passing behavior is documented: look up the current statute, rule, or MPEP section, or ask the USPTO Inventors Assistance Center.
- **Why it matters:** Acting on an incorrect assumption can cost the application or create false-marking exposure. The error is usually discovered after filing is irreversible.
- **Primary source:** current 35 U.S.C., 37 CFR, and MPEP; 35 U.S.C. § 292 (false marking).

### `A37` Run the statutory requirements before authorizing the filing
- **Check:** Verify the invention has been walked through statutory class, utility, novelty, and nonobviousness, with a recorded answer on each.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A recorded yes/no (or cannot-assess) on § 101 category and eligibility, § 101 utility, § 102 novelty, and § 103 nonobviousness. A hard no on any of the first three, or a clear obviousness finding with no secondary considerations, means do not file this draft. Consider trade secret, copyright, design, or trademark instead. Commercial promise is a separate test.
- **Why it matters:** Filing without clearing the statutory requirements pays the fee for an application that fails a requirement that could have been identified beforehand.
- **Primary source:** 35 U.S.C. §§ 101–103; MPEP 2103–2107, 2131, 2141.
