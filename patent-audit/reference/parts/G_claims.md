# Part G — Claims

64 items (17 Fatal).

Grounded in 35 U.S.C. §§ 101, 102, 103, 112; 37 CFR 1.75; MPEP 608.01(i)–(n), 2106, 2173, 2181.

## Claim-set architecture and formal requirements

### `G01` Confirm at least one independent claim exists and is the broadest claim
- **Check:** Verify the draft contains at least one independent claim that stands alone and defines a complete, operative invention, and that it is drafted to be as broad as the prior art permits.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A specification with no claim cannot obtain a filing date (35 U.S.C. § 111). The lead independent claim should recite the fewest elements and the broadest wording the art allows. Preferred-embodiment specifics belong in dependents.
- **Why it matters:** No claim means no filing date. A needlessly narrow sole independent claim yields a patent competitors can avoid.
- **Primary source:** 35 U.S.C. § 111; 37 CFR 1.75; MPEP 608.01(k).

### `G02` Provide alternative independent claims of different statutory types plus dependent backup
- **Check:** Verify the claim set includes more than one independent claim, drafted in different forms (apparatus, means, method) where the invention admits, each followed by dependent claims reciting the significant additional features.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A single apparatus claim and nothing else. Cosmetic rewordings of claim 1. Each independent should have a real dependent chain.
- **Why it matters:** If the sole independent falls, there is no backup. Different claim types also capture different classes of infringer.
- **Primary source:** 37 CFR 1.75; MPEP 608.01(n).

### `G03` Do not rely on a dependent claim to cover a feature standing alone
- **Check:** Verify the draft does not depend on a dependent claim to protect an important feature *per se*.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A commercially important feature that appears only in a dependent. Under § 112(d) the dependent incorporates every parent limitation. If the feature must be owned alone, it needs its own independent (if the art allows).
- **Why it matters:** A competitor practicing the feature without the parent's other elements does not infringe the dependent.
- **Primary source:** 35 U.S.C. § 112(d); MPEP 608.01(n).

### `G04` Check claim numbering, ordering, and physical layout against Rule 75
- **Check:** Verify claims are numbered consecutively in Arabic numerals, the least restrictive claim is claim 1, dependent claims are grouped with the claims they refer to, elements are set off by line indentation, and the claims begin on their own page.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Numbering gaps, a narrow claim 1, dependents that refer forward, run-on blocks, claims that do not start on a new sheet.
- **Why it matters:** Rule 75 violations cost an Office Action cycle and increase misconstruction risk.
- **Primary source:** 37 CFR 1.75; MPEP 608.01(i)–(m).

### `G05` Avoid multiple dependent claims and an unjustified claim count
- **Check:** Verify no claim refers in the alternative to more than one preceding claim, and that the total number of claims is justified by the complexity of the invention.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** "Any of claims 1 to 5." Excess-claim fees apply above three independents and twenty total (re-verify current 37 CFR 1.16). Near-identical dependents that add nothing.
- **Why it matters:** Multiple dependents carry a surcharge and examiner resistance. Padding costs fees and invites objection under Rule 75(b).
- **Primary source:** 37 CFR 1.75(c), 1.16; MPEP 608.01(n).

### `G06` Check claim punctuation, capitalization, and forbidden characters
- **Check:** Verify each claim has one capital letter (the first word), one period (at the end), and contains no dashes, quotation marks, parenthetical asides, trademarks, or unexpanded abbreviations.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Mid-claim periods, stray capitals, brand names as element names. Lettered subparagraphs are the permitted exception.
- **Why it matters:** Formal defects draw § 112(b) objections. Trademarks as element names are indefinite because the mark's scope can change.
- **Primary source:** 37 CFR 1.75; MPEP 608.01(m).

### `G07` Check that every claim has a proper preamble in a statutory class, and avoid Jepson form
- **Check:** Verify each independent claim opens with a preamble that names its statutory class or gives a title/purpose for the whole unit, and that the draft does not use the Jepson "wherein the improvement comprises" format unless there is a specific reason.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Preambles that use a coined product name or bake in a narrow use. Jepson form admits everything before the improvement clause as prior art.
- **Why it matters:** A claim not classifiable into a statutory class draws § 101 scrutiny. A Jepson claim isolates the novel part and makes invalidity easier.
- **Primary source:** 35 U.S.C. § 101; 37 CFR 1.75(e); MPEP 608.01(m), 2129.

## Definiteness and antecedent basis

