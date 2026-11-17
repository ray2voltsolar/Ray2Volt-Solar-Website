# Builder guide — Ray2Volt brochure pages

The brochure is "Solar & Green Energy, Explained", an 18-page A4 portrait guide from Ray2Volt Solar Private Limited (a solar company in Andhra Pradesh, India). A bank manager will hand it to their clients, and we do not know who those clients are: a retired teacher, a shop owner, a factory owner, an investor, a farmer. So every page must make sense to someone who has never thought about electricity, without talking down to someone who runs a factory. It has to look like a professionally designed publication, and the exhibits on each page — charts, flow diagrams and schematics — carry the explanation: a reader who only looks at them should still get the idea.

## How pages are built

Each page is one HTML fragment in `brochure/src/pages/NN-name.html`: a single `<section class="page" data-sec="…">`. `build.js` stitches them together with `src/base.css` (the design system) and `src/sprite.svg` (icons, arrowheads, gradients) and prints the PDF.

**Read these three files before writing anything:** `src/base.css`, `src/sprite.svg`, and `src/pages/07-net-metering.html` (the finished reference page — match its quality, density and tone). Look at `preview/07-net-metering.png` to see how it renders.

Preview your own pages only (safe to run while others work in parallel):

    cd /home/user/Ray2Volt-Solar-Website/brochure && node build.js --png --only=NN[,NN]

This prints layout problems (overflow, text spilling out of an SVG, big empty gaps) and writes `preview/NN-name.png`. **Open the PNG with the Read tool and look at it critically after every build.** Iterate until it is clean: no overlapping labels, no arrows crossing text, nothing cramped, nothing clipped, no large empty area. Expect to need several rounds. Each page is a fixed 210 × 297 mm; content must fill it comfortably and must not overflow.

Only create or edit your own page files. Do not edit `base.css`, `sprite.svg`, `build.js` or other pages; if you need a one-off style, put it inline or in a `<style>` block inside your page scoped to a class unique to your page (prefix it `pNN-`). Do not run `node build.js` without `--only`. Do not commit.

## Page skeleton

    <section class="page" data-sec="basics|metering|access|money|guide">
      <header class="ph"><span class="sec">Chapter &nbsp;·&nbsp; Topic</span><img src="{{LOGO}}" alt="Ray2Volt"></header>
      <div class="pb">
        <div>
          <div class="kicker">…</div>
          <h1 class="title">Plain words: <em>the key idea in accent colour</em></h1>
          <p class="lede">Two or three sentences that explain the idea to a complete newcomer.</p>
        </div>
        … infographic(s) and cards …
      </div>
      <footer class="pf"><span>{{FOOT}}</span><span class="pn">{{PN}}</span></footer>
    </section>

`data-sec` sets the page's accent colour. Give the last block in `.pb` the class `grow` so the page fills to the bottom.

## Design rules — corporate, data-led (the client rejected an earlier illustrated style as "cartoonish")

The register is an annual report or a consulting firm's client briefing: generous white space, hairline rules, restrained colour, light large numerals, and **charts and schematics that carry real information**. Nothing cute.

- **No illustration.** No drawn buildings, suns, landscapes, characters or scenery; no filled multi-colour icons; no gradients, shadows, glows, blobs or decorative shapes; no big rounded bubbles or pills; no emoji. If a graphic would not look at home in a bank's annual report, do not draw it.
- **Every page is built around exhibits**, titled like the reference page: `<div class="fig-title">Exhibit 1 &nbsp;·&nbsp; Title <span>Unit or "Schematic" / "Illustrative"</span></div>`. Aim for two or three exhibits a page, and choose the form that fits the idea:
  - quantities flowing between parties → **Sankey ribbons** (see Exhibit 2 on page 07: `.band` ribbons, 6px node bars, light `num` numerals with `cap` labels);
  - something changing over a day or over years → **line / area chart** with a baseline `.axis`, `.gridline`s, `.tick` labels and direct labels on the series (Exhibit 3 on page 07);
  - comparing amounts → **bar chart** with an axis and values printed at the bar ends; a build-up or breakdown → **waterfall or stacked bar**; shares → **a single stacked bar or a donut**, never a pie with many slices;
  - how things are connected or who deals with whom → **block schematic** (Exhibit 1 on page 07: `.node` rectangles 2px radius, a 21px line icon, `lbl` title + `lbl-s` subtitle, thin `.flow` connectors that run only horizontally or vertically);
  - a process → **numbered timeline** on a hairline; a choice → **decision matrix or tree** with thin connectors; thresholds → **gauges or scale bars** with marked limits.
  Compute chart geometry properly (write a small script if needed) so bars, curves and ribbons are to scale. Charts with invented data must say "Illustrative" in the exhibit title.
