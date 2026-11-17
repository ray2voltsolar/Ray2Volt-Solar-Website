# Builder guide — Ray2Volt brochure pages

The brochure is "Solar & Green Energy, Explained", an 18-page A4 portrait guide from Ray2Volt Solar Private Limited (a solar company in Andhra Pradesh, India). A bank manager will hand it to their clients, and we do not know who those clients are: a retired teacher, a shop owner, a factory owner, an investor, a farmer. So every page must make sense to someone who has never thought about electricity, without talking down to someone who runs a factory. It has to look like a professionally designed publication, and the infographic on each page carries the explanation — a reader who only looks at the pictures should still get the idea.

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

## Design rules

- **One main infographic per page**, drawn as inline SVG inside `<div class="fig">`, taking roughly a third to a half of the page. Then one or two supporting blocks (worked example, comparison, cards). Do not make a page of text boxes.
- **Colour means the same thing everywhere:** gold = solar power, blue = grid power, green = power exported / savings / "green", violet = battery storage, red = cost or caution, navy = totals and ink. Use the `.flow.solar / .grid / .export / .store / .money / .plain` line classes and the `.c-*` text classes. If a figure uses colours a reader must decode, add a `.legend`.
- **Icons:** use the sprite (`<use href="#i-house-solar" x y width height/>`; all are 64×64 viewBoxes). Available: sun, panel, house, house-solar, factory, office, apartment, pylon, meter, meter-bi, inverter, battery, plug, bulb, rupee, leaf, bank, doc, transformer, solarfarm, shop, farm, investor, handshake, shield, clock, moon, cloud-co2. Draw anything else you need in the same style: flat, rounded, white fill with a 2.6px navy (#0A2540) outline plus brand-colour details. No emoji, no clip-art, no photos.
- **SVG text:** use classes `lbl` (9px bold), `lbl-s` (7.5px muted), `lbl-b` (11px extra-bold), `num` (15px). Never smaller than 7px in a viewBox about 680 wide. Keep labels horizontal, next to what they label, clear of lines and arrowheads. Give every SVG a `viewBox`, `role="img"` and an `aria-label`.
- **Components available** (see base.css): `.card` (+ `.tint .blue .cyan .gold .green .red .violet .grey .dark .top`), `.callout` (+ `.note .ok .warn`), `.steps`, `ul.ticks / .crosses / .dots`, `.stat`, `.chips/.chip`, `.legend`, `.eq` equation tiles, `.bars/.bar` stacked bars, `table.cmp`, `.row`, `.cols-2/3/4`, `.badge`, `.head-row`, `.small`, `.tiny`.
- Typography is set by the design system (Montserrat headings, Nunito Sans body). Do not change fonts or shrink body text to make things fit — cut words instead.

## Writing rules

- Plain, warm, exact English. Short sentences. Explain every term the first time it appears on your page, in a few words ("the DISCOM, your local electricity distribution company"). Call a kWh a "unit" after introducing it. Use ₹ and Indian terms (lakh, crore) where money appears.
- Do not address a particular kind of reader ("as a homeowner…"). Where a concept suits some situations more than others, say which.
- No hype and no promises: nothing like "guaranteed savings", "zero bills", "free electricity", no exclamation marks. This is a guide, not an advertisement. Ray2Volt is mentioned only in the header/footer unless your page spec says otherwise.
- **Facts:** use only what is in `src/FACTS.md`, and keep its hedged wording where it hedges. Rules differ by state and change often, so say "set by your State Electricity Regulatory Commission" rather than inventing a number. Do not add statistics, rupee figures, percentages, dates or regulation names from memory. Illustrative numbers must be labelled as illustrative.
- **The shared worked example** (use it wherever a page shows billing, so readers can compare pages): a home uses **500 units a month**; its **3 kW** plant makes about **360 units**; **140** are used directly, **220** go to the grid, **360** come from the grid. Illustrative rates: grid power **₹7 per unit**, exported power **₹3 per unit**. Bill without solar ₹3,500. Net metering: pays for 140 units = ₹980. Net billing: ₹2,520 − ₹660 = ₹1,860. Gross metering: pays ₹3,500 for use, earns 360 × ₹3 = ₹1,080, net ₹2,420. Always note that rates are illustrative, that real tariffs have slabs and fixed charges, and that export rates are set by each state.

## When you finish

Reply with: the files you wrote, a one-line description of each page's infographic, any fact you needed that FACTS.md did not cover (and how you worded around it), and anything you are unsure renders well.