### `G08` Verify correct use of "a," "said," and "the," and distinct names for distinct elements
- **Check:** Verify each element is introduced with "a," referred back to with "said" or "the" using consistent words, and that different elements of the same kind are named "first"/"second."
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** An element positively recited twice with "a." Bare "said lever" after "a first lever" and "a second lever." Use "the" only for an implicit aspect of an already-recited element.
- **Why it matters:** Improper articles are among the most common § 112(b) rejections.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(e).

### `G09` Hunt for missing antecedents
- **Check:** Verify that every "said X" has an earlier recitation of "X" in the same words, within that claim or an available parent.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Near-synonyms offered as antecedents. Dependents that lost their antecedent when a parent was edited. Trace the whole chain.
- **Why it matters:** A missing antecedent is a non sequitur under § 112(b).
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(e).

### `G10` Flag vague, casual, and unanchored relative terms
- **Check:** Verify the claims contain no unexpanded abbreviations and no vague or relative terms unless anchored to a reference a skilled artisan can apply.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Large," "close," "suitable," "sufficient" with no yardstick. Spell out abbreviations at first use. If the specification supplies a functional measure, say so in the finding.
- **Why it matters:** Unanchored relative terms fail *Nautilus* reasonable-certainty.
- **Primary source:** 35 U.S.C. § 112(b); *Nautilus*; MPEP 2173.05(b).

### `G11` Check for prolixity
- **Check:** Verify each claim uses the minimum number of words needed to delineate the essence of the invention, with roughly one clause per necessary part.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Claims that paraphrase the detailed description. Substantially more clauses than numbered parts. Every extra word is an extra limitation an accused device can avoid.
- **Why it matters:** Prolixity is a recognized objection and silently narrows scope.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(m).

## Element recitation discipline

### `G12` Verify every element is affirmatively recited as the subject of its own clause
- **Check:** Verify each significant element is introduced positively as the subject of its own clause, and that no function is recited before the element that performs it has been affirmatively recited.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Elements smuggled in by possessives or incidental wording. Functional clauses whose actor was never recited.
- **Why it matters:** Inferred elements lack clear antecedent basis. A function with no recited actor may be given no patentable weight.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(q).

### `G13` Verify each element is followed only by its own shape or function
- **Check:** Verify no element recitation is immediately followed by the function of a *different* element.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A passive container credited with a velocity imparted by something else. Split the clauses.
- **Why it matters:** Attributing another element's function makes the claim indefinite and leaves the actual actor unclaimed.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05.

### `G14` Verify every recited operation has enough structure behind it
- **Check:** Verify that any operation, movement, or result recited in a claim is attributed to structure adequate to perform it, or is expressed as a means clause with corresponding structure in the specification.
- **Severity:** Serious
- **Applies to:** all applications; especially mechanical and electromechanical
- **What to look for:** A simple passive part credited with coordinated or timed behavior it cannot perform alone. Recite the enabling structure or a supported means clause.
- **Why it matters:** Insufficient structural support makes the claim functional at the point of novelty.
- **Primary source:** 35 U.S.C. § 112(b), (f); MPEP 2181.

### `G15` Replace negative limitations with positive ones
- **Check:** Verify the claims recite what the invention is rather than what it is not, except where a negative limitation is clear and supported.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** "Without," "free of," "excluding" used awkwardly. Voids such as holes are positive structure, not negatives. Restate as a direct connection or affirmative structure where possible.
- **Why it matters:** Unclear negatives draw § 112(b) rejections. Negative limitations also need written-description support (*Santarus*).
- **Primary source:** 35 U.S.C. § 112(a)–(b); MPEP 2173.05(i).

### `G16` Audit the connectives "and" and "or"
- **Check:** Verify each use of "and" and "or" has one unambiguous meaning, with "and" reserved for necessary structure and alternatives handled as a genus, a Markush group, or separate dependents.
- **Severity:** Serious
- **Applies to:** all applications; especially chemical
- **What to look for:** Mixed "and/or" lists in an independent claim. For compositions, "selected from the group consisting of" is the closed Markush form.
- **Why it matters:** Ambiguous connectives make scope indeterminate.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(h).

## Completeness, interrelation, and aggregation

### `G17` Verify each claim recites a complete, operative assemblage
- **Check:** Verify each claim, standing alone, recites enough elements to define a working, complete device or process consistent with what is recognized as a unit in its art.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A claim stripped so aggressively it recites a fragment with no operative identity. Add only as many elements as needed — each addition costs breadth.
- **Why it matters:** An incomplete claim fails to define the invention under § 112.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2172.01.