- **Colour is functional and sparing.** Gold = solar power, blue = grid power, green = exported power / savings / "green", violet = battery storage, red = cost or caution, navy = totals and ink, grey = baseline or "without solar". Use the `.f-*` fill, `.s-*` stroke, `.c-*` text and `.flow.*` classes. Most of each page is white, navy and grey; colour appears in the data, not in the furniture. Do not fill cards with colour to decorate them; prefer open `.card.top` blocks (a rule above, no box) for text and keep tinted backgrounds for exhibits (`.fig`, or `.fig.plain` for a hairline frame).
- **Icons** are thin-line and monochrome, used small (about 20px in a schematic node, or in a `.badge`) and only where they help identify a node — never as decoration and never large. Sprite ids: sun, panel, house, house-solar, factory, office, apartment, pylon, meter, meter-bi, inverter, battery, plug, bulb, rupee, leaf, bank, doc, transformer, solarfarm, shop, farm, investor, handshake, shield, clock, moon, cloud-co2, chart, board, people. They take `currentColor`. If you need another, draw it the same way: 64×64 viewBox, `fill="none" stroke="currentColor" stroke-width="2.6"`, round caps and joins.
- **Type:** the page title is one or two bold words or a short phrase, and the `<em>` inside it is automatically set as a lighter second line (see page 07): `<h1 class="title">Net metering <em>One meter that counts in both directions</em></h1>`. SVG text classes: `cap` (tiny letter-spaced capitals for labels), `lbl`, `lbl-s`, `lbl-b`, `num` (large light numeral), `num-b`, `tick`. Never smaller than 6.4px in a viewBox about 680 wide (scale down proportionally for narrower viewBoxes). Keep labels horizontal, beside what they label, clear of lines.
- **Components** (see base.css): `.card` and `.card.top`, `.callout` (a left rule; add `.box` for a grey ground), `.steps` (01, 02 …), `ul.ticks / .crosses / .dots`, `.stat` (large light numeral + label; `.stat.rule` adds a rule above — good in a row of three or four as a figures band), `.chips/.chip`, `.legend` (square swatches; `i.ln` for a line swatch), `.eq` equation tiles, `.bars/.bar`, `table.cmp` (ruled table; add class `num` to right-align numeric cells), `.row`, `.cols-2/3/4`, `.badge`, `.head-row`, `.small`, `.tiny`.
- Give every SVG a `viewBox`, `role="img"` and an `aria-label` that states what the exhibit shows. Do not change fonts or shrink body text to make things fit — cut words instead. Fill the page: no large empty areas, nothing overflowing.

## Writing rules

- Plain, exact, professional English — the voice of a well-edited briefing, not an advertisement and not a children's book. Short sentences. Explain every term the first time it appears on your page, in a few words ("the DISCOM, your local electricity distribution company"). Call a kWh a "unit" after introducing it. Use ₹ and Indian terms (lakh, crore) where money appears.
- Do not address a particular kind of reader ("as a homeowner…"). Where a concept suits some situations more than others, say which.
- No hype and no promises: nothing like "guaranteed savings", "zero bills", "free electricity", no exclamation marks. This is a guide, not an advertisement. Ray2Volt is mentioned only in the header/footer unless your page spec says otherwise.
- **Facts:** use only what is in `src/FACTS.md`, and keep its hedged wording where it hedges. Rules differ by state and change often, so say "set by your State Electricity Regulatory Commission" rather than inventing a number. Do not add statistics, rupee figures, percentages, dates or regulation names from memory. Illustrative numbers must be labelled as illustrative.
- **The shared worked example** (use it wherever a page shows billing, so readers can compare pages): a home uses **500 units a month**; its **3 kW** plant makes about **360 units**; **140** are used directly, **220** go to the grid, **360** come from the grid. Illustrative rates: grid power **₹7 per unit**, exported power **₹3 per unit**. Bill without solar ₹3,500. Net metering: pays for 140 units = ₹980. Net billing: ₹2,520 − ₹660 = ₹1,860. Gross metering: pays ₹3,500 for use, earns 360 × ₹3 = ₹1,080, net ₹2,420. Always note that rates are illustrative, that real tariffs have slabs and fixed charges, and that export rates are set by each state.

## When you finish

Reply with: the files you wrote, a one-line description of each page's infographic, any fact you needed that FACTS.md did not cover (and how you worded around it), and anything you are unsure renders well.