### `G18` Verify all elements interconnect and cooperate
- **Check:** Verify every element recited in a claim is logically related and physically or functionally connected to the other elements, and that the combination cooperates toward a common end.
- **Severity:** Serious
- **Applies to:** all applications; especially mechanical
- **What to look for:** A bare parts list with no interconnection clauses. Elements that do not work toward one result. Simultaneous operation is not required.
- **Why it matters:** Unconnected elements fail to distinctly claim the invention. A non-cooperating combination is an easy § 103 target.
- **Primary source:** 35 U.S.C. §§ 103, 112(b); MPEP 2172.01, 2143.

## Functional claiming and means-plus-function

### `G19` Flag elements claimed by result or function instead of structure
- **Check:** Verify no claim element is defined solely by the advantage, function, or result it produces without reciting structure or a supported means/device clause.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Claims that describe what the invention does rather than what it is. Recite structure, and use function as a qualifier, not the whole limitation.
- **Why it matters:** Pure result claiming is indefinite and often abstract.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(g).

### `G20` Check for prohibited single-means claims
- **Check:** Verify that any claim using "means" language recites a combination of two or more elements, not a single means.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A body that reduces to one "means for …" with nothing else. § 112(f) requires a combination. Adding a second recited element converts it into a combination claim.
- **Why it matters:** A single-means claim is rejected as too broad and does not invoke § 112(f) properly.
- **Primary source:** 35 U.S.C. § 112(f); MPEP 2181; *In re Hyatt*.

### `G21` Verify every means (and every component) has corresponding structure in the specification
- **Check:** Verify that each "means for" clause, and each non-means component recited in the claims, is clearly described as specific structure, material, or acts in the specification.
- **Severity:** Fatal
- **Applies to:** all applications; especially software/business method
- **What to look for:** For software, corresponding structure must include an algorithm, not a generic computer. Add an express bridging sentence where the mapping is not obvious. The linkage cannot be added later.
- **Why it matters:** A means clause with no disclosed structure is indefinite and has no scope.
- **Primary source:** 35 U.S.C. § 112(f); MPEP 2181; *Aristocrat*; *Williamson v. Citrix*.

### `G22` Verify the set includes non-means claims alongside any means claims
- **Check:** Verify that if the draft uses means-plus-function claiming, it also includes one or more independent claims written with structural language and made as broad as possible.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Every independent claim is a means claim. After *Williamson*, "means" is not required to invoke § 112(f). Structural claims can reach equivalents more predictably when drafted broadly.
- **Why it matters:** A means-only set is tethered to the disclosed structures and their equivalents.
- **Primary source:** 35 U.S.C. § 112(f); *Williamson*; MPEP 2181.

## Claim breadth versus prior art

### `G23` Count the elements in the main claim and cut every unnecessary one
- **Check:** Verify the broadest independent claim recites the fewest elements consistent with an operative, complete assemblage that is novel and nonobvious.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Housings, fasteners, power supplies, and user interfaces imported from the commercial product that play no role in the inventive concept. A thirteen-element claim is avoided by omitting any one element.
- **Why it matters:** Every additional element is one more thing an accused device must have.
- **Primary source:** 35 U.S.C. §§ 102, 103, 112; MPEP 2173.05.

### `G24` Check that each element is recited at the broadest usable level of generality
- **Check:** Verify no element in the broad independent claim carries a specific material, dimension, count, or embodiment detail that is not needed to distinguish the prior art.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Numbers, material names, and brandable components in claim 1. Recite the genus; put species in dependents. Specification specific and long; main claims general and short.
- **Why it matters:** A claim is limited to the feature exactly as recited.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(a)–(c).

### `G25` Test the claims against foreseeable design-arounds
- **Check:** Verify that for each key limitation, the auditor has considered how a competitor could achieve the same effect differently, and that the claim (and the specification's ramifications) covers that variation.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A recited direction, order, or threshold that can be inverted or offset. Broaden to the effect and put the alternative in the specification now — new matter cannot be added later.
- **Why it matters:** A claim that names one arrangement invites an easy design-around.
- **Primary source:** 35 U.S.C. §§ 112(a), 271; *Graver Tank* (equivalents are a poor substitute for clear drafting).

### `G26` Verify each claim defines over the known prior art, with novelty in recited structure
- **Check:** Verify each independent claim recites something no single prior-art reference shows, expressed as positive, structurally supported novel hardware or a novel process step, and that the difference is nonobvious.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Every recited element already in one reference. Novelty expressed only as a new function of old structure. Confirm the text and figures already support any narrowing you would need in prosecution.
- **Why it matters:** A claim that reads on a single reference is anticipated. A merely novel but obvious difference falls under § 103. Missing support blocks the narrowing amendment.
- **Primary source:** 35 U.S.C. §§ 102, 103, 112(a); MPEP 2131, 2141, 2163.

### `G27` Read every claim under its least favorable interpretation
- **Check:** Verify that no claim wording admits a second reading under which the claim would read on the prior art or lose its point of novelty.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Ambiguous terms a keyword-searching examiner will read broadly. Define load-bearing terms in the specification. Err broad at filing — narrowing later is easy, broadening after allowance is not.
- **Why it matters:** During examination the Office applies BRI. Ambiguity produces avoidable rejections.
- **Primary source:** MPEP 2111; 35 U.S.C. § 112(b).

## Correspondence with the specification and drawings

### `G28` Verify every claim term appears literally in the specification
- **Check:** Verify that every term and phrase used in the claims appears verbatim in the specification, with clear support or antecedent basis.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Renaming during editing. Search the specification for each claim term as written. Consider a glossary of the important terms.
- **Why it matters:** 37 CFR 1.75(d)(1) requires claim terms to find clear support in the description. Missing support cannot be added after filing.
- **Primary source:** 37 CFR 1.75(d)(1); 35 U.S.C. § 112(a)–(b); MPEP 608.01(o), 2173.05(e).

### `G29` Verify every claimed feature is shown in the drawings
- **Check:** Verify the drawings show every feature recited in the claims.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Elements added to the claims late. Broad recitations can be supported by specific hardware, but new hardware cannot be added after filing. Sweep alternatives into the drawings now.
- **Why it matters:** 37 CFR 1.83 requires the drawings to show every claimed feature. The only post-filing remedy may be to abandon the claim.
- **Primary source:** 37 CFR 1.83; MPEP 608.02.

## Statutory subject matter (§101)

### `G30` Test every claim against the judicial exceptions
- **Check:** Verify no claim is directed to a law of nature, natural phenomenon, or abstract idea without additional elements amounting to significantly more.
- **Severity:** Fatal
- **Applies to:** all applications; especially software/business method and diagnostic
- **What to look for:** Apply current USPTO Step 2A/2B. Look for a technological improvement, a particular machine, a transformation, or unconventional extra-solution activity actually recited. Clearing § 101 does not excuse §§ 102, 103, or 112.
- **Why it matters:** An ineligible claim will be rejected regardless of novelty.
- **Primary source:** 35 U.S.C. § 101; *Alice*; *Mayo*; MPEP 2106.

### `G31` Run the software-as-tool test on computer-implemented claims
- **Check:** Verify that any claim involving computers, software, or the Internet is directed to an application of the idea, rather than using a computer merely as a conventional means to implement an idea that could be practiced without one.
- **Severity:** Fatal
- **Applies to:** software/business method
- **What to look for:** Notionally delete every computer recitation. If a coherent business practice or mental process remains, the claim is at risk. Escapes: an improvement to computer function, unconventional hardware, or an unconventional ordered combination of conventional elements.
- **Why it matters:** Without an inventive concept beyond the abstract idea, the entire software application can fail on eligibility.
- **Primary source:** 35 U.S.C. § 101; *Alice*; *Enfish*; *Bascom*; MPEP 2106.05.

## Drafting the independent claim

### `G32` Build each independent claim as preamble, elements, interconnections, then a non-narrowing close
- **Check:** Verify every independent claim contains a preamble, an affirmative recitation of each element or step, explicit interconnections among all recited parts, and shows evidence of a deliberate broadening pass.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A parts-list claim. Trace a connected graph through every element with no orphans.
- **Why it matters:** Disconnected or incomplete recitations produce indefiniteness and easy design-arounds.
- **Primary source:** 35 U.S.C. § 112(b); 37 CFR 1.75; MPEP 608.01(m).

### `G33` Broaden the main claim to the fewest, most generalized elements that still clear the art
- **Check:** Verify the broadest independent claim has been stripped of nonessential elements and of unnecessary material, shape, and dimensional limitations, without becoming so broad that it reads on the prior art.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Prototype language in claim 1. After broadening, confirm the claim still recites enough to be novel and nonobvious. Specific versions live in dependents.
- **Why it matters:** Over-narrow independents are commercially worthless. Over-broad ones read on art. Breadth lost at filing may be unrecoverable if the case allows first action.
- **Primary source:** 35 U.S.C. §§ 102, 103, 112; MPEP 2173.05.

### `G34` Preamble names a statutory class or a deliberately broad title
- **Check:** Verify each independent claim's preamble either names a statutory class or gives a title/function broad enough that it cannot be construed narrowly.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Commercial-product preambles. Follow with an open transition ("comprising") and a colon.
- **Why it matters:** A narrow preamble can be read as a claim limitation for the life of the patent.
- **Primary source:** 35 U.S.C. § 101; MPEP 2111.02.

### `G35` Recite every significant element affirmatively, as the subject of its own clause
- **Check:** Verify each significant element is introduced positively with "a"/"an" as the subject of its own clause, not smuggled in as a possessive, an object, or an assumed part.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Whose," "its," and first appearances as objects of prepositions. List every noun and mark where it is introduced.
- **Why it matters:** Incidental introduction can mean the part does not count as a limitation, distorting scope.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(e).

### `G36` Every functional recitation has structural or means support
- **Check:** Verify no claim contains a naked functional clause, that each function is preceded by an affirmative recitation of the element that performs it, and that no element is followed by another element's function.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Dangling participial clauses. Functions too big for the recited hardware. Convert to structure or a supported means clause.
- **Why it matters:** Naked functional language is indefinite and, if it survives, is construed unpredictably.
- **Primary source:** 35 U.S.C. § 112(b), (f); MPEP 2173.05(g), 2181.

### `G37` Purge vague relative terms; hedge specific parameters
- **Check:** Verify no claim relies on undefined relative terms and that specific dimensions or parameters are hedged with "substantially," "about," or "predetermined" rather than recited absolutely, unless a precise value is the invention.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Bare size adjectives. Hard numbers that merely describe the prototype. Introduce plural elements as "a plurality of."
- **Why it matters:** Relative terms draw indefiniteness rejections. Unhedged exact dimensions let an infringer escape by a millimeter.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(b)–(c).

### `G38` Close each independent claim with a "whereby" clause that is not too narrow
- **Check:** Verify each independent claim ends with a "whereby" clause stating the advantage or use of the invention, phrased broadly enough that it cannot be turned into a narrowing limitation.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Independents that stop after the last interconnection. Whereby clauses that recite a numeric performance figure. A broad use statement can help the examiner see the § 103 point without handing an accused infringer an escape.
- **Why it matters:** An over-narrow whereby clause can be construed against the patentee. A missing one loses a free chance to state the advantage.
- **Primary source:** MPEP 2111.04 (whereby clauses); *Phillips*.

### `G39` Independent claims should not be conspicuously short — but must avoid prolixity
- **Check:** Verify no independent claim is so terse that an examiner will read it as facially overbroad, and that any padding adds no unnecessary limitations.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** One- or two-line independents. Pad with a fuller preamble, functional descriptions in means clauses, or a whereby clause — not with new structural limitations.
- **Why it matters:** Very short claims attract adverse treatment as presumptively overbroad; padding with real limitations quietly narrows scope.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(m).

### `G40` Do not cast claims in Jepson format unless required
- **Check:** Verify no claim uses a Jepson-style preamble reciting the old elements followed by "the improvement comprising," unless there is a specific reason.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Characterized in that," "of the type comprising." Convert to a single-part claim unless the examiner requested Jepson form or the contribution is otherwise unclear.
- **Why it matters:** The Jepson preamble is an admission of prior art and isolates the improvement.
- **Primary source:** 37 CFR 1.75(e); MPEP 608.01(m), 2129.

### `G41` Apply the sketchability test to every independent claim
- **Check:** Verify that a reader who has not seen the drawings can sketch the invention from the claim alone.
- **Severity:** Serious
- **Applies to:** all applications (especially mechanical)
- **What to look for:** An element whose position relative to others is never stated. If the specification or figures are required to complete the sketch, the claim is under-specified.
- **Why it matters:** A claim that cannot be sketched is not particularly pointing out the invention.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.

## Antecedents, articles, and terminology

### `G42` Every term has a proper antecedent, and articles are used correctly
- **Check:** Verify every term used later in a claim was introduced earlier with "a"/"an," that subsequent references use "said" (identical term) or "the" (clearly implied term), and that "the said" never appears.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Sub-features that appear only in the back half of a claim. A second similar element reused under the same noun. Walk each claim with a running introduced-parts list.
- **Why it matters:** Missing antecedent basis is one of the most common indefiniteness rejections.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(e).

### `G43` No term debuts in the claims; every claimed part appears in the drawings and specification
- **Check:** Verify every term and every part recited in any claim is already used in the specification and depicted in the drawings.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Terms coined during claim broadening that never made it back into the spec. A practical test: insert drawing numerals after each claim element in a working copy, see which have no number, then strip the numerals before filing.
- **Why it matters:** Claim terms with no basis draw § 112 rejections, and a missing drawing element cannot be fixed without new-matter issues.
- **Primary source:** 37 CFR 1.75(d)(1), 1.83; MPEP 608.01(o).

## Means-plus-function claims

### `G44` Label every "means" and follow it with a function or structure
- **Check:** Verify each "means" recitation carries a distinguishing adjective or ordinal and is immediately followed by "for …" plus a function, or by a structural recitation.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Bare "means" with no modifier. "Means connected to the housing" with no function. Index every means clause by its label.
- **Why it matters:** Unlabeled means clauses are indefinite and unreferenceable in dependents.
- **Primary source:** 35 U.S.C. § 112(f); MPEP 2181.

### `G45` The specification discloses corresponding structure for every means clause, in the same words
- **Check:** Verify that for each unique "means for <function>" the specification describes hardware or an algorithm performing that function, using the same words used in the claim.
- **Severity:** Fatal
- **Applies to:** all applications (especially software/business method)
- **What to look for:** A means clause invented during broadening whose function is described only in different words, or not at all. Point, for each means clause, at a specification passage using the claim's own functional wording.
- **Why it matters:** No corresponding structure means the claim is invalid under § 112(b)/(f). This cannot be cured after filing.
- **Primary source:** 35 U.S.C. § 112(f); MPEP 2181; *Aristocrat*.

## Claim mechanics, punctuation, and format

### `G46` Use open transitional language and avoid loose disjunctives
- **Check:** Verify every claim uses "comprising" or "including" rather than "consisting" or "having only," unless closed language is a deliberate chemical choice, and that no claim uses a loose "or" except for equivalent parts or a disjunctive machine function.
- **Severity:** Serious
- **Applies to:** all applications (closed transitions are a particular risk in chemical claims)
- **What to look for:** "Consisting" used by accident. Alternatives that should be a genus, a Markush group, or separate dependents.
- **Why it matters:** "Consisting" is closed: an infringer escapes by adding a part. Loose disjunctives are indefinite.
- **Primary source:** MPEP 2111.03; 35 U.S.C. § 112(b).

### `G47` Enforce claim punctuation and typographic hygiene
- **Check:** Verify no claim contains abbreviations, dashes, parentheses, or quotation marks except as permitted for lettered subparagraphs, and that each claim has exactly one capital letter and one period aside from those subparagraphs.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Units written as abbreviations, quoted trademarks, specification-style asides.
- **Why it matters:** Punctuation defects draw formal objections and can become indefiniteness issues.
- **Primary source:** 37 CFR 1.75; MPEP 608.01(m).

### `G48` Format the claim set: subparagraphs, hanging indents, line skips, and page layout
- **Check:** Verify long claims are broken into lettered subparagraphs in hanging-indent style, that a line is skipped between claims, and that the claims begin on a new page with adequate line spacing.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Multi-element claims as a single unbroken block. Independent numbers not visually distinct.
- **Why it matters:** Rule 75(i) calls for separate paragraphs for elements or steps.
- **Primary source:** 37 CFR 1.75(i); MPEP 608.01(m).

## Dependent claims

### `G49` Every independent claim carries a backup set covering every novel feature
- **Check:** Verify each independent claim is followed by several dependent claims, and that every possibly novel or significant feature and combination appears somewhere in the claim set.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** A lone independent with one or two dependents. Features eliminated during broadening that never returned as dependents. Features the drafter dismissed as unimportant that later carry the case.
- **Why it matters:** Without narrower backup, a single reference invalidates the whole patent. Thin dependents also let the examiner make the next action final on newly cited art.
- **Primary source:** 35 U.S.C. § 112(d); 37 CFR 1.75; MPEP 608.01(n).

### `G50` Each dependent claim uses proper referencing form
- **Check:** Verify every dependent claim opens by referring to its parent by the parent's exact title in the first or second line, and uses "wherein" to narrow an existing element or "further including"/"further comprising" to add elements.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A preamble that does not correspond to the parent. A reference buried mid-claim. An independent that refers to another claim.
- **Why it matters:** Improper dependent form creates missing antecedents and may be treated as an extra independent for fees.
- **Primary source:** 35 U.S.C. § 112(d); 37 CFR 1.75; MPEP 608.01(n).

### `G51` Dependent claims narrow only — no substitutions and no class changes
- **Check:** Verify each dependent claim either recites a parent element more specifically or adds elements, never substituting a different part or switching statutory class.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** A parent reciting red bricks and a dependent changing them to yellow. Method limitations depending from apparatus claims, or mixed method/apparatus Markush groups. Mentally expand each dependent to include all of its parent's wording.
- **Why it matters:** A substituting dependent is improper. Mixed classes create fatal uncertainty about when infringement occurs.
- **Primary source:** 35 U.S.C. § 112(d); MPEP 608.01(n), 2173.05(p).

### `G52` Dependent claims need structural support, and must narrow the means rather than the function
- **Check:** Verify no dependent recites a purely functional limitation without structure or means, and that a dependent limiting a parent's means-plus-function element modifies the means, not the function.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Wherein said X operates with…" and no hardware. "Wherein said ratio ranges from 5 to 10" attached to a means-plus-function parent — narrow the means instead.
- **Why it matters:** Purely functional dependents are indefinite, and they are the fallback most likely to fall with the independent.
- **Primary source:** 35 U.S.C. § 112(b), (f); MPEP 2181.

### `G53` Depend directly from the independent claim and number dependents near their parents
- **Check:** Verify almost all dependent claims depend directly from an independent claim rather than from another dependent, and that each dependent is numbered close to its parent.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** Long chains that silently import every prior limitation. Scattered numbering.
- **Why it matters:** Needlessly chained dependents are far narrower than intended, so the fallback they were written to provide is illusory.
- **Primary source:** 37 CFR 1.75; MPEP 608.01(n).

### `G54` Use significant limitations and cover feasible permutations
- **Check:** Verify dependent claims recite limitations an infringer would plausibly adopt, and that feasible combinations of the subsidiary features are claimed, not just each feature individually.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Colors, cosmetic dimensions, and arbitrary tolerances. With features a, b, and c, look for a, b, c and the workable pairs and triple.
- **Why it matters:** Trivially specific limitations may be novel but obvious, so they provide no real fallback. Uncovered permutations are scope given away.
- **Primary source:** 35 U.S.C. §§ 102–103; MPEP 608.01(n).

### `G55` Include single-element differentiation claims, one maximal claim, and one publicly detectable claim
- **Check:** Verify most dependents recite a single added element (for claim differentiation), that at least one dependent recites as many parts as possible, and that at least one claim covers something whose infringement can be observed publicly.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Every dependent piles on three or four limitations. Abstract means terms never reified. Claims that can be detected only inside a competitor's factory.
- **Why it matters:** Single-element dependents broaden the independent by differentiation. A maximal dependent can support a broader damages base. An unobservable claim cannot practically be enforced.
- **Primary source:** claim-differentiation doctrine; 35 U.S.C. § 284; MPEP 2173.05.

## Claim sets and statutory classes

### `G56` Provide multiple, substantially differently phrased independent claim sets, with and without means clauses
- **Check:** Verify the application contains additional claim sets whose independents phrase the invention in substantially different ways, including one set using means-plus-function clauses and one set without.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Independents that differ by a word or two. Legitimate techniques: start from a different element, use different generic names, invert order, convert means to structure. Claim unique blanks, supplies, accessories, or a novel process of making if they exist.
- **Why it matters:** Alternative independents are additional weapons and additional chances for allowable subject matter. Unclaimed intermediates are dedicated to the public.
- **Primary source:** 37 CFR 1.75; disclosure-dedication doctrine; MPEP 608.01(n).

### `G57` Include an independent method claim and its dependent set wherever possible
- **Check:** Verify the application includes at least one independent method claim with its own dependents whenever the invention involves any dynamic operation.
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** Apparatus-only sets for machines that clearly operate. Method sets that are hardware with "-ing" bolted on. Cover more than one statutory class.
- **Why it matters:** Method claims are usually not limited to specific hardware and are often broader. Omitting them leaves coverage that cannot be recaptured except by a new application.
- **Primary source:** 35 U.S.C. §§ 100(b), 101; 37 CFR 1.75.

### `G58` Every method-claim step is an action step in gerund form
- **Check:** Verify each substantive clause of every method claim begins with an "-ing" action word, that hardware is introduced with "providing," and that "comprising the steps of" is not used.
- **Severity:** Serious
- **Applies to:** all applications with method claims
- **What to look for:** Noun-phrase clauses in a method claim. The word "step," which can invite a narrower construction. Results or states of being offered as steps.
- **Why it matters:** Non-action clauses create indefiniteness and mixed-class problems.
- **Primary source:** 35 U.S.C. § 112(b); MPEP 2173.05(p).

### `G59` Every process claim is tied to a practical application
- **Check:** Verify each process claim is either tied in a substantial way to a particular machine or apparatus, recites a transformation of an article, or otherwise recites a practical application that is not an abstract idea under current § 101 guidance.
- **Severity:** Fatal
- **Applies to:** all applications with method claims; especially software/business method
- **What to look for:** A generic "computer" in the preamble as the only tie. Claims that recite only data manipulation, mental steps, or organizing human activity. Machine-or-transformation is a useful clue, not the sole test after *Bilski* and *Alice*. Answer "which machine, or what transforms into what, or what technological improvement?" from the claim text.
- **Why it matters:** A process claim that is neither a practical application nor significantly more than an abstract idea is ineligible.
- **Primary source:** 35 U.S.C. § 101; *Bilski*; *Alice*; MPEP 2106.

### `G60` Method claims focus all steps on a single actor
- **Check:** Verify each method claim's steps could all be performed by one actor, rather than being split between a service provider and its customers.
- **Severity:** Serious
- **Applies to:** all applications with method claims; especially software/business method and networked systems
- **What to look for:** Annotations that name two actors. Mixes of server-side and customer-side steps. Rewrite so one actor performs or controls every step, and consider parallel claims from each actor's perspective.
- **Why it matters:** Direct infringement of a method claim requires a single actor to perform all the steps (*Akamai* / *Limelight* framework). A divided claim is expensive to enforce.
- **Primary source:** 35 U.S.C. § 271; *Limelight v. Akamai*; MPEP does not decide infringement — flag as a drafting defect.

### `G61` Software inventions include a tangible, non-transitory computer-readable medium claim
- **Check:** Verify a software invention is claimed not only as a method and machine but also as a manufacture — a tangible, non-transitorily encoded medium — with a mirrored set of dependents.
- **Severity:** Serious
- **Applies to:** software/business method
- **What to look for:** Recite both "tangible" and "non-transitory" (or current equivalent). A claim to a bare signal is unpatentable (*Nuijten*). Dependents copied from the method set must be re-preambled; leftover "The method of claim X" is a common paste error.
- **Why it matters:** Without a medium claim there are no offensive rights against a distributor of the software itself.
- **Primary source:** 35 U.S.C. § 101; *In re Nuijten*; MPEP 2106.03.

### `G62` Each independent claim stands entirely on its own
- **Check:** Verify no independent claim refers to, incorporates, relies on, or borrows a referent from any other claim.
- **Severity:** Fatal
- **Applies to:** all applications
- **What to look for:** Copy-paste from a first set: "said wheel" in claim 10 when "a wheel" appears only in claim 1. "A second lever" with no first lever in that claim. Dependents of a second set pointing at claim 1 by leftover reference.
- **Why it matters:** A borrowing independent lacks antecedent basis and may be treated as an improper dependent.
- **Primary source:** 35 U.S.C. § 112(b), (d); 37 CFR 1.75; MPEP 608.01(n).

## Claim count, fees, and multiple dependency

### `G63` Keep the set within three independent and twenty total claims unless justified
- **Check:** Count independent claims and total claims and verify the set does not exceed three independent or twenty total without a documented justification based on the invention's complexity.
- **Severity:** Quality
- **Applies to:** all applications
- **What to look for:** The opposite failures: an over-padded set that incurs excess-claim fees, and an under-used allotment that wastes coverage already paid for. Re-verify current 37 CFR 1.16 amounts. A working pattern is three independents and several dependents each.
- **Why it matters:** The basic filing fee covers three independents and twenty total. Excess claims cost real money; an under-populated set forfeits protection already paid for.
- **Primary source:** 37 CFR 1.16; current USPTO fee schedule.

### `G64` Avoid multiple dependent claims
- **Check:** Verify no claim depends on more than one previous claim (for example, "The widget of claims 1 or 2 wherein …").
- **Severity:** Serious
- **Applies to:** all applications
- **What to look for:** "Claims" (plural) and "or claim" in dependent references. Common in European-style drafts. Expand into separate single-dependency claims and recheck the total count.
- **Why it matters:** Multiple dependents carry a surcharge and, for fee purposes, count as the number of claims to which they refer.
- **Primary source:** 37 CFR 1.75(c), 1.16; MPEP 608.01(n).
